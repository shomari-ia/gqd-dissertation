# Storage Map v2.0

**Controlled date:** 2026-10-29

The project uses separate systems for version-controlled reproducibility, HPC execution, large scientific artifacts, committee deliverables, and dissertation writing. The `run_id` is the primary scientific join key.

| Location | Holds | Control rule |
|---|---|---|
| **GitHub repository** | inputs, scripts, configuration, provenance, QC summaries, ledgers/registers, canonical scope/workflow/gates, text results, reproducible final figures | Versioned by Git. No large Gaussian binaries. |
| **MCSR / HPC archive** | active execution files and full Gaussian scientific artifacts produced on Maple/Magnolia | Preserve run-specific identity; do not overwrite historical runs. |
| **Google Drive — CDSE/GQD Dissertation/04_RUN_ARCHIVE/<RUN_ID>/** | full .log, .chk, .fchk, .wfx, cube files, final geometry exports and associated run package | One controlled run folder per RUN_ID; write-once scientific archive behavior. |
| **Google Drive — 01_SCIENTIFIC_EVIDENCE/** | SEP evidence packages | Evidence is organized by scientific claim/milestone, not by file type. |
| **Google Drive — 00_CURRENT_STATUS/** | current scientific status, evidence register, current committee package | Must reflect only the current accepted scientific state. |
| **Google Drive — 07_DISSERTATION_CHAPTERS/** | current manuscript chapters / review copies | Numbers enter prose only after scientific acceptance and traceability. |
| **Google Drive — 10_RESEARCH_JOURNAL_PUBLICATION_EDITION/** | curated print/defense journal and assets | Derived from canonical records; never replaces LAB_JOURNAL.md. |
| **Zotero → docs/references.bib** | bibliography | Citation control through Zotero / Better BibTeX and Git. |

## Run archive unit

Recommended Drive structure:

```
04_RUN_ARCHIVE/
└── <RUN_ID>/
    ├── input/
    ├── log/
    ├── checkpoint/
    ├── geometry/
    ├── provenance/
    ├── QC/
    └── MANIFEST.txt
```

The run folder is the human-reviewable package for the full calculation.

## Traceability chain

`reported result → Scientific Evidence Register → run_log.tsv → provenance/QC → archive_manifest.tsv → full run artifact`

Given any reported number, the project should be able to identify:
- scientific claim;
- run ID;
- input file;
- Git commit;
- scheduler/job ID;
- node;
- Gaussian build;
- full output-log checksum;
- checkpoint/archive location;
- scientific disposition.

## Integrity

`archive_manifest.tsv` records the SHA-256, size, file type and run ID for archived scientific files.

Run:

`scripts/build_archive_manifest.sh --verify`

to verify the scientific archive represented in the project manifest.

## Non-archived scratch

Gaussian scratch such as `.rwf`, `.int`, `.d2e` and temporary `Gau-*` files are not part of the permanent scientific archive unless a specific recovery event requires preservation.
