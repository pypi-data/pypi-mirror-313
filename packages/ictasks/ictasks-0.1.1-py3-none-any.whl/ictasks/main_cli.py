"""
Main entry point for ictasks
"""

import os
from pathlib import Path
import argparse
import logging
import queue
from functools import partial

from iccore import logging_utils
from iccore.serialization import read_yaml
from icsystemutils.cluster.node import ComputeNode

import ictasks
from ictasks.session import SessionConfig

logger = logging.getLogger(__name__)


def taskfarm(args):

    logging_utils.setup_default_logger()

    if args.config.resolve().exists():
        raw_config = read_yaml(args.config.resolve())
        config = SessionConfig(**raw_config)
    else:
        config = SessionConfig()

    if config.slurm_job:
        nodes = [ComputeNode(address=a) for a in config.slurm_job.nodes]
    else:
        nodes = [ComputeNode(address="localhost")]

    tasks = ictasks.task.read_taskfile(args.tasklist.resolve())
    task_queue = queue.Queue()
    for task in tasks:
        task_queue.put(task)

    work_dir = args.work_dir.resolve()
    write_task_func = partial(ictasks.task.write, work_dir)
    ictasks.session.run(
        task_queue, work_dir, config, nodes, write_task_func, write_task_func
    )


def main_cli():

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dry_run",
        type=int,
        default=0,
        help="Dry run script - 0 can modify, 1 can read, 2 no modify - no read",
    )
    subparsers = parser.add_subparsers(required=True)

    taskfarm_parser = subparsers.add_parser("taskfarm")

    taskfarm_parser.add_argument(
        "--work_dir",
        type=Path,
        default=Path(os.getcwd()),
        help="Directory to run the session in",
    )
    taskfarm_parser.add_argument("--config", type=Path, help="Path to a config file")
    taskfarm_parser.add_argument("--tasklist", type=Path, help="Path to tasklist file")

    taskfarm_parser.set_defaults(func=taskfarm)
    args = parser.parse_args()

    args.func(args)


if __name__ == "__main__":
    main_cli()
