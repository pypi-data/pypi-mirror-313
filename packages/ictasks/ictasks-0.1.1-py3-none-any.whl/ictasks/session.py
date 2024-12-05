"""
This module is for a single batch job or session
"""

import time
import logging
import uuid
from pathlib import Path
import os
import copy
from queue import Queue, SimpleQueue
from typing import Callable
from functools import partial

from pydantic import BaseModel

from iccore.system.process import ProcessLauncher
from icsystemutils.cluster.node import ComputeNode
from icsystemutils.cpu import cpu_info

import ictasks
from ictasks.scheduler.schedulers import slurm
from .task import Task, get_task_dirname
from .worker import WorkerHost, Worker
from .stopping_condition import StoppingCondition
from .scheduler.schedulers.slurm import SlurmJob

logger = logging.getLogger(__name__)


class SessionConfig(BaseModel):
    """This class represents a single batch job or session

    Attributes:
        job_id (str): Idenitifier for the job or session
        nodelist (:obj:`list`): List of compute nodes available to run on
        tasks_path (:obj:`Path`): Path to a list of tasks to run
    """

    job_id: str = ""
    cores_per_node: int = 0
    threads_per_core: int = 1
    cores_per_task: int = 1
    stopping_conditions: list[StoppingCondition] = []
    stop_on_error: bool = True
    stdout_filename: str = "task_stdout.txt"
    stderr_filename: str = "task_stderr.txt"
    slurm_job: SlurmJob | None = None

    def model_post_init(self, __context):
        slurm_id = slurm.get_id()
        if not self.slurm_job and slurm_id:
            self.slurm_job = SlurmJob(id=slurm_id)

        if not self.job_id:
            if self.slurm_job:
                self.job_id = slurm_id
            else:
                self.job_id = str(uuid.uuid4())


def _on_task_finished(
    workers: SimpleQueue[tuple[WorkerHost, Worker]],
    tasks: Queue[Task],
    on_task_completed: Callable | None,
    task: Task,
    host_worker: tuple[WorkerHost, Worker],
    pid: int,
    returncode: int,
):
    """
    This is called when a task is finished. We update the task and worker
    queues (which are thread safe) and if a user completion callback is provided
    we fire it.
    """

    tasks.task_done()
    workers.put(host_worker)

    logging.info("Task %s on pid %d finished with code %d", task.id, pid, returncode)

    if on_task_completed:
        finished_task = copy.deepcopy(task)
        finished_task.pid = pid
        finished_task.state = "finished"
        finished_task.finish_time = time.time()
        finished_task.return_code = returncode
        on_task_completed(finished_task)


def _launch_task(
    host_worker: tuple[WorkerHost, Worker],
    launcher: ProcessLauncher,
    on_task_finished: Callable,
    work_dir: Path,
    config: SessionConfig,
    task: Task,
    on_task_launched: Callable | None,
):
    """
    Launch the task async on the allotted worker and host
    """

    # Write the pre-launch state to file
    ictasks.task.write(work_dir, task)

    host, worker = host_worker
    if config.slurm_job:
        cmd = f"srun -env I_MPI_PIN_PROCESSOR_LIST {worker.cores.as_string()} -n"
        cmd += f"{config.cores_per_task} --host {host.address} {task.launch_cmd}"
    else:
        cmd = task.launch_cmd

    task_dir = work_dir / get_task_dirname(task)

    launched_task = copy.deepcopy(task)
    launched_task.launch_time = time.time()
    launched_task.state = "running"
    launched_task.host_id = host.id
    launched_task.worker_id = worker.id

    # Launch the task async, it will fire the provided callback when
    # finished
    proc = launcher.run(
        cmd,
        task_dir,
        stdout_path=task_dir / config.stdout_filename,
        stderr_path=task_dir / config.stderr_filename,
        callback=partial(
            on_task_finished,
            launched_task,
            (host, worker),
        ),
    )

    if on_task_launched:
        launched_task.pid = proc.pid
        on_task_launched(launched_task)

    logger.info("Task %s launched with pid: %d", task.id, proc.pid)


def _setup_worker_queue(
    config: SessionConfig, nodes: list[ComputeNode]
) -> SimpleQueue[tuple[WorkerHost, Worker]]:
    """
    Find available workers, one per available processor across
    compute nodes and add them to a queue.
    """
    if config.cores_per_node == 0:
        cpu = cpu_info.read()
        cores_per_node = cpu.cores_per_node
        threads_per_core = cpu.threads_per_core
    else:
        cores_per_node = config.cores_per_node
        threads_per_core = config.threads_per_core

    cores_per_task = config.cores_per_task
    hosts = ictasks.worker.load(nodes, cores_per_node, threads_per_core, cores_per_task)
    workers: SimpleQueue[tuple[WorkerHost, Worker]] = SimpleQueue()
    for host in hosts:
        for worker in host.workers:
            workers.put((host, worker))
    return workers


def run(
    tasks: Queue[Task],
    work_dir: Path = Path(os.getcwd()),
    config: SessionConfig = SessionConfig(),
    nodes: list[ComputeNode] | None = None,
    on_task_launched: Callable | None = None,
    on_task_completed: Callable | None = None,
):
    """
    Run the session by iterating over all tasks and assigning them to waiting workers.
    :param config: The configuration for this run
    :param tasks: A queue populated with tasks to run
    :param nodes: Compute nodes to run tasks on, defaults to localhost if not provided
    :param work_dir: Directory to write output to
    :param on_task_launched: Callback fired when a task launches
    :param on_task_complete: Callback fired when a task completes
    """

    if not nodes:
        nodes = [ComputeNode(address="localhost")]

    workers = _setup_worker_queue(config, nodes)
    launcher = ProcessLauncher()

    logger.info("Starting with %d workers and %d tasks", workers.qsize(), tasks.qsize())
    while not tasks.empty():
        task = tasks.get()
        logger.info(
            "Launching task id: %s. %d remaining in queue.", task.id, tasks.qsize()
        )
        host_worker = workers.get()
        _launch_task(
            host_worker,
            launcher,
            partial(_on_task_finished, workers, tasks, on_task_completed),
            work_dir,
            config,
            task,
            on_task_launched,
        )

    logger.info("Task queue is empty. Waiting for running tasks to finish.")
    tasks.join()
    logger.info("Task queue is empty and all tasks finished, stopping run.")
