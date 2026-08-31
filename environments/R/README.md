# R Analysis Environment

This repository uses R 4.5.1 on the Maple HPC cluster with `renv`
for project-level dependency management and reproducibility.

## Maple startup

Load the R module:

    module load R/4.5.1

Set the user library used to bootstrap renv:

    export R_LIBS_USER="$HOME/R/library/4.5"

The repository-level `.Rprofile` activates the project's renv environment.

## Reproducibility

Restore the recorded R package environment with:

    Rscript -e 'renv::restore()'

Update the lockfile after intentionally adding or changing packages with:

    Rscript -e 'renv::snapshot()'

Do not manually edit `renv.lock`.
