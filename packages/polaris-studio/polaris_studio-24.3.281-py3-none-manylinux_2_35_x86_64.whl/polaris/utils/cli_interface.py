# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
# !/usr/bin/env python

from pathlib import Path
import click

from polaris.project.polaris import Polaris  # noqa: E402
from polaris.project.project_restorer import restore_project_from_csv
from polaris.utils.logging_utils import stdout_logging
from polaris.runs import summary


@click.group(invoke_without_command=False)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        click.echo("You can only invoke commands run, upgrade or build_from_git")


@cli.command()  # type: ignore
@click.option("--data_dir", required=True, help="Model directory")
@click.option(
    "--config_file",
    required=False,
    help="Convergence control file override. Defaults to convergence_control.yaml",
    default=None,
)
@click.option("--num_threads", required=False, help="Number of threads to use for model run", type=int)
@click.option(
    "--population_scale_factor", required=False, help="Population sampling factor", type=click.FloatRange(0.0001, 1.0)
)
@click.option(
    "--upgrade", required=False, help="Whether we want to upgrade the model to the latest structure before running it"
)
@click.option(
    "--do_pop_synth/--no_pop_synth",
    required=False,
    default=None,
    help='Override the "should run population sythesizer" flag from convergence_control.yaml',
)
@click.option(
    "--do_skim/--no_skim",
    required=False,
    default=None,
    help='Override the "should run skimming" flag from convergence_control.yaml',
)
@click.option(
    "--do_abm_init/--no_abm_init",
    required=False,
    default=None,
    help="Override the 'should run abm_init iteration' flag from convergence_control.yaml ",
)
@click.option(
    "--polaris_exe",
    required=False,
    help="Path to the polaris executable to be used. Defaults to the executable shipped with polaris",
)
@click.option(
    "--num_abm_runs",
    required=False,
    help="Number of ABM runs to be run. Defaults to the value in convergence_control.yaml",
    type=int,
)
@click.option(
    "--start_iteration_from",
    required=False,
    help="Start running from this iteration. Defaults to the value in convergence_control.yaml",
    type=int,
)
def run(
    data_dir,
    config_file,
    upgrade,
    num_threads,
    population_scale_factor,
    do_pop_synth,
    do_skim,
    do_abm_init,
    polaris_exe,
    num_abm_runs,
    start_iteration_from,
):
    stdout_logging()
    model = Polaris.from_dir(data_dir, config_file=config_file)

    if upgrade:
        model.upgrade()

    args = {
        "num_threads": num_threads,
        "do_pop_synth": do_pop_synth,
        "do_skim": do_skim,
        "do_abm_init": do_abm_init,
        "polaris_exe": polaris_exe,
        "num_abm_runs": num_abm_runs,
        "start_iteration_from": start_iteration_from,
        "population_scale_factor": population_scale_factor,
    }
    args = {k: v for k, v in args.items() if v is not None}
    model.run(**args)


@cli.command()  # type: ignore
@click.option("--data_dir", required=True, help="Model directory")
@click.option("--force", required=False, help="Force the application of the given migration ID", multiple=True)
def upgrade(data_dir, force):
    stdout_logging()
    model = Polaris.from_dir(data_dir)
    model.upgrade(force_migrations=force)


@cli.command()  # type: ignore
@click.option("--data_dir", required=True, help="Target model directory")
@click.option("--city", required=True, help="City model to build - corresponds to the git repository")
@click.option("--db_name", required=False, help="DB name. Defaults to the value in abm_scenario.json", default=None)
@click.option(
    "--overwrite",
    required=False,
    help="Overwrite any model in the target directory. Defaults to False",
    default=False,
)
@click.option(
    "--inplace",
    required=False,
    help="Build in place or a sub-directory. Defaults to subdirectory",
    is_flag=True,
    default=False,
)
@click.option("--upgrade", required=False, help="Whether we should upgrade the model after building it")
def build_from_git(data_dir, city, db_name, overwrite, inplace, upgrade):
    stdout_logging()
    model = Polaris.build_from_git(model_dir=data_dir, city=city, db_name=db_name, overwrite=overwrite, inplace=inplace)
    if upgrade:
        model.upgrade()


@cli.command()  # type: ignore
@click.option("--data_dir", required=True, help="Target model directory")
@click.option("--city", required=True, help="City model to build - corresponds to the git repository")
@click.option("--upgrade", required=False, help="Whether we should upgrade the model after building it")
def build(data_dir, city, upgrade):
    stdout_logging()
    restore_project_from_csv(data_dir, data_dir, city, True)
    if upgrade:
        Polaris.from_dir(data_dir).upgrade()


@cli.command()  # type: ignore
@click.option("--data_dir", required=True, help="Target model directory")
def aggregate_summaries(data_dir):
    summary.aggregate_summaries(Path(data_dir), save=True)


@cli.command()  # type: ignore
@click.option("--license_path", required=True, help="Adds the license to the Python installation folder")
def add_license(license_path):
    from shutil import copy

    if not Path(license_path).exists():
        raise FileNotFoundError(f"License file not found: {license_path}")

    bin_folder = Path(__file__).parent.parent / "bin"
    copy(license_path, bin_folder)


if __name__ == "__main__":
    cli()  # type: ignore
