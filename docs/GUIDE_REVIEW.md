# Review of the Draft Reproducibility Guide

The draft (`Dissertation_HPC_Reproducibility_Guide_OpenPBS_Maple`) is sound on
principles and over-built for the project's actual state. This file records what
was kept, what was cut, and what was corrected — so the difference is a
documented decision rather than an inconsistency someone notices later.

## Corrections — things that were wrong or would break

**1. Checkpoint filename collisions.** The Windows prep document uses
`%chk=cooh_gqd.chk` for the PM6 job and the *same* name for the B3LYP job. Since
the DFT stage reads its geometry from the PM6 checkpoint, running both with one
filename overwrites the PM6 record and destroys the hand-off. Fixed by giving
every stage its own checkpoint under `archive/chk/`, with `%oldchk` naming the
source explicitly.

**2. `guess=read` across a method or basis change.** The computational guide
carries `geom=check guess=read` from the B3LYP checkpoint into an
M06-2X/6-311+G(d,p) single point. The basis set changes, so the stored
wavefunction is not a valid guess. The same problem, worse, applies to reading a
PM6 wavefunction into a DFT job. `geom=check` alone is correct for every stage
transition here; `guess=read` is valid only for a same-level restart.

**3. Stale template content.** The draft's `config/systems.yml` example lists
doxorubicin, a LANL2DZ platinum basis, and `DOCK-EGFR-DOX` run IDs — none of
which belong to this project. Its DFT block also specifies 6-31G(d), while
Chapter 2 specifies 6-31G(d,p). Replaced with the real five systems and the
Chapter 2 level of theory.

**4. No `.gitattributes`.** The draft documents the CRLF problem in the reports
but never fixes it. `* text=auto eol=lf` is the fix, and it has to be committed
before any script is.

## Cuts — right idea, wrong time

| Cut | Reason |
|---|---|
| `docking/`, `molecular_dynamics/`, `free_energy/` trees | Phase III is months out. Git does not track empty directories; they would exist only as `.gitkeep` clutter and would date badly once the actual analysis shape is known. |
| Feature branches | One person, one line of work. Branch-and-merge adds ceremony without isolating anything. Tags at phase boundaries give the milestone marking that was actually wanted. |
| `CHANGELOG.md` | Duplicates `git log` and the run log, and drifts the moment you forget to update it. |
| `tests/` | Nothing to unit-test. The real test is the QC gate, which now lives in `scripts/verify_gaussian.sh` and runs automatically. |
| Three separate config files | `analysis_parameters.yml` has nothing in it yet. One `systems.yml` until it genuinely outgrows itself. |
| MD/docking/free-energy QC sections | Correct content, wrong chapter. They move into `computational_workflow.md` when Phase III starts. |

## The central change: the run log is generated, not typed

The draft's 24-column `run_log.tsv` is the part most likely to fail in practice.
Half of its columns (`nodes`, `cpus`, `memory`, `walltime`, `job_script`) restate
what the PBS script already says, and the PBS script is already version
controlled and already referenced by `git_commit`. Restating a fact is how two
records start disagreeing. Hand-typing 24 tab-separated fields per job, across
roughly sixty Phase I jobs, in Notepad++, is a data-entry task that will quietly
degrade after about week three.

The system here splits the log by who knows the fact:

- **The job knows** its ID, node, start and end time, commit, and checksums — so
  the job writes them itself, into a `.prov` file.
- **The log knows** whether it terminated normally, whether the optimization
  completed, how many imaginary frequencies there are, and the final energies —
  so the QC script extracts them, into a `.summary.txt`.
- **You know** why you ran it and what you decided — so you write that, and only
  that, in `run_notes.tsv`.

`scripts/build_run_log.sh` assembles all three into `run_log.tsv` on demand.
Because it is regenerated rather than edited, the file cannot drift from the
underlying evidence, and because your notes live in a separate file joined on
`run_id`, regenerating never overwrites anything you wrote.

This directly serves the requirement that data and text will be constantly
edited, added, and removed: the parts you edit are small and separate, and the
parts you must not corrupt are never edited at all.

## Kept, essentially as written

- Preserving failed and superseded runs with a stated reason
- The `system_method_task_version` naming pattern
- Checksums on every archived scientific file
- Scientific commit messages, and committing at meaningful checkpoints
- Provenance capture inside the job script
- Recording random seeds (moves to Phase III, where stochastic methods appear)
- The central traceability rule, which is restated in the README

## The one addition the draft did not cover

Storage assignment. The draft treats GitHub as the system and mentions
"archival storage" in passing, but a working setup needs an explicit rule for
where each artifact lives and how the pieces rejoin. That is
`docs/storage_map.md`, with `run_id` as the join key across GitHub, Google
Drive, and the cluster, and Zotero exporting into the repository so the
bibliography is versioned with the methods that cite it.
