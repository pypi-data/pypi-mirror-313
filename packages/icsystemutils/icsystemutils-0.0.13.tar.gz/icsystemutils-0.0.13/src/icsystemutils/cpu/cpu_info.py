"""
This module allows calculation and storage of cpu info
"""

import sys

from pydantic import BaseModel

from icsystemutils.cpu import proc_info, sys_ctl

from .cpu import PhysicalProcessor


class CpuInfo(BaseModel, frozen=True):
    """Information on a system's CPUs

    :param list[PhysicalProcessor] physical_procs: Collection of physical processors
    :param int threads_per_core: Number of threads available per processor core
    :param int cores_per_node: Number of cores per compute node (network location)
    """

    physical_procs: list[PhysicalProcessor]
    threads_per_core: int = 1
    cores_per_node: int = 1


def read() -> CpuInfo:

    if sys.platform == "darwin":
        procs = sys_ctl.read()
    else:
        procs = proc_info.read()

    # This is assuming all processors have same number of cores
    # and all cores have same number of threads
    first_proc = procs[0]
    cores_per_node = len(first_proc.cores)
    threads_per_core = first_proc.cores[0].num_threads

    return CpuInfo(
        physical_procs=procs,
        cores_per_node=cores_per_node,
        threads_per_core=threads_per_core,
    )
