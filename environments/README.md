# Reproducible Analysis Environments

The authoritative Maple HPC analysis environments are:

## Python
- Maple module: `python311`
- Python version: 3.11.3
- Virtual environment: `$HOME/.venvs/gqd`
- Direct dependencies: `environments/python/requirements.in`
- Full environment lock: `environments/python/requirements-lock.txt`

## R
- Maple module: `R/4.5.1`
- R version: 4.5.1
- Project dependency manager: `renv`
- Lockfile: `renv.lock`
- Setup notes: `environments/R/README.md`

## Conda portability file

`environments/environment.yml` is retained as an optional Conda-style portability
specification. It is not the authoritative environment used for the Maple HPC
dissertation workflow.

For exact Maple reproducibility, use the Python requirements files and `renv.lock`.
