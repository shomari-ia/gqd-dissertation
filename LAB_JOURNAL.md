## Entry template (copy this block for each new entry)

```text
### Entry NNN — YYYY-MM-DD — <short title>
- Scientific/build objective:
- Starting state:
- Commands / actions performed:
- Files changed:
- Job IDs / run IDs:
- Git commit:
- Validation performed:
- Result:
- Problems encountered:
- Root cause:
- Correction:
- Why the correction was justified:
- Decision / advancement gate:
- Archive / checksum status:
- What remains:
- Next action:
``` 


## Entry 001 — 2026-07-20 → 2026-09-08 — FOUNDATION: Reproducibility architecture and accepted PM6 COOH-GQD baseline

*Retrospective foundation entry documenting the computational and
reproducibility work completed before implementation of the formal
session-based Work Journal. Subsequent entries follow the standardized
single-session format.*

- Scientific/build objective:
  Establish a reproducible computational research environment for the GQD
  dissertation and move Phase I from untracked preliminary structure work to
  an accepted, provenance-linked PM6 optimization of the monocarboxylated GQD.

- Starting state:
  Initial structure preparation had been performed outside the final
  reproducibility framework.

  Five PM6 Gaussian inputs had been constructed during early structure
  preparation. Gaussian/GaussView access on the Windows laptop was unavailable,
  so Avogadro and Open Babel were used for local structure preparation.

  Existing PM6 calculations were present on Maple but had not originally been
  executed under the final Git-linked provenance architecture.

  The intended scheduler/environment was initially unclear, and early planning
  incorrectly assumed a Slurm-based workflow.

  B3LYP input preparation had also stalled because optimized Cartesian
  coordinates were being considered for manual transfer from PM6 output.

  At this stage there was no complete system connecting:
      computational input
      → Git commit
      → PBS job
      → Gaussian output
      → QC
      → run log
      → checksum
      → archive
      → scientific journal.

- Commands / actions performed:
  Recovered and reviewed existing PM6 Gaussian calculations.

  Confirmed that five early PM6 calculations had reached:
      Optimization completed
      Normal termination

  Determined that the working HPC environment was Maple using OpenPBS rather
  than Slurm.

  Reworked Gaussian job submission around Maple/OpenPBS and the site's
  node-specific Gaussian execution requirements.

  Established that higher-level Gaussian calculations could read optimized
  PM6 geometries directly from checkpoint files using:
      geom=check

  This eliminated manual copying of large Cartesian coordinate blocks.

  Built the repository-based reproducibility architecture including:
      README.md
      .gitignore
      run_log.tsv
      Gaussian QC scripts
      provenance capture
      checksum/archive scripts
      analysis environment definitions
      bibliography integration.

  Established the GitHub/Maple workflow and the Google Drive write-once
  scientific archive keyed by RUN_ID.

  Established the Python analysis environment and cclib workflow.

  Re-ran the COOH-GQD PM6 calculation under the complete tracked pipeline.

  Accepted:
      PM6-COOH-GQD-005

  as the first fully provenance-linked COOH-GQD baseline calculation.

- Files changed:
  Repository backbone and documentation, including:
      README.md
      .gitignore
      run_log.tsv
      scripts/
      environments/
      docs/references.bib
      Phase I PM6 input/provenance/summary infrastructure
      reproducibility documentation.

  Exact historical changes remain preserved in Git history.

- Job IDs / run IDs:
  ACCEPTED:
      PM6-COOH-GQD-005
      PBS job: 7463337.maple

  SUPERSEDED / PRE-REPRODUCIBILITY:
      earlier PM6 structure-preparation calculations

  EXPLORATORY / NON-PRODUCTION:
      B3LYP pilot job 7420602

  The exploratory B3LYP pilot established workflow feasibility but is not
  treated as a dissertation production result.

- Git commit:
  Key reproducibility commits from the foundation period include:

      2b1d86d — accepted PM6-COOH-GQD-005 provenance state
      59e7c22 — run-log development
      b7adbc0 — archive manifest
      21d5f93 — run003 recovery documentation
      c1c20e0 — Python/R environments
      809a023 — bibliography state

  Git history remains authoritative for exact file-level chronology.

- Validation performed:
  Early PM6 calculations:
      Optimization completed
      Normal termination

  PM6-COOH-GQD-005:
      tracked PBS execution
      Git-linked provenance
      clean/recorded repository state at execution
      Gaussian QC
      final energy capture
      output checksum
      archive linkage
      run-log registration

  Chemical connectivity validation of the optimized COOH-GQD geometry was
  identified as the next scientific QC gate and was intentionally deferred to
  the following journal entry.

- Result:
  PASS — reproducibility foundation established.

  The project transitioned from preliminary computational work into a
  structured, auditable research workflow.

  PM6-COOH-GQD-005 became the accepted pre-optimized geometry for the
  monocarboxylated graphene quantum dot.

  The calculation was accepted computationally, but final chemical connectivity
  validation of the -COOH attachment remained pending before advancement to
  tracked B3LYP production.

- Problems encountered:
  1. Licensed Gaussian/GaussView tools were unavailable on the Windows laptop.
  2. Initial workflow planning assumed Slurm instead of Maple/OpenPBS.
  3. B3LYP geometry preparation was being approached through manual coordinate
     transfer.
  4. Early Gaussian input formatting produced blank-line/input-output naming
     problems.
  5. Early calculations lacked the final compute-node Git provenance system.
  6. One archived run experienced archive truncation and required recovery.
  7. Windows/Linux line-ending differences created reproducibility risk.

- Root cause:
  The project began before the actual HPC environment, scheduler behavior,
  file-transfer policy, repository architecture, and provenance requirements
  had been fully characterized.

  Several issues therefore resulted from infrastructure mismatch rather than
  from the underlying scientific model.

- Correction:
  Windows structure preparation was supported with Avogadro/Open Babel while
  HPC calculations remained on Maple.

  Scheduler scripts were rewritten for OpenPBS.

  Maple's verified Gaussian configuration and node-specific execution behavior
  replaced earlier assumptions.

  `geom=check` was adopted to transfer optimized PM6 geometry through Gaussian
  checkpoint files rather than manually reconstructing coordinates.

  Input-formatting errors were corrected.

  A commit-before-submission provenance rule was adopted.

  Large binary outputs were separated from Git and placed in the write-once
  archive.

  Binary FileZilla transfer was adopted for checkpoint/archive files.

  Git pull-before-work and push-after-work became the synchronization rule for
  text-based project artifacts.

- Why the correction was justified:
  The corrections aligned the workflow with the actual Maple/OpenPBS
  environment while improving scientific provenance.

  None of these corrections were used to conceal unsuccessful work or silently
  alter reported results.

  Failed, exploratory, superseded, and accepted calculations remained
  distinguishable.

  The resulting architecture makes every accepted dissertation result
  traceable through input, scheduler execution, output, QC, checksum,
  archive location, and Git history.

- Archive / checksum status:
  Relevant tracked PM6 outputs were transferred into the established
  write-once archive structure.

  Archive directories use RUN_ID as the joining key between computational
  files and `run_log.tsv`.

  Checksum verification became part of the accepted-run workflow.

  PM6-COOH-GQD-005 was retained as the accepted baseline calculation.

- What remains:
  1. Validate the chemical connectivity of the -COOH group directly from the
     accepted PM6-COOH-GQD-005 optimized Cartesian geometry.
  2. Resolve the Open Babel bonding concern using independent geometric
     analysis.
  3. Confirm whether PM6-COOH-GQD-005 is scientifically cleared for B3LYP.
  4. Finalize the scientific scope document.
  5. Lock the Phase I drug set.
  6. Bring each selected drug through the same tracked structure-preparation
     and QC framework.
  7. Begin B3LYP-D3(BJ)/6-31G(d,p)+SMD optimization/frequency calculations.

- Next action:
  Perform direct connectivity analysis on the final optimized Cartesian
  coordinates from PM6-COOH-GQD-005 using cclib and NumPy.

  If the COOH-to-GQD covalent attachment passes geometric validation,
  document the result in Entry 002 and clear the structure for progression
  to tracked B3LYP optimization/frequency calculations.




### Entry 002 — 2026-09-09 — Validation of COOH-GQD connectivity in accepted PM6 geometry

- Scientific/build objective:
  Verify that the –COOH functional group remains covalently attached to the
  circumcoronene GQD following optimization in the accepted tracked calculation
  PM6-COOH-GQD-005. This validation addresses the concern that a chemically
  plausible molecular formula or visualization alone does not prove correct bonding.

- Starting state:
  PM6-COOH-GQD-005 had previously completed successfully and was accepted under
  full provenance. Open Babel analysis of the optimized Gaussian output produced
  molecular formula C55H18O2 and recognized the structure as one molecular
  component. However, Open Babel also reported an unusual carbon-valence warning,
  so direct geometric verification was required before advancing to B3LYP.

- Commands / actions performed:
  Activated the project Python virtual environment:
      source "$HOME/.venvs/gqd/bin/activate"

  Verified:
      Python 3.11.3
      cclib 1.8.1

  Parsed the final optimized Cartesian coordinates from:
      archive/logs/cooh_gqd_pm6_opt_v01.run005.log

  Used cclib and NumPy to:
      1. count C and O atoms,
      2. identify the carbon lying within 1.8 Å of both oxygen atoms,
      3. measure both carboxyl C–O distances, and
      4. determine the nearest non-carboxyl carbon and its C–C distance.

- Files changed:
  LAB_JOURNAL.md only after documentation of this validation.
  No molecular structures or computational results were modified.

- Job IDs / run IDs:
  PM6-COOH-GQD-005
  PBS job: 7463337.maple

- Git commit:
  Accepted PM6 run provenance commit: 2b1d86d
  Connectivity-validation journal commit: PENDING

- Validation performed:
  Total atoms: 75
  Carbon atoms: 55
  Oxygen atoms: 2
  Gaussian oxygen atom numbers: 73 and 74
  Candidate carboxyl carbon: Gaussian atom 58

  Measured distances:
      C58–O73 = 1.2096 Å
      C58–O74 = 1.3796 Å
      C58–C40 = 1.4618 Å

- Result:
  PASS.

  The optimized structure retains a covalently attached carboxylic acid group.
  The two C–O distances are consistent with the inequivalent carbonyl and
  hydroxyl-side bonds of –COOH, while the 1.4618 Å C58–C40 distance is
  consistent with direct covalent attachment of the carboxyl carbon to the
  conjugated GQD framework.

  Therefore, the optimized PM6 geometry is not represented as a detached
  carboxylic fragment and satisfies the connectivity quality-control gate.

- Problems encountered:
  Open Babel reported:
      "Accepted unusual valence(s): C(3)"
  during automatic bond perception of the conjugated graphene-like structure.

- Root cause:
  The warning was associated with automatic valence/bond perception in the
  extended conjugated structure rather than evidence of physical separation
  of the –COOH group.

- Correction:
  No correction to the molecular geometry was required.
  Connectivity was instead validated directly from the final Gaussian Cartesian
  coordinates using interatomic distances.

- Why the correction was justified:
  Direct Cartesian analysis of the accepted optimized geometry provides stronger
  evidence of covalent attachment than relying solely on file-format bond
  perception or visualization.

- Decision / advancement gate:
  PM6-COOH-GQD-005 is cleared for use as the starting geometry for the
  tracked B3LYP COOH-GQD optimization/frequency calculation.

- Archive / checksum status:
  PM6-COOH-GQD-005 was previously archived under the established reproducibility
  workflow and its provenance/checksum record retained.

- What remains:
  Prepare the accepted PM6 checkpoint as the starting geometry for the tracked
  B3LYP-D3(BJ)/6-31G(d,p)+SMD optimization/frequency calculation.
  Bring the individual drug structures through equivalent tracked structure
  validation before Phase I comparison calculations.

- Next action:
  Resolve the current untracked repository files, commit this validation entry,
  confirm the accepted PM6 checkpoint path, and prepare B3LYP-COOH-GQD-001.

