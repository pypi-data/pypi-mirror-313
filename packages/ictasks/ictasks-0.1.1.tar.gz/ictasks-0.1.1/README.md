# `ictasks`

This is a set of utilities to support running groups of small tasks as part of a single HPC batch submission at ICHEC.

The repo includes:

1) the `ictasks` package with tooling building blocks
2) Snapshots of the ICHEC [Taskfarm](https://www.ichec.ie/academic/national-hpc/documentation/tutorials/task-farming) tool available on our HPC systems in the `applications` directory.

# Installing #

The package can be installed from PyPI:

``` shell
pip install ictasks
```

# Features #

## Taskfarm ##

The `taskfarm` feature will launch the tasks in the pointed to `tasklist` file:

``` shell
ictasks taskfarm --tasklist $PATH_TO_TASKLIST
```

See the `test/data/tasklist.dat` file for an example input with two small tasks.

If you run this on your local machine it will create a directory per task, launch the task in that directory and output a status file `task.json`. By default all processors on the machine (or compute node) will be assigned tasks. There are two ways to control this, and many other, settings:

1. With environment variables using a `TASKFARM_` prefix, consistent with the original ICHEC `taskfarm` tool and documented here: https://www.ichec.ie/academic/national-hpc/documentation/tutorials/task-farming

2. With a config file in `yaml` format - passed in with a `--config` command line argument. Config values take precedence over environment variables if both are specified for the same setting.

### Using a config file ###

The config file below shows an example constraining tasks to run on only a single core per compute node. We can also specify tasks in the config instead of in a tasklist file.


``` yaml
environment:
	job_id: my_job
	workers:
		cores_per_node: 1

tasks:
	items:
	  - id: 0
	    launch_cmd: "echo 'hello from task 0'"
	  - id: 1
	    launch_cmd: "echo 'hello from task 1'"
```

we can run this with:

``` shell
ictasks taskfarm --config my_config.yaml
```

# License #

This package is Coypright of the Irish Centre for High End Computing. It can be used under the terms of the GNU Public License (GPL). See the included `LICENSE.txt` file for details.





