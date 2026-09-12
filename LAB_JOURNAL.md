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




