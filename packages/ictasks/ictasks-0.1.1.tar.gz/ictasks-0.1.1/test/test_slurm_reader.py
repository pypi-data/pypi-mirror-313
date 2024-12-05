from pathlib import Path

from ictasks.scheduler.schedulers import slurm
from ictasks.scheduler.schedulers.slurm import SlurmJob


def get_test_data_dir():
    test_dir = Path(__file__).parent
    return test_dir / "data"


def test_slurm_reader():
    pass


def test_slurm_job():
    nodelist_path = get_test_data_dir() / "sample_nodelist.dat"
    with open(nodelist_path, 'r') as f:
        nodelist = f.read()

    job = slurm.load_job(nodelist)
    assert len(job.nodes) == 12
