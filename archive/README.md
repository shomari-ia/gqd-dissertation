# archive/ — large files, not in Git

Nothing in here is version-controlled. It is the staging area for files that
are too large or too binary for GitHub but are still part of the scientific
record:

    archive/chk/    Gaussian checkpoints  (the geometry hand-off between stages)
    archive/logs/   full Gaussian output logs
    archive/wfx/    wavefunction files for Multiwfn / NCIPLOT

Every file here is traceable: its SHA-256, size, file type, and associated
`run_id` are recorded in `archive_manifest.tsv`. Gaussian output-log hashes
also appear in `run_log.tsv`, the provenance record, and the committed
`*.summary.txt` record.

Mirror this directory to Google Drive (`02_archive/`) after each batch of jobs
— see `docs/storage_map.md`.

Checkpoints are **not** disposable in this project. B3LYP jobs read their
geometry from the PM6 checkpoint via `geom=check`, so deleting a `.chk` breaks
the provenance chain between stages.
