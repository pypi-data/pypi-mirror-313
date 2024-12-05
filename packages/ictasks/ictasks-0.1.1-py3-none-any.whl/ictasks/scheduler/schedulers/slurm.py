import os

from pydantic import BaseModel


class SlurmJob(BaseModel):
    id: str = ""
    nodes: list[str] = []


def get_id() -> str:
    job_id = os.environ.get("SLURM_JOB_ID")
    if job_id:
        return job_id
    return ""


def get_nodelist() -> str:
    nodelist = os.environ.get("SLURM_JOB_NODELIST")
    if nodelist:
        return nodelist
    return ""


def _parse_brackets(content: str) -> list[str]:
    first_idx = content.index("[")
    last_idx = content.index("]")

    prefix = content[:first_idx]
    bracket_internals = content[first_idx + 1 : last_idx]

    entries = []
    bracket_entries = bracket_internals.split(",")
    for bracket_entry in bracket_entries:
        if "-" in bracket_entry:
            start, end = bracket_entry.split("-")
            for idx in range(int(start), int(end) + 1):
                entries.append(prefix + str(idx))
        else:
            entries.append(prefix + bracket_entry)
    return entries


def _parse_nodelist(nodelist: str) -> list[str]:

    entries = []
    in_brackets = False
    working = ""
    for c in nodelist:
        if c == "[":
            in_brackets = True
            working += c
        elif c == "]":
            in_brackets = False
            working += c
        elif c == "," and not in_brackets:
            entries.append(working)
            working = ""
        else:
            working += c
    if working:
        entries.append(working)

    nodes = []
    for entry in entries:
        if "[" in entry and "]" in entry:
            nodes.extend(_parse_brackets(entry))
        else:
            nodes.append(entry)
    return nodes


def load_job(nodelist: str = "") -> SlurmJob:
    job_id = get_id()
    if not nodelist:
        nodelist = get_nodelist()

    nodes = _parse_nodelist(nodelist)
    return SlurmJob(id=job_id, nodes=nodes)
