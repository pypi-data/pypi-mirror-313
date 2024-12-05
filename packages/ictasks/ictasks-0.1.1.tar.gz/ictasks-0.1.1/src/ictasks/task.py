"""
This module describes a task, i.e. a small unit of work
"""

from pathlib import Path
import logging

from pydantic import BaseModel

from iccore.filesystem import read_file, get_dirs
from iccore.serialization import read_json, write_model
from iccore.string_utils import split_strip_lines


logger = logging.getLogger(__name__)


class Task(BaseModel):
    """
    This is a computational task executed as a process with a launch command.
    :param id: An identifier for the task
    :param launch_cmd: The command to launch the task as a process
    :param state: The current state of the task
    :param return_code: The return code from the task process.
    :param launch_time: The time the process was launched at
    :param finish_time: The time the process finished at
    :param worker_id: Identifier of the worker the task ran on
    :param host_id: Identifier of the host the task ran on
    :param pid: Identifier for the task process
    """

    id: str
    launch_cmd: str
    state: str = "created"
    return_code: int = 0
    launch_time: float = 0.0
    finish_time: float = 0.0
    worker_id: int = -1
    host_id: int = -1
    pid: int = 0

    @property
    def is_finished(self) -> bool:
        return self.state == "finished"

    @property
    def is_running(self) -> bool:
        return self.state == "running"


def get_task_dirname(task: Task) -> Path:
    """
    Get the task's directory name as a Path
    """
    return Path(f"task_{task.id}")


def write(path: Path, task: Task, filename: str = "task.json"):
    """
    Write the task to file
    """
    write_model(task, path / get_task_dirname(task) / filename)


def read(path: Path, filename: str = "task.json") -> Task:
    """
    Read a task from the given path
    """
    return Task(**read_json(path / filename))


def read_all(path: Path) -> list[Task]:
    """
    Read all tasks in a given directory
    """
    return [read(eachDir) for eachDir in get_dirs(path, "task_")]


def load_taskfile(content: str) -> list[Task]:
    """
    Load tasks from a string, with one launch command per line.
    The string %TASKNUM% will be replaced with the task id.
    """
    lines = split_strip_lines(content)
    return [
        Task(id=str(idx), launch_cmd=lines[idx].replace("%TASKID%", str(idx)))
        for idx in range(len(lines))
    ]


def read_taskfile(path: Path) -> list[Task]:
    """
    Read tasks from a file, with one launch command per line.
    """
    logger.info("Reading tasks from: %s", path)
    return load_taskfile(read_file(path))
