from pathlib import Path
import os
import shutil
import queue
from functools import partial

import ictasks.session
import ictasks.task
from ictasks.task import Task


def test_basic_tasks_session():

    work_dir = Path(os.getcwd()) / "test_basic_tasks_session"

    task_queue = queue.Queue()
    task_queue.put(Task(id="0", launch_cmd="echo 'hello from task 0'"))
    task_queue.put(Task(id="1", launch_cmd="echo 'hello from task 1'"))

    write_task_func = partial(ictasks.task.write, work_dir)
    
    ictasks.session.run(task_queue, work_dir,
                        on_task_launched = write_task_func,
                        on_task_completed = write_task_func)

    shutil.rmtree(work_dir)
    

