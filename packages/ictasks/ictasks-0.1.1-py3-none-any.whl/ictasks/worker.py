import logging
from pathlib import Path

from pydantic import BaseModel

from iccore.filesystem import read_file_lines
from iccore.base_models import Range
from icsystemutils.cluster.node import ComputeNode


logger = logging.getLogger(__name__)


class Worker(BaseModel):

    id: int
    cores: Range


class WorkerHost(BaseModel):

    id: int
    node: ComputeNode
    workers: list[Worker] = []

    @property
    def address(self) -> str:
        return self.node.address


def _get_core_range(proc_id: int, cores_per_node: int, cores_per_task: int) -> Range:
    start = proc_id % cores_per_node * cores_per_task
    end = start + cores_per_task - 1
    return Range(start=start, end=end)


def load(
    nodes: list[ComputeNode],
    cores_per_node: int,
    threads_per_core: int,
    cores_per_task: int,
) -> list[WorkerHost]:
    logger.info("Setting up workers")

    num_procs = int(cores_per_node / cores_per_task) * threads_per_core
    return [
        WorkerHost(
            id=idx,
            node=node,
            workers=[
                Worker(
                    id=proc_id % cores_per_node,
                    cores=_get_core_range(proc_id, cores_per_node, cores_per_task),
                )
                for proc_id in range(num_procs)
            ],
        )
        for idx, node in enumerate(nodes)
    ]


def read(
    path: Path, cores_per_node: int, threads_per_core: int, cores_per_task: int
) -> list[WorkerHost]:
    logger.info("Reading nodefile at: %s, path")

    nodes = [ComputeNode(address=line) for line in read_file_lines(path)]
    return load(nodes, cores_per_node, threads_per_core, cores_per_task)
