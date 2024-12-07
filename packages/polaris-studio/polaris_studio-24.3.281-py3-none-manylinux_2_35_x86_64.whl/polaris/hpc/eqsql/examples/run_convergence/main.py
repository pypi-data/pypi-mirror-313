# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
import json
import logging
import os
import sys
import traceback
from pathlib import Path
from shutil import rmtree
from socket import gethostname

from custom_callbacks import (
    iterations_fn,
    pre_loop_fn,
    start_of_loop_fn,
    get_scenario_json_fn,
    end_of_loop_fn,
    async_end_of_loop_fn,
    post_loop_fn,
    build_polaris_crash_handler,
)
from polaris.hpc.eqsql.task_container import TaskContainer
from polaris.project.polaris import Polaris
from polaris.runs.convergence.convergence_config import ConvergenceConfig
from polaris.utils.copy_utils import magic_copy
from polaris.utils.env_utils import get_data_root, where_am_i_running
from polaris.utils.logging_utils import function_logging


def example_json():
    return {
        "run-id": "jamie_test_run",
        "where-is-polaris-exe": f"/mnt/p/VMS_Software/15-CI-CD-Artifacts/Polaris/polaris-linux/develop/latest/ubuntu-20.04/Integrated_Model",
        "where-is-base-model": "/mnt/p/VMS_Software/15-CI-CD-Artifacts/Polaris/models/RUN/Grid",
        "put-logs-here": "~/logs",
    }


def main(payload):
    # We get a task container helper object to allow us to log messages back to the db
    task_container = TaskContainer.from_env(payload)

    run_id = "not-specified"
    try:
        run_id = payload.get("run-id")
        model = setup_run(task_container, run_id)
        model.run_config = configure_run(task_container, model.run_config)
        model.upgrade()
        model.run(
            pre_loop_fn=pre_loop_fn,
            start_of_loop_fn=start_of_loop_fn,
            iterations_fn=iterations_fn,
            scenario_file_fn=get_scenario_json_fn,
            end_of_loop_fn=end_of_loop_fn,
            async_end_of_loop_fn=async_end_of_loop_fn,
            post_loop_fn=post_loop_fn,
            polaris_crash_handler=build_polaris_crash_handler(model.run_config),
        )

        # report_run() # send back runstats to eq/sql
        # update_job(run_id, "FINISHED", "Completed all required steps")
    except Exception:
        tb = traceback.format_exc()
        # update_job(run_id, "FAILED", tb)
        print(tb, flush=True)
        logging.critical(tb)
        exit(1)


def setup_run(task_container, run_id):
    payload = task_container.payload
    run_dir = get_data_root() / "models"
    model_dir = run_dir / f"{run_id}"

    print(f"Local Run Dir: {model_dir}")

    models_src_dir = Path(os.path.expanduser(payload["where-is-base-model"])).resolve()

    # copy model
    if model_dir.exists() and payload.get("overwrite-model-files", True):
        rmtree(model_dir)
        magic_copy(models_src_dir, model_dir)
    elif not model_dir.exists():
        magic_copy(models_src_dir, model_dir)

    model = Polaris.from_dir(model_dir)

    # # We store the payload on the config object to allow for later callbacks to use the information therein
    model.run_config.user_data = task_container.payload

    if "where-is-polaris-exe" in payload:
        exe = payload["where-is-polaris-exe"]
        if isinstance(exe, dict):
            lu = {where_am_i_running(k): v for k, v in exe.items()}
            exe = lu[where_am_i_running()]

        model.run_config.polaris_exe = exe
    else:
        raise RuntimeError("no exe defined")

    task_container.log("Finished copying files")

    return model


# def setup_logging(remote_dir, local_dir):
#     date_stamp = datetime.datetime.now().strftime("%Y%m%d_%H-%M-%S")

#     handlers = []

#     # if we are running on bebop, the /mnt/q drives won't be mounted, so don't try to stream output there
#     if Path(remote_dir).parent.exists():
#         mkdir_p(remote_dir)
#         handlers.append(FileHandler(os.path.join(remote_dir, f"convergence_runner_{date_stamp}_{gethostname()}.log")))

#     mkdir_p(local_dir)
#     handlers.append(FileHandler(os.path.join(local_dir, f"convergence_runner_{date_stamp}_{gethostname()}.log")))
#     handlers.append(logging.StreamHandler(sys.stdout))

#     logging.basicConfig(handlers=handlers, force=True, format="%(asctime)s - %(levelname)s - %(message)s")
#     return str(remote_dir)


@function_logging("Configuring Run")
def configure_run(task_container: TaskContainer, config: ConvergenceConfig):
    payload = task_container.payload
    if "run-config" not in task_container.payload:
        return config

    run_config = payload["run-config"]
    config.set_from_dict(run_config)
    task_container.log("Finished configuring")

    return config


def run_run(model):
    logging.info(f"Running Polaris Convergence {str(model.model_path)} on {gethostname()}")


if __name__ == "__main__":
    filename = sys.argv[1]
    with open(filename, "r") as f:
        payload = json.loads(f.read())
    main(payload)
