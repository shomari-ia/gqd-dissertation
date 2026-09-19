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


### Entry 001 — 2026-07-20 → 2026-09-08 — FOUNDATION: Reproducibility Architecture & PM6 COOH-GQD Baseline

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




### Entry 003 — 2026-09-10 — B3LYP-COOH-GQD-001 preflight and production submission

- Scientific/build objective:
  Validate the accepted PM6 checkpoint as the starting geometry for the first
  tracked production B3LYP calculation, audit the B3LYP input and reproducibility
  chain, correct any provenance-related problems, and submit
  B3LYP-COOH-GQD-001 to Maple.

- Starting state:
  PM6-COOH-GQD-005 had been accepted under full provenance.

  Direct Cartesian analysis had verified the optimized COOH-GQD structure:

      molecular composition: C55H18O2
      total atoms: 75
      charge: 0
      multiplicity: 1

      C58-O73 = 1.2096 Å
      C58-O74 = 1.3796 Å
      C58-C40 = 1.4618 Å

  The -COOH group therefore passed the direct covalent-connectivity gate.

  The existing B3LYP input used the correct scientific method but still
  referenced the older generic PM6 checkpoint rather than the accepted
  run005 checkpoint.

- Commands / actions performed:
  Located all available PM6 checkpoints and identified:

      archive/chk/cooh_gqd_pm6_opt_v01.run005.chk

  as the checkpoint associated with accepted run:

      PM6-COOH-GQD-005

  Verified checkpoint size:

      12 MB

  Recorded checkpoint SHA256:

      79d756a8ab5ec8968dd7ed022171fda4f194f565a38c518f368e398d1c716677

  `formchk` was not available in the Maple login-shell PATH, so a small
  OpenPBS compute-node validation job was submitted using the same
  node-specific Gaussian environment logic as the production workflow.

  Checkpoint-validation PBS job:

      7633381.maple

  The validation job ran on:

      cn119
      Gaussian build: g16-c01-avx2

  Gaussian successfully read the checkpoint as a G16 checkpoint and produced
  a temporary formatted checkpoint containing:

      Number of atoms: 75
      Charge: 0
      Multiplicity: 1

  Validation result:

      CHECKPOINT_READABILITY=PASS

  Inspected the existing B3LYP input:

      calculations/phase1_dft/b3lyp/inputs/
      cooh_gqd_b3lyp_optfreq_v01.com

  Confirmed:

      %mem=32GB
      %nprocshared=16
      B3LYP/6-31G(d,p)
      EmpiricalDispersion=GD3BJ
      SCRF=(SMD,Solvent=Water)
      opt
      freq
      geom=check
      charge 0
      multiplicity 1
      no guess=read

  Corrected the checkpoint source from:

      %oldchk=archive/chk/cooh_gqd_pm6_opt_v01.chk

  to:

      %oldchk=archive/chk/cooh_gqd_pm6_opt_v01.run005.chk

  Committed the corrected input before submission.

  A remote Git update caused the initial push to be rejected. The local
  commit was safely rebased onto origin/main using:

      git pull --rebase origin main

  and then successfully pushed.

  Final production Git commit:

      795588f

  Verified no pre-existing B3LYP working log or checkpoint existed, preventing
  accidental output collision.

  Recorded B3LYP input SHA256:

      6b29c78bcce591d59cebdf99336dc2452bb99de4c9d94ff99a00c8f9a8ffd57d

  Submitted:

      RUN_ID=B3LYP-COOH-GQD-001

  with:

      1 Maple node
      16 CPU
      32 GB memory
      48-hour walltime

  PBS job:

      7633495.maple

- Files changed:
  calculations/phase1_dft/b3lyp/inputs/
  cooh_gqd_b3lyp_optfreq_v01.com

  The only scientific-input change was the `%oldchk` reference to the
  accepted PM6-COOH-GQD-005 checkpoint.

- Job IDs / run IDs:
  Checkpoint validation:
      PBS job 7633381.maple

  Production:
      RUN_ID B3LYP-COOH-GQD-001
      PBS job 7633495.maple

- Git commit:
  795588f

- Validation performed:
  Production provenance file:

      calculations/phase1_dft/b3lyp/prov/
      B3LYP-COOH-GQD-001.prov

  recorded:

      run_id=B3LYP-COOH-GQD-001
      job_id=7633495.maple
      execution_host=cn045
      gaussian_build=g16-c01-avx2
      git_commit=795588f
      git_dirty=no
      input_sha256=
      6b29c78bcce591d59cebdf99336dc2452bb99de4c9d94ff99a00c8f9a8ffd57d

  The running Gaussian log independently confirmed:

      NAtoms=75
      Charge=0
      Multiplicity=1

  Route:

      #p opt freq B3LYP/6-31G(d,p)
      EmpiricalDispersion=GD3BJ
      SCRF=(SMD,Solvent=Water)
      geom=check

  The first reported B3LYP SCF point converged:

      E(RB3LYP) = -2256.96666058 A.U.
      after 15 cycles

- Result:
  PASS for preflight and production submission.

  B3LYP-COOH-GQD-001 successfully entered production on Maple with the
  correct accepted PM6 geometry, scientific method, computational resources,
  Git provenance, and input checksum.

  The calculation is currently active.

  The reported first SCF energy is an intermediate optimization value and is
  not treated as the final B3LYP energy.

- Problems encountered:
  1. `formchk` was unavailable from the interactive Maple login-shell PATH.
  2. The pre-existing B3LYP input referenced the generic PM6 checkpoint rather
     than the accepted run005 checkpoint.
  3. The first Git push of the corrected B3LYP input was rejected because
     origin/main contained newer work.
  4. Reproducibility inspection identified that archive-manifest RUN_ID parsing
     is currently PM6-specific.
  5. QC summary naming currently derives from the output-log basename rather
     than directly from the explicit production RUN_ID.

- Root cause:
  Gaussian utilities are configured within Maple's compute-node-specific
  environment rather than the login shell.

  The B3LYP input predated final acceptance of PM6-COOH-GQD-005.

  The Git remote had advanced independently before the B3LYP input push.

  Some reproducibility scripts were initially designed around the first PM6
  workflow and have not yet been generalized across all computational stages.

- Correction:
  Used an OpenPBS compute-node validation job to test the checkpoint within
  Maple's verified Gaussian environment.

  Updated `%oldchk` to the accepted run005 checkpoint.

  Rebased the local Git commit onto the current remote main branch and pushed
  successfully.

  Confirmed that the existing QC/run-log fallback remains functional for the
  current B3LYP calculation.

  Deferred generalization of the archive/QC naming architecture to a separate
  infrastructure task rather than modifying production behavior during the
  scientific run.

- Why the correction was justified:
  Each correction preserved the existing validated computational architecture
  while ensuring that B3LYP-COOH-GQD-001 is traceable to the exact accepted
  PM6 geometry and exact Git-controlled input.

  No scientific method was changed during the correction.

- Decision / advancement gate:
  PASS for submission.

  All pre-submission scientific and reproducibility checks were satisfied.
  B3LYP-COOH-GQD-001 was submitted as PBS job 7633495.maple from Git commit
  795588f with a clean repository state.

  Final scientific acceptance remains pending:

      optimization completion,
      frequency calculation,
      zero imaginary frequencies,
      normal Gaussian termination,
      QC PASS,
      final energy extraction,
      Gibbs free-energy extraction,
      checksum verification,
      run-log registration,
      and archive preservation.

- Archive / checksum status:
  Input SHA256 recorded:

      6b29c78bcce591d59cebdf99336dc2452bb99de4c9d94ff99a00c8f9a8ffd57d

  PM6 source checkpoint SHA256 recorded:

      79d756a8ab5ec8968dd7ed022171fda4f194f565a38c518f368e398d1c716677

  Production B3LYP output checksum will be recorded only after completion.

- What remains:
  1. Monitor B3LYP-COOH-GQD-001 without interfering with execution.
  2. Confirm geometry optimization completion.
  3. Confirm frequency calculation completion.
  4. Verify zero imaginary frequencies.
  5. Confirm Normal termination.
  6. Run the Gaussian QC gate.
  7. Record final SCF and Gibbs free energies.
  8. Update run_log.tsv through the automated workflow.
  9. Preserve the accepted B3LYP log/checkpoint in the archive.
  10. Generalize archive-manifest and explicit RUN_ID summary handling as a
      separate reproducibility infrastructure task.

- Next action:
  Begin Entry 004 when B3LYP-COOH-GQD-001 completes or when a scientifically
  meaningful event requiring intervention occurs.




### Entry 004 — 2026-09-11 — B3LYP-COOH-GQD-001 completion, frequency QC, and scientific acceptance

- Scientific/build objective:
  Evaluate the completed B3LYP-COOH-GQD-001 production calculation, verify
  geometry optimization and frequency results, confirm provenance integrity,
  extract final thermochemical quantities, and determine whether the optimized
  COOH-GQD structure passes the advancement gate.

- Starting state:
  B3LYP-COOH-GQD-001 had been submitted from the accepted
  PM6-COOH-GQD-005 geometry as PBS job 7633495.maple.

  Production input:
      calculations/phase1_dft/b3lyp/inputs/
      cooh_gqd_b3lyp_optfreq_v01.com

  Production Git commit:
      795588f

  Input SHA256:
      6b29c78bcce591d59cebdf99336dc2452bb99de4c9d94ff99a00c8f9a8ffd57d

- Commands / actions performed:
  Confirmed that PBS job 7633495.maple had exited the queue.

  Inspected final SCF energies and Gaussian termination.

  Checked geometry-optimization completion.

  Inspected harmonic frequencies and explicitly counted negative frequencies.

  Ran the formal Gaussian QC gate:

      scripts/verify_gaussian.sh \
      archive/logs/cooh_gqd_b3lyp_optfreq_v01.log \
      calculations/phase1_dft/b3lyp/summaries

  Rebuilt the machine-generated run ledger:

      scripts/build_run_log.sh --write

- Job IDs / run IDs:
      RUN_ID: B3LYP-COOH-GQD-001
      PBS job: 7633495.maple
      execution host: cn045

- Validation performed:
  Gaussian termination:
      NORMAL

  Geometry optimization:
      COMPLETED

  Harmonic-frequency analysis:
      imaginary frequencies = 0

  System:
      atoms = 75
      charge = 0
      multiplicity = 1

  QC status:
      PASS

  Gaussian exit:
      0

  QC exit:
      0

- Result:
  Final electronic SCF energy:

      E(RB3LYP) = -2257.22593711 Hartree

  Zero-point correction:

      0.541834 Hartree

  Gibbs free energy:

      -2256.741041 Hartree

  CPU time:

      1 day 12 hours 7 minutes 41.1 seconds

  Wall-clock elapsed time:

      2 hours 16 minutes 6.5 seconds

  Output SHA256:

      bcc0062f2341239b8cc12a2f92ef14f714c558ca4acf3b2e7d73c92b5d1c8467

- Interpretation:
  The B3LYP-D3(BJ)/6-31G(d,p), SMD-water optimization completed normally.
  Harmonic-frequency analysis found zero imaginary frequencies.

  Therefore, the optimized COOH-GQD geometry corresponds to a local minimum
  on the calculated potential-energy surface at the stated level of theory.

  The final SCF energy and Gibbs free energy supersede intermediate
  optimization energies and are the accepted values for this run.

  Two "Optimization completed." records appeared in the Gaussian log.
  Inspection of both locations showed all four convergence criteria satisfied
  and "Stationary point found." in each case. This did not indicate failure.
  Final acceptance was based on normal termination, successful QC, and zero
  imaginary frequencies.

- Decision / advancement gate:
  PASS.

  B3LYP-COOH-GQD-001 is accepted as the optimized
  B3LYP-D3(BJ)/6-31G(d,p), SMD-water COOH-GQD baseline structure.

  The calculation satisfied all required scientific acceptance criteria:

      normal Gaussian termination,
      completed geometry optimization,
      all optimization convergence criteria satisfied,
      stationary point confirmed,
      zero imaginary frequencies,
      Gaussian exit code = 0,
      QC exit code = 0,
      and reproducible provenance linked to the production Git commit.

  Accepted final values for this run are:

      Electronic SCF energy:
      -2257.22593711 Hartree

      Zero-point correction:
      0.541834 Hartree

      Gibbs free energy:
      -2256.741041 Hartree

      Output SHA256:
      bcc0062f2341239b8cc12a2f92ef14f714c558ca4acf3b2e7d73c92b5d1c8467

  The optimized structure therefore passes the B3LYP geometry and
  frequency-validation gate and may serve as the accepted DFT baseline
  geometry for subsequent Phase I calculations.

  Advancement beyond this point is permitted only after the accepted
  B3LYP log, checkpoint, completed provenance, QC summary, and run-log
  record are preserved under the reproducibility/archive workflow.

  Scientific status:
      ACCEPTED — B3LYP-COOH-GQD-001

  Reproducibility/archive status:
      ACCEPTANCE RECORD COMPLETE;
      PERMANENT RUN-SPECIFIC ARCHIVE PRESERVATION PENDING.

### Entry 005 — 2026-09-11 — B3LYP-COOH-GQD-001 archive and reproducibility closure

- Scientific/build objective:
  Preserve the accepted B3LYP-COOH-GQD-001 Gaussian artifacts as immutable,
  run-specific records; verify their integrity; and update the archive and
  naming infrastructure so the accepted B3LYP calculation remains traceable
  independently of mutable working files.

- Starting state:
  B3LYP-COOH-GQD-001 had passed geometry optimization, frequency analysis,
  formal QC, and scientific acceptance.

  Accepted production working artifacts:

      archive/logs/cooh_gqd_b3lyp_optfreq_v01.log
      archive/chk/cooh_gqd_b3lyp_optfreq_v01.chk

  Accepted run:

      B3LYP-COOH-GQD-001

  Acceptance Git commit:

      0591f8a

- Commands / actions performed:
  Recorded SHA256 fingerprints of the accepted B3LYP working artifacts.

  Created immutable run-specific preservation copies using `cp -p`:

      archive/logs/cooh_gqd_b3lyp_optfreq_v01.run001.log
      archive/chk/cooh_gqd_b3lyp_optfreq_v01.run001.chk

  Verified the preservation copies against their source artifacts using
  SHA256 checksums.

  Updated `scripts/build_archive_manifest.sh` so:

      PM6 run-specific files map to PM6-COOH-GQD-###,
      B3LYP run-specific files map to B3LYP-COOH-GQD-###,
      and only immutable `.runNNN.*` scientific artifacts are inventoried.

  Mutable generic `.log` and `.chk` working/handoff files are therefore no
  longer treated as permanent archive records.

  Updated `docs/naming_conventions.md` so `B3LYP` is the canonical run-stage
  label for primary B3LYP-D3(BJ)/6-31G(d,p) optimization/frequency
  calculations.

  Regenerated:

      archive_manifest.tsv

  Performed Bash syntax validation:

      bash -n scripts/build_archive_manifest.sh

  Performed Git whitespace validation:

      git diff --check

  Performed full archive checksum verification:

      scripts/build_archive_manifest.sh --verify

- Files changed:
      archive_manifest.tsv
      docs/naming_conventions.md
      scripts/build_archive_manifest.sh
      LAB_JOURNAL.md

  Large Gaussian log/checkpoint preservation copies remain under `archive/`
  and are excluded from Git according to the established storage architecture.

- Job IDs / run IDs:
      RUN_ID: B3LYP-COOH-GQD-001
      PBS job: 7633495.maple
      execution host: cn045

- Validation performed:
  Source B3LYP log SHA256:

      bcc0062f2341239b8cc12a2f92ef14f714c558ca4acf3b2e7d73c92b5d1c8467

  Preserved run001 log SHA256:

      bcc0062f2341239b8cc12a2f92ef14f714c558ca4acf3b2e7d73c92b5d1c8467

  Source B3LYP checkpoint SHA256:

      b8d45cb64aaf8bb49d5140bf44167253859dfb65ed1dc740437b0fc79071ba88

  Preserved run001 checkpoint SHA256:

      b8d45cb64aaf8bb49d5140bf44167253859dfb65ed1dc740437b0fc79071ba88

  Source and preservation-copy hashes matched exactly.

  Archive manifest contains eight immutable run-specific scientific files:

      6 PM6 artifacts
      2 B3LYP artifacts

  B3LYP manifest records correctly map to:

      B3LYP-COOH-GQD-001

  Bash syntax validation:

      PASS

  Git whitespace validation:

      PASS

  Archive verification:

      PASS

- Result:
  The accepted B3LYP Gaussian log and checkpoint were preserved without
  alteration as immutable run-specific artifacts associated with
  B3LYP-COOH-GQD-001.

  The mutable generic working artifacts remain available for computational
  handoff while `.run001.*` artifacts preserve the accepted scientific result.

  The archive manifest now distinguishes permanent run-specific records from
  mutable working files.

- Problems encountered:
  The original archive-manifest logic assigned every `.runNNN` artifact to
  the PM6-COOH-GQD run family.

  The initial generalized manifest also inventoried mutable generic B3LYP
  working files, which appeared as UNASSIGNED.

  The naming-conventions document used `DFT` as the primary stage label even
  though the accepted production workflow used `B3LYP`.

  A Python cleanup command using `pathlib` failed because Maple's default
  `python` environment did not provide the `pathlib` module.

- Root cause:
  The original archive infrastructure was developed around the first PM6
  workflow before B3LYP production runs entered the pipeline.

  Generic Gaussian working artifacts and immutable run-specific artifacts had
  not yet been formally separated in the archive-manifest logic.

  The naming documentation predated adoption of the explicit B3LYP RUN_ID
  convention.

- Correction:
  Added explicit PM6 and B3LYP run-family mappings.

  Restricted permanent archive inventory to:

      *.runNNN.*

  Updated naming documentation so `B3LYP` is the canonical primary
  optimization/frequency stage label.

  Used a Perl-based text cleanup compatible with the Maple environment when
  the attempted Python `pathlib` method was unavailable.

- Why the correction was justified:
  Permanent archive records must have stable checksums and explicit RUN_ID
  associations.

  Mutable working and checkpoint handoff files may legitimately change during
  later calculations and therefore should not be treated as immutable
  archived records.

  The naming standard must match the RUN_ID convention actually used by
  accepted production calculations.

- Decision / advancement gate:
  PASS.

  B3LYP-COOH-GQD-001 has completed scientific acceptance and local
  reproducibility/archive closure.

  Its accepted Gaussian log and checkpoint now exist as immutable,
  checksum-verified run-specific artifacts.

  The local archive manifest correctly associates both artifacts with
  B3LYP-COOH-GQD-001 and passes full integrity verification.

  The workflow is cleared to advance beyond the COOH-GQD baseline and begin
  the next defined Phase I scientific calculation.

- Archive / checksum status:
  Permanent log:

      archive/logs/cooh_gqd_b3lyp_optfreq_v01.run001.log

  SHA256:

      bcc0062f2341239b8cc12a2f92ef14f714c558ca4acf3b2e7d73c92b5d1c8467

  Permanent checkpoint:

      archive/chk/cooh_gqd_b3lyp_optfreq_v01.run001.chk

  SHA256:

      b8d45cb64aaf8bb49d5140bf44167253859dfb65ed1dc740437b0fc79071ba88

  Local archive-manifest verification:

      PASS

- What remains:
  1. Commit Entry 005 together with the archive manifest, manifest-script
     correction, and naming-convention update.
  2. Synchronize the immutable B3LYP run artifacts with the Google Drive
     write-once archive if that transfer has not yet been completed.
  3. Generalize archive RUN_ID mapping further as additional systems and
     computational stages enter production.
  4. Determine the next Phase I production calculation.

- Next action:
  Commit and push the archive-closure documentation and infrastructure changes,
  then begin planning the next Phase I calculation from the accepted B3LYP
  COOH-GQD baseline.




### Entry 006 — 2026-09-13 — Phase I drug-set scope lock and Erlotinib structure-preparation preflight

- Scientific/build objective:
  Formally lock the Phase I anticancer drug set before tracked drug
  calculations begin and establish Erlotinib as the first drug system to enter
  structure preparation and PM6 pre-optimization.

- Starting state:
  The COOH-GQD baseline workflow had completed PM6 optimization, B3LYP
  optimization/frequency validation, scientific acceptance, provenance
  capture, and immutable archive closure.

  The computational workflow already specified the intended drug sequence:

      Erlotinib
      Gefitinib
      Venetoclax
      ABT-737

  However, `docs/scientific_scope.md` still listed:

      DRUG SET STATUS: PENDING FINAL SCOPE LOCK

  No tracked drug PM6 calculations had been launched.

  The structure directories contained no drug structures:

      structures/raw/.gitkeep
      structures/prepared/.gitkeep

- Commands / actions performed:
  Inspected all Phase I calculation directories and files.

  Confirmed that no existing Erlotinib, Gefitinib, Venetoclax, or ABT-737
  calculation files, Gaussian inputs, logs, checkpoints, provenance records,
  QC summaries, or archived drug runs existed.

  Inspected:

      config/systems.yml
      docs/computational_workflow.md
      docs/scientific_scope.md
      structures/raw/
      structures/prepared/

  Confirmed the configured Phase I drug set:

      Erlotinib — EGFR
      Gefitinib — EGFR
      Venetoclax (ABT-199) — Bcl-2
      ABT-737 — Bcl-2

  Confirmed the intended computational order:

      Erlotinib
      Gefitinib
      Venetoclax
      ABT-737

  Updated `docs/scientific_scope.md` so:

      DRUG SET STATUS: LOCKED

  Added explicit language requiring a documented scientific rationale and
  Git-tracked scope amendment for any later drug substitution, removal, or
  addition.

- Files changed:
      docs/scientific_scope.md
      LAB_JOURNAL.md

- Job IDs / run IDs:
  No Gaussian job was submitted during this entry.

  No drug RUN_ID was assigned yet.

- Validation performed:
  Confirmed the drug set matches `config/systems.yml`.

  Confirmed the locked set matches the sequence defined in
  `docs/computational_workflow.md`.

  Confirmed no drug structure files currently exist in:

      structures/raw/
      structures/prepared/

  Confirmed no pre-existing drug Gaussian input or output files are present
  in the Phase I calculation directories.

- Result:
  The Phase I drug set is now formally locked as:

      Erlotinib
      Gefitinib
      Venetoclax (ABT-199)
      ABT-737

  Erlotinib is confirmed as the first drug system to enter the tracked
  structure-preparation and computational workflow.

- Problems encountered:
  The drug systems were fully documented in configuration and workflow files,
  but the scientific-scope document remained in a provisional state.

  No drug source or prepared structures had yet been added to the repository.

- Root cause:
  The COOH-GQD baseline workflow was completed before activation of the drug
  branch of Phase I.

- Correction:
  Formally locked the existing four-drug Phase I set in
  `docs/scientific_scope.md`.

  Established Erlotinib as the first drug to enter structure acquisition,
  preparation, and PM6 pre-optimization.

- Why the correction was justified:
  The scope document explicitly required formal drug-set confirmation before
  tracked drug PM6 calculations were launched.

  Locking the drug set prevents silent scientific-scope drift after
  calculations begin and preserves traceability between the dissertation plan,
  repository configuration, and actual production jobs.

- Decision / advancement gate:
  PASS.

  The Phase I drug set is formally locked.

  Erlotinib is cleared to advance to source-structure acquisition and
  structure preparation.

  No PM6 production job should be submitted until the Erlotinib source
  structure, provenance, connectivity, charge, multiplicity, and prepared
  geometry have been validated.

- Archive / checksum status:
  Not applicable for a new drug calculation yet.

- What remains:
  1. Acquire the Erlotinib source structure from PubChem CID 176870.
  2. Preserve the original source structure under `structures/raw/`.
  3. Prepare and validate the structure under `structures/prepared/`.
  4. Confirm formula, atom count, charge, multiplicity, and connectivity.
  5. Build the Erlotinib PM6 Gaussian input.
  6. Assign the first Erlotinib PM6 RUN_ID.
  7. Commit all pre-submission provenance before launching Gaussian.

- Next action:
  Acquire and validate the Erlotinib source structure before creating its PM6
  production input.




### Entry 007 — 2026-09-17 — Erlotinib raw-source acquisition and validation

- Scientific/build objective:
  Acquire the canonical Erlotinib source structure, preserve it as an immutable
  provenance root, and validate molecular identity, composition, connectivity,
  charge consistency, and source-file integrity before structure preparation.

- Starting state:
  The Phase I drug set had been formally locked.

  Erlotinib was designated as the first drug system to enter the tracked
  Phase I structure-preparation and computational workflow.

  No Erlotinib source or prepared structures previously existed in the
  repository.

- Commands / actions performed:
  Downloaded the PubChem 3D SDF record for:

      Erlotinib
      PubChem CID 176870

  Source file:

      structures/raw/erlotinib_pubchem_cid176870_3d.sdf

  Recorded the SHA256 fingerprint.

  Inspected the SDF atom and bond blocks.

  Verified elemental composition directly from the atom block.

  Inspected charge-related records.

  Confirmed SDF termination and coordinate metadata.

  Performed an independent graph-connectivity check using Python.

  Counted bond orders and explicitly identified the triple bond.

  Checked for Open Babel on Maple; neither `obabel` nor `babel` was available
  in the login environment.

- Files changed:
      structures/raw/erlotinib_pubchem_cid176870_3d.sdf
      LAB_JOURNAL.md

- Job IDs / run IDs:
  No Gaussian job was submitted.

  No computational RUN_ID was assigned.

- Validation performed:
  PubChem CID:

      176870

  Formula from SDF atom block:

      C22H23N3O4

  Element counts:

      C = 22
      H = 23
      N = 3
      O = 4

  Total atoms:

      52

  Total bonds:

      54

  Bond-order distribution:

      single bonds = 45
      double bonds = 8
      triple bonds = 1

  Triple bond:

      atoms 28-29

  Graph-connectivity validation:

      connected atoms = 52
      connected components = 1
      isolated atoms = none

  Formal-charge validation:
      no `M  CHG` formal-charge record was observed.

  PubChem MMFF94 partial-charge data were present, but these represent
  atom-level partial charges rather than a nonzero formal molecular charge.

  SDF terminator:

      $$$$

  Raw source SHA256:

      9e776f75f2a17693890715f5df6e0569ae73b0c8ed3fa150d099f8f0a047e1dc

- Result:
  The raw PubChem Erlotinib structure is internally consistent with the
  intended neutral Erlotinib system.

  The molecular graph contains all 52 atoms in one connected component,
  contains no isolated atoms, and contains the expected single triple bond
  associated with the ethynyl functionality.

  The raw source file is accepted as the provenance root for the Erlotinib
  computational branch.

- Problems encountered:
  The initial PubChem download attempt was executed from the home directory
  rather than the repository root, so `structures/raw/` was not found.

  Open Babel was not available in the Maple login environment.

- Root cause:
  The first download command was run before changing into
  `~/gqd-dissertation`.

  Open Babel is not installed or exposed in the current Maple login PATH.

- Correction:
  Re-ran the PubChem download from the repository root.

  Used direct SDF inspection and a Python graph-connectivity check instead of
  Open Babel for raw-source validation.

- Why the correction was justified:
  Raw-source validation requires confirmation of identity, composition, and
  molecular connectivity, not a specific software package.

  The independent graph check verified one connected molecular component with
  the expected atom and bond counts, which was sufficient for the current
  source-validation gate.

- Decision / advancement gate:
  PASS.

  The Erlotinib raw-source structure is accepted as the immutable provenance
  root for the Erlotinib Phase I workflow.

  Erlotinib may advance to prepared-structure generation.

  No PM6 production job should be submitted until the prepared structure is
  generated, validated, and committed.

- Archive / checksum status:
  Raw source:

      structures/raw/erlotinib_pubchem_cid176870_3d.sdf

  SHA256:

      9e776f75f2a17693890715f5df6e0569ae73b0c8ed3fa150d099f8f0a047e1dc

  Git source commit:

      8027ea9

- What remains:
  1. Generate the prepared Erlotinib structure.
  2. Preserve the raw PubChem file unchanged.
  3. Validate the prepared structure against the raw source.
  4. Confirm formula, atom count, charge, multiplicity, and connectivity.
  5. Build the Erlotinib PM6 Gaussian input.
  6. Assign the first Erlotinib PM6 RUN_ID.
  7. Commit all pre-submission files before launching Gaussian.

- Next action:
  Create and validate the prepared Erlotinib structure under
  `structures/prepared/`.




### Entry 008 — 2026-09-18 — Erlotinib MMFF94 preparation and validation

- Scientific/build objective:
  Generate and validate the prepared Erlotinib geometry that will serve as the
  starting structure for tracked PM6 pre-optimization.

- Starting state:
  The validated raw Erlotinib PubChem structure had been preserved at:

      structures/raw/erlotinib_pubchem_cid176870_3d.sdf

  Raw-source Git commit:

      8027ea9

  Raw-source SHA256:

      9e776f75f2a17693890715f5df6e0569ae73b0c8ed3fa150d099f8f0a047e1dc

  The raw structure had passed identity, composition, connectivity, and
  source-integrity validation.

- Commands / actions performed:
  Loaded the Maple Open Babel module:

      module load obabel/3.1.1

  Verified the executable:

      /usr/local/apps/obabel-3.1.1/bin/obabel

  The executable reported:

      Open Babel 3.1.0 -- Jul 22 2021

  Verified that MMFF94 was available as a supported force field.

  Generated the prepared Erlotinib structure with MMFF94 minimization:

      obabel \
        structures/raw/erlotinib_pubchem_cid176870_3d.sdf \
        -O structures/prepared/erlotinib_mmff94_prep_v01.mol \
        --minimize \
        --ff MMFF94 \
        --steps 500

  Compared raw and prepared molecular identity using SMILES.

  Compared atom count, bond count, elemental composition, atom ordering,
  bond topology, coordinate displacement, and graph connectivity.

- Files changed:
      structures/prepared/erlotinib_mmff94_prep_v01.mol
      LAB_JOURNAL.md

- Job IDs / run IDs:
  No Gaussian job was submitted.

  No production RUN_ID was assigned during this entry.

- Validation performed:
  Prepared structure:

      structures/prepared/erlotinib_mmff94_prep_v01.mol

  Prepared SHA256:

      7342e15fce9c13a399dd6fa4b2bf14694011c708986a0a9bcdfc89886f34e701

  Prepared atom count:

      52

  Prepared bond count:

      54

  Element counts:

      C = 22
      H = 23
      N = 3
      O = 4

  Raw and prepared SMILES were identical:

      O(c1c(OCCOC)cc2ncnc(Nc3cc(ccc3)C#C)c2c1)CCOC

  Raw and prepared atom ordering:

      IDENTICAL

  Raw and prepared bond topology:

      IDENTICAL

  Same-index coordinate RMSD:

      0.039226 Å

  Prepared graph connectivity:

      connected atoms = 52
      connected components = 1
      isolated atoms = none

- Result:
  MMFF94 preparation changed the Erlotinib coordinates slightly without
  altering molecular identity, composition, atom ordering, or bond topology.

  The prepared structure remains one connected neutral Erlotinib molecule and
  is accepted as the starting geometry for PM6 pre-optimization.

- Problems encountered:
  Open Babel was initially thought to be unavailable because it was not present
  in the default Maple PATH.

- Root cause:
  Open Babel is provided through the Maple module system rather than the
  default login environment.

- Correction:
  Loaded:

      obabel/3.1.1

  The loaded executable reported Open Babel 3.1.0.

- Why the correction was justified:
  The canonical workflow specifies MMFF94 cleanup before PM6.

  Using the Maple Open Babel module keeps structure preparation reproducible
  while preserving the raw PubChem structure unchanged.

- Decision / advancement gate:
  PASS.

  The prepared Erlotinib geometry is accepted for PM6 input construction.

  The raw PubChem structure remains the immutable provenance root.

  PM6 input generation may proceed after the prepared structure and journal
  record are committed to Git.

- Archive / checksum status:
  Prepared structure:

      structures/prepared/erlotinib_mmff94_prep_v01.mol

  SHA256:

      7342e15fce9c13a399dd6fa4b2bf14694011c708986a0a9bcdfc89886f34e701

- What remains:
  1. Commit the prepared Erlotinib structure and Entry 008.
  2. Inspect the existing COOH-GQD PM6 input as the canonical template.
  3. Generate the Erlotinib PM6 Gaussian input.
  4. Assign RUN_ID PM6-ERLOTINIB-001.
  5. Validate charge, multiplicity, coordinates, atom count, and checkpoint path.
  6. Commit all pre-submission files before Gaussian submission.

- Next action:
  Commit the validated prepared Erlotinib structure and inspect the existing
  PM6 input template before constructing PM6-ERLOTINIB-001.




### Entry 009 — 2026-09-18 — PM6-ERLOTINIB-001 preflight and production-input lock

- Scientific/build objective:
  Construct and validate the first tracked Erlotinib PM6 production input,
  confirm that the proposed RUN_ID and output paths are unused, and lock the
  Gaussian input in Git before PBS submission.

- Starting state:
  The Erlotinib raw PubChem structure had passed identity and connectivity
  validation.

  The MMFF94-prepared Erlotinib structure had been accepted at:

      structures/prepared/erlotinib_mmff94_prep_v01.mol

  Prepared structure SHA256:

      7342e15fce9c13a399dd6fa4b2bf14694011c708986a0a9bcdfc89886f34e701

  Prepared-structure Git commit:

      af99947

  No tracked Erlotinib Gaussian calculation had yet been submitted.

- Commands / actions performed:
  Generated the Gaussian PM6 input directly from the validated prepared
  Erlotinib coordinates.

  Production input:

      calculations/phase1_dft/pm6/inputs/erlotinib_pm6_opt_v01.com

  Input header:

      %chk=archive/chk/erlotinib_pm6_opt_v01.chk
      %mem=8GB
      %nprocshared=8
      #p PM6 opt SCF=XQC

  Gaussian title:

      erlotinib PM6 pre-optimization | system=erlotinib charge=0 mult=1 | v01

  Charge and multiplicity:

      0 1

  Counted Gaussian coordinate records and elemental composition.

  Compared Gaussian coordinates directly against the prepared `.mol`
  structure.

  Checked for pre-existing Erlotinib RUN_ID records, checkpoints, logs,
  provenance files, and QC summaries.

- Files changed:
      calculations/phase1_dft/pm6/inputs/erlotinib_pm6_opt_v01.com
      LAB_JOURNAL.md

- Job IDs / run IDs:
  Proposed RUN_ID:

      PM6-ERLOTINIB-001

  No PBS job submitted yet.

- Validation performed:
  Input atom count:

      52

  Element counts:

      C = 22
      H = 23
      N = 3
      O = 4

  Charge:

      0

  Multiplicity:

      1

  Prepared-structure atom count:

      52

  Gaussian-input atom count:

      52

  Element ordering:

      IDENTICAL

  Maximum coordinate difference between prepared structure and Gaussian input:

      0.0 Å

  Therefore, the Gaussian coordinate block is an exact transfer of the
  accepted prepared Erlotinib geometry.

  Proposed checkpoint:

      archive/chk/erlotinib_pm6_opt_v01.chk

  Proposed output:

      archive/logs/erlotinib_pm6_opt_v01.log

  Existing PM6-ERLOTINIB RUN_ID records:

      NONE

  Existing Erlotinib PM6 checkpoint:

      NONE

  Existing Erlotinib PM6 log:

      NONE

  Existing PM6-ERLOTINIB-001 provenance:

      NONE

  Existing Erlotinib PM6 QC summary:

      NONE

  Input SHA256:

      004dda6b08e68e6cb97aa9b1e068b73ace5fe8ac76f19fcc0d008b8dfba5572b

- Result:
  The first Erlotinib PM6 Gaussian input was generated successfully from the
  accepted MMFF94-prepared structure.

  Molecular composition, atom ordering, coordinates, charge, multiplicity,
  checkpoint path, and output naming were validated.

  No existing Erlotinib PM6 artifacts or RUN_ID records conflict with the
  proposed production run.

- Problems encountered:
  None during PM6 input construction or collision checking.

- Root cause:
  Not applicable.

- Correction:
  Not applicable.

- Why the correction was justified:
  Not applicable.

- Decision / advancement gate:
  PASS.

  The Erlotinib PM6 production input is accepted for pre-submission Git
  locking.

  RUN_ID:

      PM6-ERLOTINIB-001

  may be used for the first tracked Erlotinib PM6 calculation.

  PBS submission must occur only after the input and this journal record are
  committed to Git so the production job can reference a fixed provenance
  commit.

- Archive / checksum status:
  Production input:

      calculations/phase1_dft/pm6/inputs/erlotinib_pm6_opt_v01.com

  Input SHA256:

      004dda6b08e68e6cb97aa9b1e068b73ace5fe8ac76f19fcc0d008b8dfba5572b

  No production log or checkpoint exists yet.

- What remains:
  1. Commit the Erlotinib PM6 production input and Entry 009.
  2. Record the resulting Git commit.
  3. Submit PM6-ERLOTINIB-001 through OpenPBS.
  4. Confirm job ID, execution host, provenance capture, and initial Gaussian
     parsing.
  5. Run the QC gate after job completion.
  6. Preserve accepted log/checkpoint as run-specific archive artifacts if the
     calculation passes.

- Next action:
  Commit the PM6 Erlotinib input and Entry 009, then submit
  PM6-ERLOTINIB-001.




### Entry 010 — 2026-09-18 — PM6-ERLOTINIB-001 completion, QC, and scientific acceptance

- Scientific/build objective:
  Evaluate the completed PM6-ERLOTINIB-001 production calculation, verify
  optimization success and provenance integrity, record the accepted PM6
  geometry handoff, and determine whether Erlotinib may advance to the B3LYP
  optimization/frequency stage.

- Starting state:
  PM6-ERLOTINIB-001 had been submitted from the validated MMFF94-prepared
  Erlotinib geometry.

  Production input:

      calculations/phase1_dft/pm6/inputs/erlotinib_pm6_opt_v01.com

  Production Git commit:

      f677160

  Input SHA256:

      004dda6b08e68e6cb97aa9b1e068b73ace5fe8ac76f19fcc0d008b8dfba5572b

- Commands / actions performed:
  Submitted the tracked PM6 Erlotinib calculation through OpenPBS.

  Confirmed production provenance capture.

  Inspected the completed Gaussian output.

  Verified Gaussian termination, geometry-optimization completion, and
  stationary-point detection.

  Inspected the formal QC summary.

  Recorded the final PM6 SCF value.

  Verified the production checkpoint and calculated its SHA256 checksum.

  Rebuilt the machine-generated run ledger using:

      scripts/build_run_log.sh --write

- Job IDs / run IDs:
      RUN_ID: PM6-ERLOTINIB-001
      PBS job: 7709167.maple
      execution host: cn037

- Validation performed:
  Gaussian build:

      g16-c01-avx2

  Gaussian termination:

      NORMAL

  Geometry optimization:

      COMPLETED

  Stationary point:

      FOUND

  System:

      atoms = 52
      charge = 0
      multiplicity = 1

  Gaussian exit:

      0

  QC exit:

      0

  QC status:

      PASS

  Production Git provenance:

      git_commit = f677160
      git_dirty = no

- Result:
  Final PM6 SCF value:

      E(RPM6) = -0.367805799799E-01 Hartree

  Gaussian CPU time:

      0 days 0 hours 7 minutes 38.2 seconds

  Gaussian elapsed time:

      0 days 0 hours 1 minute 27.6 seconds

  Output SHA256:

      9a8cf2d2cb6b8c30fd8844a3339d8b39e11d40d4d4cd8298195c49e84af7fcf4

  Checkpoint SHA256:

      90d7869c00373ddae1b9921139d68f149410ed472a11d5671cace8ac3d3b309a

- Interpretation:
  The Erlotinib PM6 pre-optimization completed normally and reached a
  stationary optimized geometry.

  The PM6 calculation serves as a geometry-preparation step for subsequent
  B3LYP-D3(BJ)/6-31G(d,p), SMD-water optimization and frequency analysis.

  The PM6 energy is retained for reproducibility and bookkeeping only. It is
  not comparable to the later DFT energies and will not enter binding-energy
  calculations.

- Problems encountered:
  During early monitoring, an incomplete `qstat -f` command was cancelled
  manually after Bash waited for continuation input.

  This did not affect the PBS job, which had already been submitted
  successfully and completed normally.

- Root cause:
  The shell continuation character was entered before the intended filtering
  command was completed.

- Correction:
  Cancelled only the unfinished interactive shell command with Ctrl+C.

  The active PBS job was not cancelled or altered.

- Why the correction was justified:
  The incomplete command existed only in the login shell and had no effect on
  PBS job 7709167.maple.

- Decision / advancement gate:
  PASS.

  PM6-ERLOTINIB-001 is accepted as the PM6-preoptimized Erlotinib geometry.

  The calculation satisfied the required PM6 advancement criteria:

      normal Gaussian termination,
      completed geometry optimization,
      stationary point found,
      Gaussian exit code = 0,
      QC exit code = 0,
      formal QC status = PASS,
      and complete Git-linked production provenance.

  Scientific status:

      ACCEPTED — PM6-ERLOTINIB-001

  Erlotinib is cleared to advance to the B3LYP-D3(BJ)/6-31G(d,p),
  SMD-water optimization/frequency stage after permanent run-specific PM6
  archive preservation is completed.

- Archive / checksum status:
  Working production log:

      archive/logs/erlotinib_pm6_opt_v01.log

  Output SHA256:

      9a8cf2d2cb6b8c30fd8844a3339d8b39e11d40d4d4cd8298195c49e84af7fcf4

  Working production checkpoint:

      archive/chk/erlotinib_pm6_opt_v01.chk

  Checkpoint SHA256:

      90d7869c00373ddae1b9921139d68f149410ed472a11d5671cace8ac3d3b309a

  PERMANENT RUN-SPECIFIC ARCHIVE PRESERVATION PENDING.

- What remains:
  1. Commit the completed provenance, QC summary, run-log record, and this
     scientific-acceptance entry.
  2. Preserve the accepted PM6 log and checkpoint as immutable run001
     artifacts.
  3. Extend archive-manifest RUN_ID mapping to PM6-ERLOTINIB.
  4. Verify the updated archive manifest.
  5. Construct the Erlotinib B3LYP optimization/frequency input from the
     accepted PM6 checkpoint.

- Next action:
  Commit the PM6 Erlotinib scientific-acceptance record before performing
  permanent archive closure.








