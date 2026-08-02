# Storage Map

Four locations. Each holds exactly one kind of thing. When you are unsure where
something goes, the answer is in this table.

| Location | Holds | Versioned by | Rule |
|---|---|---|---|
| **GitHub repo** | inputs (`.com`), scripts, `config/`, `docs/`, `run_log.tsv`, `*.prov`, `*.summary.txt`, results tables and figures | Git commits + tags | Nothing larger than ~5 MB. Nothing binary except final figures. |
| **`archive/` → Google Drive `02_archive/`** | full `.log`, `.chk`, `.fchk`, `.wfx`, cube files | `run_id` folder names | Write once. Never edit in place. A correction is a new `run_id`. |
| **Google Docs (Drive `01_manuscript/`)** | chapter prose while drafting | Docs revision history | Numbers enter prose only after they exist in `run_log.tsv`. |
| **Zotero → `docs/references.bib`** | bibliography | Better BibTeX auto-export, then Git | Pinned citation keys only. |

## The join key

`run_id` appears in five places and ties the whole record together:

    run_log.tsv row  →  calculations/**/prov/<run_id>.prov
                     →  calculations/**/summaries/<stem>.summary.txt
                     →  Drive 02_archive/phase1_dft/<run_id>/
                     →  the results table cell that reports the number

Given any number in Chapter 2, you can walk backwards to the input file, the
job script, the commit, the node it ran on, and the checksum of the output it
came from. That traceability is the entire point of the system.

## What is *not* stored anywhere

Gaussian scratch (`.rwf`, `.int`, `.d2e`, `Gau-*`) and PBS stdout files. They
are regenerable and enormous. `.gitignore` already excludes them; delete them
from the cluster after a successful QC gate.

## Integrity

Every archived file's SHA-256, size, file type, and associated `run_id` are
recorded in `archive_manifest.tsv`. Gaussian output-log hashes are also
recorded in `run_log.tsv` and the corresponding provenance records.

Run:

    scripts/build_archive_manifest.sh --verify

to re-hash every archived file and compare it with the committed manifest. A
size or checksum mismatch indicates that a file changed or was corrupted during
storage or transfer.
