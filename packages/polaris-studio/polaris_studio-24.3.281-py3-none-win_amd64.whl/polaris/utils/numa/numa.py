# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
import psutil
import itertools
import logging
import os
from pathlib import Path
import socket
from tempfile import gettempdir
from typing import List

from polaris.utils.file_utils import readlines
from polaris.utils.list_utils import first_and_only
from polaris.utils.numa.numa_hardware_report import NumaHardware, NumaNodeHardware, numactl


def numa_available():
    if numactl is None:
        return False
    return NumaHardware.from_cli().available


def read_nodes_in_use():
    nodes_in_use = set()
    logging.info(f"Looking for numa files in {gettempdir()}")
    for f in Path(str(gettempdir())).glob(f"pstudio_proc_{socket.gethostname()}_*"):
        pid = int(f.name.split("_")[-1])
        if psutil.pid_exists(pid):
            logging.info(f"  => Found {f} which has a running pid")
            line = first_and_only(e for e in readlines(f) if "numa nodes:" in e)
            nodes_in_use = set.union(nodes_in_use, [int(e) for e in line.strip().split(":")[1].strip().split(" ")])
        else:
            logging.info(f"  => Deleting numa node allocation file {f} as pid no longer exists")
            f.unlink()

    return nodes_in_use


def write_nodes_in_use(nodes_to_use: List[NumaNodeHardware]):
    numa_options_file = Path(gettempdir()) / f"pstudio_proc_{socket.gethostname()}_{os.getpid()}"
    nodes = " ".join(str(e.node_id) for e in nodes_to_use)
    with open(numa_options_file, "w") as fp:
        fp.write(f"numa nodes: {nodes}")
        logging.info(f"Numa node file: {numa_options_file} - {nodes}")
    return numa_options_file


def get_numa_nodes_to_use(num_threads, numa_report=None, nodes_in_use=None):
    logging.info("Getting numa nodes to use")
    numa_report = numa_report or NumaHardware.from_cli()

    # Figure out what nodes aren't in use
    node_ids_in_use = [e.node_id for e in nodes_in_use] if nodes_in_use is not None else read_nodes_in_use()
    nodes_available = [n for n in numa_report.nodes if n.node_id not in node_ids_in_use]

    # How many CPUs each provides
    node_counts = [n.num_cpus for n in nodes_available]
    node_count_cumulative = zip(nodes_available, list(itertools.accumulate(node_counts)))

    # How many we will need to hit our desired thread count
    nodes_to_use = []
    for n, count in node_count_cumulative:
        nodes_to_use.append(n)
        if count > num_threads:
            break
    return nodes_to_use


def get_numactl_opts(nodes_to_use: List[NumaNodeHardware]):
    cpu_bind = f"--cpunodebind={','.join(str(e.node_id) for e in nodes_to_use)}"

    # mem_bind = f"--membind={','.join(str(e.node_id) for e in nodes_to_use)}"
    # We have removed the membind option as it was being too restrictive when calculated from the
    # core requirement - i.e. 2 nodes might be enough CPU but won't provide enough memory for the
    # model. This could be better handled by estimating (or user providing) the memory requirements
    # and then reserving nodes sufficient for the larger of the two (cpu reqs or mem requirements)
    # return ["numactl", cpu_bind, mem_bind]
    return ["numactl", cpu_bind]
