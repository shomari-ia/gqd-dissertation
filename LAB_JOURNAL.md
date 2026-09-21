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




### Entry 011 — 2026-09-18 — PM6-ERLOTINIB-001 immutable archive closure

- Scientific/build objective:
  Preserve the accepted PM6-ERLOTINIB-001 production artifacts as immutable,
  run-specific archive copies and extend the archive manifest so the new
  Erlotinib artifacts resolve to their canonical RUN_ID.

- Starting state:
  PM6-ERLOTINIB-001 had passed scientific acceptance and was committed in:

      ca591f7

  Accepted working log:

      archive/logs/erlotinib_pm6_opt_v01.log

  Accepted working checkpoint:

      archive/chk/erlotinib_pm6_opt_v01.chk

  Output SHA256:

      9a8cf2d2cb6b8c30fd8844a3339d8b39e11d40d4d4cd8298195c49e84af7fcf4

  Checkpoint SHA256:

      90d7869c00373ddae1b9921139d68f149410ed472a11d5671cace8ac3d3b309a

- Commands / actions performed:
  Created immutable run-specific archive copies:

      archive/logs/erlotinib_pm6_opt_v01.run001.log
      archive/chk/erlotinib_pm6_opt_v01.run001.chk

  Verified that each immutable copy was byte-identical to its accepted
  working artifact using SHA256.

  Extended:

      scripts/build_archive_manifest.sh

  with Erlotinib PM6 RUN_ID mapping:

      erlotinib_pm6_* -> PM6-ERLOTINIB-${run_number}

  Rebuilt the archive manifest.

  Verified all immutable archive artifacts.

- Files changed:
      scripts/build_archive_manifest.sh
      archive_manifest.tsv
      LAB_JOURNAL.md

- Job IDs / run IDs:
      RUN_ID: PM6-ERLOTINIB-001
      PBS job: 7709167.maple

- Validation performed:
  Working log SHA256:

      9a8cf2d2cb6b8c30fd8844a3339d8b39e11d40d4d4cd8298195c49e84af7fcf4

  Immutable log SHA256:

      9a8cf2d2cb6b8c30fd8844a3339d8b39e11d40d4d4cd8298195c49e84af7fcf4

  Working checkpoint SHA256:

      90d7869c00373ddae1b9921139d68f149410ed472a11d5671cace8ac3d3b309a

  Immutable checkpoint SHA256:

      90d7869c00373ddae1b9921139d68f149410ed472a11d5671cace8ac3d3b309a

  Archive verification:

      PASSED

  Total immutable archive files verified:

      10

- Result:
  The PM6-ERLOTINIB-001 log and checkpoint have been preserved as immutable,
  run-specific archive artifacts.

  The archive manifest now resolves the Erlotinib PM6 run-specific artifacts
  to:

      PM6-ERLOTINIB-001

  without changing the existing COOH-GQD PM6 or B3LYP mappings.

- Problems encountered:
  An inspection command initially referenced:

      archive/manifest.tsv

  but the manifest builder writes:

      archive_manifest.tsv

  at the repository root.

- Root cause:
  The inspection command used an incorrect manifest path.

- Correction:
  Used the actual manifest filename:

      archive_manifest.tsv

- Why the correction was justified:
  The manifest builder itself completed successfully and explicitly reported:

      wrote archive_manifest.tsv (10 files)

  Archive verification also passed for all 10 files.

- Decision / advancement gate:
  PASS.

  PM6-ERLOTINIB-001 archive closure is complete.

  The accepted PM6 geometry and its provenance are permanently preserved.

  Erlotinib is cleared to advance to the B3LYP-D3(BJ)/6-31G(d,p),
  SMD-water optimization/frequency stage.

- Archive / checksum status:
  IMMUTABLE ARCHIVE CLOSED.

  Log:

      archive/logs/erlotinib_pm6_opt_v01.run001.log

  Checkpoint:

      archive/chk/erlotinib_pm6_opt_v01.run001.chk

  Archive manifest:

      archive_manifest.tsv

  Archive verification status:

      PASS

- What remains:
  1. Commit the archive-manifest update and Entry 011.
  2. Construct the Erlotinib B3LYP optimization/frequency input from the
     accepted PM6 checkpoint.
  3. Perform B3LYP preflight and lock the production input in Git before
     submission.

- Next action:
  Commit the PM6 Erlotinib archive closure, then begin construction of the
  Erlotinib B3LYP optimization/frequency production input.





### Entry 012 — 2026-09-19 — B3LYP-ERLOTINIB-001 preflight and production-input lock

- Scientific/build objective:
  Construct and validate the Erlotinib B3LYP-D3(BJ)/6-31G(d,p),
  SMD-water optimization/frequency production input using the accepted
  immutable PM6 checkpoint as the starting geometry.

- Starting state:
  PM6-ERLOTINIB-001 had passed scientific acceptance and immutable archive
  closure.

  Accepted PM6 checkpoint:

      archive/chk/erlotinib_pm6_opt_v01.run001.chk

  PM6 checkpoint SHA256:

      90d7869c00373ddae1b9921139d68f149410ed472a11d5671cace8ac3d3b309a

  PM6 archive closure commit:

      396df99

- Commands / actions performed:
  Checked for existing B3LYP Erlotinib RUN_ID records, output logs,
  checkpoints, provenance files, and summaries.

  No collisions were found.

  Constructed:

      calculations/phase1_dft/b3lyp/inputs/erlotinib_b3lyp_optfreq_v01.com

  using the accepted COOH-GQD B3LYP production input as the canonical syntax
  template.

- Files changed:
      calculations/phase1_dft/b3lyp/inputs/erlotinib_b3lyp_optfreq_v01.com
      LAB_JOURNAL.md

- Job IDs / run IDs:
  Proposed RUN_ID:

      B3LYP-ERLOTINIB-001

  No PBS job submitted yet.

- Validation performed:
  Source checkpoint:

      archive/chk/erlotinib_pm6_opt_v01.run001.chk

  Source checkpoint SHA256:

      90d7869c00373ddae1b9921139d68f149410ed472a11d5671cace8ac3d3b309a

  New checkpoint:

      archive/chk/erlotinib_b3lyp_optfreq_v01.chk

  Route:

      #p opt freq B3LYP/6-31G(d,p) EmpiricalDispersion=GD3BJ SCRF=(SMD,Solvent=Water) geom=check

  Memory:

      32GB

  Shared processors:

      16

  Charge:

      0

  Multiplicity:

      1

  Geometry source:

      accepted PM6 checkpoint via geom=check

  Input SHA256:

      10ad2235c7c2ab1a16007aca9fa63f6bdab137660db00b6301b8508e6cbe8fd6

  Existing B3LYP-ERLOTINIB RUN_ID records:

      NONE

  Existing Erlotinib B3LYP checkpoint:

      NONE

  Existing Erlotinib B3LYP log:

      NONE

- Result:
  The Erlotinib B3LYP optimization/frequency production input was constructed
  successfully from the immutable accepted PM6 checkpoint.

  The calculation follows the same validated B3LYP-D3(BJ)/6-31G(d,p),
  SMD-water protocol used for the accepted COOH-GQD baseline.

- Problems encountered:
  None.

- Root cause:
  Not applicable.

- Correction:
  Not applicable.

- Why the correction was justified:
  Not applicable.

- Decision / advancement gate:
  PASS.

  B3LYP-ERLOTINIB-001 is approved for pre-submission Git locking.

  PBS submission must occur only after this input and journal record are
  committed so the production job can reference a fixed Git commit.

- Archive / checksum status:
  Source PM6 checkpoint is already preserved as an immutable run001 artifact.

  B3LYP production input SHA256:

      10ad2235c7c2ab1a16007aca9fa63f6bdab137660db00b6301b8508e6cbe8fd6

  No B3LYP production log or checkpoint exists yet.

- What remains:
  1. Commit the B3LYP Erlotinib production input and Entry 012.
  2. Record the resulting Git commit.
  3. Submit B3LYP-ERLOTINIB-001.
  4. Capture PBS job ID, node, Gaussian build, and production provenance.
  5. Evaluate optimization completion and frequency results after execution.

- Next action:
  Lock the B3LYP Erlotinib production input in Git before submission.


### Entry 013 — 2026-09-19 — B3LYP-ERLOTINIB-001 completion, frequency QC, and scientific acceptance

- Scientific/build objective:
  Evaluate the completed Erlotinib B3LYP-D3(BJ)/6-31G(d,p), SMD-water
  optimization/frequency calculation, verify that the optimized structure is
  a true minimum, confirm production provenance, and determine whether the
  B3LYP Erlotinib baseline may be scientifically accepted.

- Starting state:
  B3LYP-ERLOTINIB-001 had been submitted from the immutable accepted PM6
  checkpoint:

      archive/chk/erlotinib_pm6_opt_v01.run001.chk

  Production input:

      calculations/phase1_dft/b3lyp/inputs/erlotinib_b3lyp_optfreq_v01.com

  Production Git commit:

      1c91891

  Input SHA256:

      10ad2235c7c2ab1a16007aca9fa63f6bdab137660db00b6301b8508e6cbe8fd6

- Commands / actions performed:
  Inspected the completed Gaussian log and automated QC summary.

  Verified normal Gaussian termination.

  Verified completed geometry optimization and stationary-point detection.

  Counted all vibrational frequencies.

  Confirmed the expected 3N-6 vibrational mode count for a nonlinear
  52-atom system.

  Checked for imaginary frequencies.

  Extracted the final SCF energy, zero-point correction, Gibbs correction,
  and thermochemical energies.

  Verified the production checkpoint and calculated its SHA256 checksum.

  Rebuilt the machine run ledger using:

      scripts/build_run_log.sh --write

- Files changed:
      run_log.tsv
      LAB_JOURNAL.md

  Production provenance and QC files generated:

      calculations/phase1_dft/b3lyp/prov/B3LYP-ERLOTINIB-001.prov
      calculations/phase1_dft/b3lyp/summaries/erlotinib_b3lyp_optfreq_v01.summary.txt

- Job IDs / run IDs:
      RUN_ID: B3LYP-ERLOTINIB-001
      PBS job: 7709220.maple
      execution host: cn046

- Validation performed:
  Gaussian build:

      g16-c01-avx2

  Gaussian termination:

      NORMAL

  Geometry optimization:

      COMPLETED

  Stationary point:

      FOUND

  Gaussian exit:

      0

  QC exit:

      0

  QC status:

      PASS

  System:

      atoms = 52
      charge = 0
      multiplicity = 1

  Expected vibrational modes:

      3N - 6 = 150

  Observed vibrational modes:

      150

  Imaginary frequencies:

      0

  Lowest vibrational frequency:

      14.3361 cm^-1

  Production Git provenance:

      git_commit = 1c91891
      git_dirty = no

- Result:
  Final B3LYP electronic energy:

      E(RB3LYP) = -1317.40085224 Hartree

  Zero-point correction:

      0.420518 Hartree

  Thermal correction to Gibbs Free Energy:

      0.359949 Hartree

  Sum of electronic and zero-point energies:

      -1316.980334 Hartree

  Sum of electronic and thermal free energies:

      -1317.040903 Hartree

  Gaussian CPU time:

      0 days 4 hours 49 minutes 2.5 seconds

  Gaussian elapsed time:

      0 days 0 hours 18 minutes 11.8 seconds

  Output SHA256:

      042787f2a35a5ff283eafb0d8fab152d3fcb02d8c123780b26f8358f4a7698a4

  Checkpoint SHA256:

      7b5414ef0a5ada369029e566a838758c1f7faaf68587bb53c2ab9fc4a610faf1

- Interpretation:
  B3LYP-ERLOTINIB-001 converged to a stationary structure with no imaginary
  vibrational frequencies.

  The exact expected number of vibrational modes was recovered:

      150 of 150

  with a lowest positive mode of:

      14.3361 cm^-1

  The absence of negative frequencies supports classification of the optimized
  structure as a local minimum on the B3LYP-D3(BJ)/6-31G(d,p), SMD-water
  potential-energy surface.

  The lowest mode is soft but positive. It does not invalidate the optimized
  minimum, although low-frequency vibrational modes should be treated with
  appropriate caution when interpreting harmonic thermochemical quantities.

- Problems encountered:
  None during production execution or scientific QC.

- Root cause:
  Not applicable.

- Correction:
  Not applicable.

- Why the correction was justified:
  Not applicable.

- Decision / advancement gate:
  PASS.

  B3LYP-ERLOTINIB-001 is scientifically accepted.

  Acceptance criteria satisfied:

      normal Gaussian termination,
      completed optimization,
      stationary point found,
      150 expected vibrational modes observed,
      zero imaginary frequencies,
      Gaussian exit code = 0,
      QC exit code = 0,
      QC status = PASS,
      and complete Git-linked production provenance.

  Scientific status:

      ACCEPTED — B3LYP-ERLOTINIB-001

  Erlotinib may advance to permanent run-specific archive closure.

- Archive / checksum status:
  Working production log:

      archive/logs/erlotinib_b3lyp_optfreq_v01.log

  Output SHA256:

      042787f2a35a5ff283eafb0d8fab152d3fcb02d8c123780b26f8358f4a7698a4

  Working production checkpoint:

      archive/chk/erlotinib_b3lyp_optfreq_v01.chk

  Checkpoint SHA256:

      7b5414ef0a5ada369029e566a838758c1f7faaf68587bb53c2ab9fc4a610faf1

  PERMANENT RUN-SPECIFIC ARCHIVE PRESERVATION PENDING.

- What remains:
  1. Commit the completed provenance, QC summary, run-log record, and Entry 013.
  2. Preserve the accepted B3LYP log and checkpoint as immutable run001
     artifacts.
  3. Extend archive-manifest mapping for B3LYP-ERLOTINIB.
  4. Verify archive integrity.
  5. Continue to the next Phase I Erlotinib workflow stage after archive
     closure.

- Next action:
  Commit the B3LYP Erlotinib scientific-acceptance package before immutable
  archive closure.




### Entry 014 — 2026-09-19 — B3LYP-ERLOTINIB-001 immutable archive closure

- Scientific/build objective:
  Preserve the accepted B3LYP-ERLOTINIB-001 production artifacts as immutable,
  run-specific archive copies and extend archive-manifest mapping so the new
  Erlotinib B3LYP artifacts resolve to their canonical RUN_ID.

- Starting state:
  B3LYP-ERLOTINIB-001 had passed scientific acceptance and was committed in:

      bde18ac

  Accepted working log:

      archive/logs/erlotinib_b3lyp_optfreq_v01.log

  Accepted working checkpoint:

      archive/chk/erlotinib_b3lyp_optfreq_v01.chk

  Output SHA256:

      042787f2a35a5ff283eafb0d8fab152d3fcb02d8c123780b26f8358f4a7698a4

  Checkpoint SHA256:

      7b5414ef0a5ada369029e566a838758c1f7faaf68587bb53c2ab9fc4a610faf1

- Commands / actions performed:
  Created immutable run-specific archive copies:

      archive/logs/erlotinib_b3lyp_optfreq_v01.run001.log
      archive/chk/erlotinib_b3lyp_optfreq_v01.run001.chk

  Verified that each immutable copy was byte-identical to its accepted
  working artifact using SHA256.

  Extended:

      scripts/build_archive_manifest.sh

  with Erlotinib B3LYP RUN_ID mapping:

      erlotinib_b3lyp_* -> B3LYP-ERLOTINIB-${run_number}

  Rebuilt the archive manifest.

  Verified all immutable archive artifacts.

- Files changed:
      scripts/build_archive_manifest.sh
      archive_manifest.tsv
      LAB_JOURNAL.md

- Job IDs / run IDs:
      RUN_ID: B3LYP-ERLOTINIB-001
      PBS job: 7709220.maple

- Validation performed:
  Working log SHA256:

      042787f2a35a5ff283eafb0d8fab152d3fcb02d8c123780b26f8358f4a7698a4

  Immutable log SHA256:

      042787f2a35a5ff283eafb0d8fab152d3fcb02d8c123780b26f8358f4a7698a4

  Working checkpoint SHA256:

      7b5414ef0a5ada369029e566a838758c1f7faaf68587bb53c2ab9fc4a610faf1

  Immutable checkpoint SHA256:

      7b5414ef0a5ada369029e566a838758c1f7faaf68587bb53c2ab9fc4a610faf1

  Archive verification:

      PASSED

  Total immutable archive files verified:

      12

  Manifest entries for both Erlotinib B3LYP run001 artifacts resolve to:

      B3LYP-ERLOTINIB-001

- Result:
  The B3LYP-ERLOTINIB-001 log and checkpoint have been preserved as immutable,
  run-specific archive artifacts.

  The archive manifest correctly records both files under the canonical
  B3LYP Erlotinib RUN_ID.

  Existing COOH-GQD and Erlotinib PM6 mappings remain intact.

- Problems encountered:
  None during this archive-closure stage.

- Root cause:
  Not applicable.

- Correction:
  Not applicable.

- Why the correction was justified:
  Not applicable.

- Decision / advancement gate:
  PASS.

  B3LYP-ERLOTINIB-001 archive closure is complete.

  The isolated-molecule Erlotinib PM6 -> B3LYP baseline is now scientifically
  accepted, reproducibly documented, and permanently archived.

- Archive / checksum status:
  IMMUTABLE ARCHIVE CLOSED.

  Log:

      archive/logs/erlotinib_b3lyp_optfreq_v01.run001.log

  Checkpoint:

      archive/chk/erlotinib_b3lyp_optfreq_v01.run001.chk

  Archive manifest:

      archive_manifest.tsv

  Archive verification status:

      PASS

- What remains:
  1. Commit the B3LYP Erlotinib archive closure.
  2. Determine the next Phase I Erlotinib stage according to the canonical
     computational workflow.
  3. Preserve the accepted B3LYP structure as the reference isolated-drug
     state for subsequent interaction calculations.

- Next action:
  Commit the B3LYP Erlotinib archive closure and inspect the canonical workflow
  before beginning the next Erlotinib calculation stage.



### Entry 015 — 2026-09-21 — Gefitinib raw PubChem source acquisition and validation

- Scientific/build objective:
  Acquire the canonical PubChem 3D structure for Gefitinib and validate its
  identity, elemental composition, connectivity, charge state, and suitability
  for reproducible molecular preparation.

- Starting state:
  Gefitinib is the second drug in the locked Phase I calculation order.

  Canonical system definition:

      PubChem CID: 123631
      target context: EGFR
      charge: 0
      multiplicity: 1

  No Gefitinib structure or calculation files existed in the repository before
  this acquisition step.

- Commands / actions performed:
  Downloaded the PubChem 3D SDF for CID 123631.

  Validated the structure using Open Babel and direct SDF parsing.

  Checked:
      molecular formula,
      atom count,
      bond count,
      elemental composition,
      molecular connectivity,
      isolated atoms,
      explicit SDF charge records,
      PubChem conformer metadata,
      and canonical molecular representation.

- Files changed:
      structures/raw/gefitinib_pubchem_cid123631_3d.sdf
      LAB_JOURNAL.md

- Job IDs / run IDs:
  No Gaussian RUN_ID assigned at this stage.

- Git commit:
  Pending.

- Validation performed:
  Raw source:

      PubChem CID 123631

  Molecular formula:

      C22H24ClFN4O3

  Atom count:

      55

  Bond count:

      58

  Element counts:

      C  = 22
      H  = 24
      Cl = 1
      F  = 1
      N  = 4
      O  = 3

  Connected components:

      1

  Component size:

      55 atoms

  Isolated atoms:

      none

  Explicit M CHG records:

      none

  Open Babel SMILES:

      Clc1cc(Nc2ncnc3c2cc(OCCCN2CCOCC2)c(OC)c3)ccc1F

  PubChem MMFF94 conformer energy:

      107.6811

  Raw SDF SHA256:

      b8602df6114c41ef4de41d73209befd7cd84ff0a7431292f718a615fef7d6de9

  Open Babel environment:

      module label: obabel/3.1.1
      executable: /usr/local/apps/obabel-3.1.1/bin/obabel
      reported version: Open Babel 3.1.0

- Result:
  The downloaded PubChem structure is internally consistent with Gefitinib,
  contains the expected 55 atoms and molecular formula C22H24ClFN4O3, consists
  of one connected molecular graph, and contains no isolated atoms or explicit
  formal-charge records.

- Problems encountered:
  None.

- Root cause:
  Not applicable.

- Correction:
  Not applicable.

- Why the correction was justified:
  Not applicable.

- Decision / advancement gate:
  PASS.

  The PubChem CID 123631 3D SDF is accepted as the immutable raw Gefitinib
  source structure.

  Gefitinib may advance to reproducible MMFF94 preparation.

- Archive / checksum status:
  Raw source retained at:

      structures/raw/gefitinib_pubchem_cid123631_3d.sdf

  SHA256:

      b8602df6114c41ef4de41d73209befd7cd84ff0a7431292f718a615fef7d6de9

- What remains:
  1. Commit the validated raw Gefitinib source.
  2. Generate the MMFF94-prepared Gefitinib structure.
  3. Validate atom order, connectivity, composition, and geometry preservation.
  4. Construct the Gefitinib PM6 Gaussian input only after preparation passes.

- Next action:
  Commit the accepted raw Gefitinib source and validation record.




### Entry 016 — 2026-09-21 — Gefitinib MMFF94 preparation and validation

- Scientific/build objective:
  Generate a reproducibly prepared Gefitinib geometry from the accepted raw
  PubChem structure using MMFF94 minimization and verify that molecular identity,
  atom ordering, composition, and bonding remain unchanged.

- Starting state:
  The accepted immutable raw Gefitinib source was:

      structures/raw/gefitinib_pubchem_cid123631_3d.sdf

  PubChem CID:

      123631

  Raw-source acceptance commit:

      3760ef3

  Raw-source SHA256:

      b8602df6114c41ef4de41d73209befd7cd84ff0a7431292f718a615fef7d6de9

- Commands / actions performed:
  Loaded the documented Open Babel Maple environment.

  Performed MMFF94 minimization using:

      obabel structures/raw/gefitinib_pubchem_cid123631_3d.sdf \
        -O structures/prepared/gefitinib_mmff94_prep_v01.mol \
        --minimize --ff MMFF94 --steps 500

  Compared raw and prepared structures using:
      atom count,
      atom ordering,
      bond topology,
      SMILES,
      and same-index Cartesian coordinate RMSD.

- Files changed:
      structures/prepared/gefitinib_mmff94_prep_v01.mol
      LAB_JOURNAL.md

- Job IDs / run IDs:
  No Gaussian RUN_ID assigned at this stage.

- Git commit:
  Pending.

- Validation performed:
  Raw atom count:

      55

  Prepared atom count:

      55

  Atom order identical:

      True

  Bond topology identical:

      True

  Raw SMILES:

      Clc1cc(Nc2ncnc3c2cc(OCCCN2CCOCC2)c(OC)c3)ccc1F

  Prepared SMILES:

      Clc1cc(Nc2ncnc3c2cc(OCCCN2CCOCC2)c(OC)c3)ccc1F

  Same-index coordinate RMSD:

      0.08239655994584419 Å

  Prepared structure SHA256:

      03d3b29cb3f71befd0671c12746b0dbc95f842a6b1308928aaf3fe4d76fba85c

  Open Babel environment:

      module label: obabel/3.1.1
      executable: /usr/local/apps/obabel-3.1.1/bin/obabel
      reported version: Open Babel 3.1.0

- Result:
  MMFF94 minimization produced a modest geometry relaxation while preserving
  the molecular identity, atom order, and complete bond topology of Gefitinib.

- Problems encountered:
  None.

- Root cause:
  Not applicable.

- Correction:
  Not applicable.

- Why the correction was justified:
  Not applicable.

- Decision / advancement gate:
  PASS.

  The prepared Gefitinib structure is accepted for Gaussian PM6 input
  construction.

- Archive / checksum status:
  Prepared structure:

      structures/prepared/gefitinib_mmff94_prep_v01.mol

  SHA256:

      03d3b29cb3f71befd0671c12746b0dbc95f842a6b1308928aaf3fe4d76fba85c

- What remains:
  1. Commit the validated prepared Gefitinib structure.
  2. Construct the Gefitinib PM6 Gaussian input.
  3. Validate exact coordinate transfer from the prepared MOL file.
  4. Lock the production input in Git before submission.

- Next action:
  Commit the validated Gefitinib MMFF94 preparation.


### Entry 017 — 2026-09-21 — Gefitinib PM6 production input construction and preflight lock

- Scientific/build objective:
  Construct the Gefitinib PM6 production input from the accepted MMFF94-prepared
  structure, verify exact coordinate transfer and production metadata, and
  confirm that the proposed RUN_ID and output paths are collision-free before
  submission.

- Starting state:
  Accepted prepared Gefitinib structure:

      structures/prepared/gefitinib_mmff94_prep_v01.mol

  Prepared-structure acceptance commit:

      5156176

  Prepared structure SHA256:

      03d3b29cb3f71befd0671c12746b0dbc95f842a6b1308928aaf3fe4d76fba85c

- Commands / actions performed:
  Generated the Gaussian PM6 input:

      calculations/phase1_dft/pm6/inputs/gefitinib_pm6_opt_v01.com

  using the accepted prepared MOL coordinates without atom reordering.

  Verified:
      Gaussian route,
      checkpoint path,
      memory,
      processor count,
      title,
      charge,
      multiplicity,
      atom count,
      atom order,
      exact coordinate transfer,
      input SHA256,
      RUN_ID collision status,
      and output-path collision status.

- Files changed:
      calculations/phase1_dft/pm6/inputs/gefitinib_pm6_opt_v01.com
      LAB_JOURNAL.md

- Job IDs / run IDs:
  Proposed production RUN_ID:

      PM6-GEFITINIB-001

  PBS job:

      not yet submitted

- Git commit:
  Pending.

- Validation performed:
  Gaussian header:

      %chk=archive/chk/gefitinib_pm6_opt_v01.chk
      %mem=8GB
      %nprocshared=8
      #p PM6 opt SCF=XQC

  Title:

      gefitinib PM6 pre-optimization | system=gefitinib charge=0 mult=1 | v01

  Charge / multiplicity:

      0 1

  Prepared MOL atom count:

      55

  Gaussian input atom count:

      55

  Element order identical:

      True

  Maximum coordinate delta:

      0.0 Å

  Input SHA256:

      065ac1eea119603f167ab3f0e5dd820fb04ff88fde6fddad5c23058d59c5eb9c

  RUN_ID collision check:

      no existing PM6-GEFITINIB-001 records

  Working output collision check:

      no existing archive/logs/gefitinib_pm6_opt_v01.log
      no existing archive/chk/gefitinib_pm6_opt_v01.chk

- Result:
  The Gefitinib PM6 production input is internally consistent with the accepted
  prepared structure and is ready to be locked in Git before submission.

- Problems encountered:
  An initial Python input-generation command used f-string syntax unsupported by
  the Python version available on Maple.

- Root cause:
  The Maple Python interpreter does not support that f-string syntax.

- Correction:
  Replaced the f-string formatting with the older compatible .format() method
  and regenerated the input.

- Why the correction was justified:
  The failure occurred before successful file generation. The corrected script
  produced a 55-atom input with exact atom-order and coordinate preservation.

- Decision / advancement gate:
  PASS.

  The Gefitinib PM6 input is approved for production lock.

  Proposed production identifier:

      PM6-GEFITINIB-001

- Archive / checksum status:
  Production input:

      calculations/phase1_dft/pm6/inputs/gefitinib_pm6_opt_v01.com

  SHA256:

      065ac1eea119603f167ab3f0e5dd820fb04ff88fde6fddad5c23058d59c5eb9c

  No production log or checkpoint exists yet.

- What remains:
  1. Commit the PM6 production input and Entry 017.
  2. Verify clean Git state.
  3. Submit PM6-GEFITINIB-001.
  4. Capture PBS job ID and production provenance.
  5. Perform scientific acceptance after completion.

- Next action:
  Commit the Gefitinib PM6 production input before submission.




### Entry 018 — 2026-09-21 — PM6-GEFITINIB-001 completion and scientific acceptance

- Scientific/build objective:
  Evaluate the completed Gefitinib PM6 geometry optimization, confirm Gaussian
  and QC success, verify the production checkpoint and provenance, and determine
  whether the PM6 Gefitinib baseline may advance to B3LYP optimization.

- Starting state:
  Production input:

      calculations/phase1_dft/pm6/inputs/gefitinib_pm6_opt_v01.com

  Production RUN_ID:

      PM6-GEFITINIB-001

  Production Git commit:

      4356191

  Input SHA256:

      065ac1eea119603f167ab3f0e5dd820fb04ff88fde6fddad5c23058d59c5eb9c

- Commands / actions performed:
  Inspected the completed Gaussian provenance record, QC summary, optimization
  markers, production checkpoint, and run ledger.

  Rebuilt:

      run_log.tsv

  using:

      scripts/build_run_log.sh --write

- Files changed:
      run_log.tsv
      LAB_JOURNAL.md

  Production-generated records:

      calculations/phase1_dft/pm6/prov/PM6-GEFITINIB-001.prov
      calculations/phase1_dft/pm6/summaries/gefitinib_pm6_opt_v01.summary.txt

- Job IDs / run IDs:
      RUN_ID: PM6-GEFITINIB-001
      PBS job: 7712055.maple
      execution host: cn070

- Git commit:
      production input commit: 4356191
      acceptance commit: pending

- Validation performed:
  Gaussian build:

      g16-c01-avx2

  Charge / multiplicity:

      0 1

  Atom count:

      55

  Gaussian termination:

      NORMAL

  Optimization:

      COMPLETED

  Stationary point:

      FOUND

  Gaussian exit:

      0

  QC exit:

      0

  QC status:

      PASS

  Final PM6 SCF energy:

      -0.143959081671 Hartree

  Production Git provenance:

      git_commit = 4356191
      git_dirty = no

  Output SHA256:

      98369b71273ba9db221a7a02a3f55285240e2ccbb1de93041b1b48c66e7a1e68

  Checkpoint SHA256:

      4caf81939e1808f877c0360758b9274190af73655d69064d87fecda7bcaa2925

- Result:
  Gefitinib PM6 optimization completed successfully and produced a valid
  stationary geometry and checkpoint suitable for the B3LYP stage.

- Problems encountered:
  None during production execution or QC.

- Root cause:
  Not applicable.

- Correction:
  Not applicable.

- Why the correction was justified:
  Not applicable.

- Decision / advancement gate:
  PASS.

  PM6-GEFITINIB-001 is scientifically accepted.

  Gefitinib may advance to B3LYP-D3(BJ)/6-31G(d,p), SMD-water optimization
  and frequency analysis after immutable PM6 archive closure.

- Archive / checksum status:
  Working log:

      archive/logs/gefitinib_pm6_opt_v01.log

  Log SHA256:

      98369b71273ba9db221a7a02a3f55285240e2ccbb1de93041b1b48c66e7a1e68

  Working checkpoint:

      archive/chk/gefitinib_pm6_opt_v01.chk

  Checkpoint SHA256:

      4caf81939e1808f877c0360758b9274190af73655d69064d87fecda7bcaa2925

  Permanent run-specific archive preservation pending.

- What remains:
  1. Commit the PM6 Gefitinib acceptance package.
  2. Preserve the accepted PM6 log and checkpoint as immutable run001 artifacts.
  3. Extend archive-manifest mapping for Gefitinib PM6.
  4. Verify archive integrity.
  5. Construct the Gefitinib B3LYP input from the immutable PM6 checkpoint.

- Next action:
  Commit the PM6 Gefitinib scientific-acceptance package before archive closure.



### Entry 019 — 2026-09-21 — PM6-GEFITINIB-001 immutable archive closure

- Scientific/build objective:
  Preserve the accepted PM6-GEFITINIB-001 production log and checkpoint as
  immutable run-specific archive artifacts and extend archive-manifest mapping
  so the Gefitinib PM6 files resolve to their canonical RUN_ID.

- Starting state:
  PM6-GEFITINIB-001 had passed scientific acceptance and was committed in:

      7a62911

  Accepted working log:

      archive/logs/gefitinib_pm6_opt_v01.log

  Accepted working checkpoint:

      archive/chk/gefitinib_pm6_opt_v01.chk

  Log SHA256:

      98369b71273ba9db221a7a02a3f55285240e2ccbb1de93041b1b48c66e7a1e68

  Checkpoint SHA256:

      4caf81939e1808f877c0360758b9274190af73655d69064d87fecda7bcaa2925

- Commands / actions performed:
  Created immutable run-specific copies:

      archive/logs/gefitinib_pm6_opt_v01.run001.log
      archive/chk/gefitinib_pm6_opt_v01.run001.chk

  Verified each immutable copy was byte-identical to the accepted working
  artifact using SHA256.

  Extended:

      scripts/build_archive_manifest.sh

  with Gefitinib PM6 mapping:

      gefitinib_pm6_* -> PM6-GEFITINIB-${run_number}

  Rebuilt:

      archive_manifest.tsv

  Verified the complete immutable archive.

- Files changed:
      scripts/build_archive_manifest.sh
      archive_manifest.tsv
      LAB_JOURNAL.md

- Job IDs / run IDs:
      RUN_ID: PM6-GEFITINIB-001
      PBS job: 7712055.maple

- Validation performed:
  Working log SHA256:

      98369b71273ba9db221a7a02a3f55285240e2ccbb1de93041b1b48c66e7a1e68

  Immutable log SHA256:

      98369b71273ba9db221a7a02a3f55285240e2ccbb1de93041b1b48c66e7a1e68

  Working checkpoint SHA256:

      4caf81939e1808f877c0360758b9274190af73655d69064d87fecda7bcaa2925

  Immutable checkpoint SHA256:

      4caf81939e1808f877c0360758b9274190af73655d69064d87fecda7bcaa2925

  Archive verification:

      PASSED

  Total immutable archive files verified:

      14

  Manifest entries for both Gefitinib PM6 run001 artifacts resolve to:

      PM6-GEFITINIB-001

- Result:
  PM6-GEFITINIB-001 has been preserved as a fully traceable immutable archive
  set.

  The archive manifest correctly records both the production log and checkpoint
  under the canonical Gefitinib PM6 RUN_ID.

- Problems encountered:
  None during archive closure.

- Root cause:
  Not applicable.

- Correction:
  Not applicable.

- Why the correction was justified:
  Not applicable.

- Decision / advancement gate:
  PASS.

  PM6-GEFITINIB-001 archive closure is complete.

  Gefitinib may advance to B3LYP-D3(BJ)/6-31G(d,p), SMD-water optimization
  and frequency analysis using the immutable PM6 checkpoint.

- Archive / checksum status:
  IMMUTABLE ARCHIVE CLOSED.

  Log:

      archive/logs/gefitinib_pm6_opt_v01.run001.log

  Checkpoint:

      archive/chk/gefitinib_pm6_opt_v01.run001.chk

  Archive manifest:

      archive_manifest.tsv

  Archive verification:

      PASS

- What remains:
  1. Commit the Gefitinib PM6 archive closure.
  2. Construct the Gefitinib B3LYP input from the immutable PM6 checkpoint.
  3. Preflight and lock the B3LYP production input.
  4. Submit B3LYP-GEFITINIB-001.

- Next action:
  Commit the PM6 Gefitinib reproducibility archive closure.



### Entry 020 — 2026-09-21 — Gefitinib B3LYP input construction and preflight

- Scientific/build objective:
  Construct and validate the Gefitinib B3LYP-D3(BJ)/6-31G(d,p),
  SMD-water optimization and frequency-analysis input from the accepted
  immutable PM6 checkpoint.

- Starting state:
  Gefitinib PM6 baseline had passed scientific acceptance and immutable
  archive closure.

  Accepted immutable PM6 checkpoint:

      archive/chk/gefitinib_pm6_opt_v01.run001.chk

  PM6 checkpoint SHA256:

      4caf81939e1808f877c0360758b9274190af73655d69064d87fecda7bcaa2925

  PM6 archive-closure commit:

      24dbd86

- Commands / actions performed:
  Constructed:

      calculations/phase1_dft/b3lyp/inputs/gefitinib_b3lyp_optfreq_v01.com

  using the accepted Erlotinib B3LYP input as the production-method template.

  The input reads geometry and wavefunction information from the immutable
  Gefitinib PM6 checkpoint using:

      %oldchk=archive/chk/gefitinib_pm6_opt_v01.run001.chk

  The B3LYP working checkpoint is:

      %chk=archive/chk/gefitinib_b3lyp_optfreq_v01.chk

- Files changed:
      calculations/phase1_dft/b3lyp/inputs/gefitinib_b3lyp_optfreq_v01.com
      LAB_JOURNAL.md

- Job IDs / run IDs:
      Planned RUN_ID: B3LYP-GEFITINIB-001

- Git commit:
      input lock commit: pending

- Validation performed:
  Gefitinib B3LYP input SHA256:

      8b54814e17859421125fcb4874f9e7ce0f8b66858ee8ea5f36d3db985a61342d

  Immutable PM6 source-checkpoint SHA256:

      4caf81939e1808f877c0360758b9274190af73655d69064d87fecda7bcaa2925

  Compared against accepted Erlotinib B3LYP input template.

  Validation results:

      template_lines = 10
      target_lines = 10
      route_identical = True
      memory_identical = True
      nproc_identical = True
      charge_mult_identical = True
      nonblank_lines_after_charge_mult = 0

  Route:

      #p opt freq B3LYP/6-31G(d,p) EmpiricalDispersion=GD3BJ SCRF=(SMD,Solvent=Water) geom=check

  Resources encoded in Gaussian input:

      %mem=32GB
      %nprocshared=16

  Charge / multiplicity:

      0 1

  Collision preflight:
  No existing Gefitinib B3LYP working log or checkpoint was found.

  The existing occurrence of B3LYP-GEFITINIB-001 in LAB_JOURNAL.md is a
  previously documented planned future action and is not an executed-run
  record.

- Result:
  Gefitinib B3LYP production input is structurally consistent with the
  previously accepted B3LYP workflow and points to the correct immutable
  PM6 checkpoint.

- Problems encountered:
  None.

- Root cause:
  Not applicable.

- Correction:
  Not applicable.

- Why the correction was justified:
  Not applicable.

- Decision / advancement gate:
  PASS.

  The Gefitinib B3LYP input is approved for production locking in Git.

  Submission must occur only after the input and this journal entry are
  committed, pushed, and the repository is confirmed clean.

- Archive / checksum status:
  Source PM6 checkpoint is immutable and archive-verified.

  B3LYP output archive artifacts do not yet exist because the production run
  has not yet been submitted.

- What remains:
  1. Commit and push the validated Gefitinib B3LYP input.
  2. Confirm repository synchronization and clean state.
  3. Assign production RUN_ID B3LYP-GEFITINIB-001.
  4. Submit the production calculation.
  5. Validate optimization, frequencies, and thermochemistry after completion.

- Next action:
  Lock the Gefitinib B3LYP production input in Git.




### Entry 021 — 2026-09-21 — B3LYP-GEFITINIB-001 completion and scientific acceptance

- Scientific/build objective:
  Evaluate the completed Gefitinib B3LYP-D3(BJ)/6-31G(d,p),
  SMD-water optimization and frequency analysis and determine whether the
  optimized isolated-drug structure satisfies the Phase I acceptance criteria.

- Starting state:
  Production input:

      calculations/phase1_dft/b3lyp/inputs/gefitinib_b3lyp_optfreq_v01.com

  Production RUN_ID:

      B3LYP-GEFITINIB-001

  Production Git commit:

      58199fe

  Input SHA256:

      8b54814e17859421125fcb4874f9e7ce0f8b66858ee8ea5f36d3db985a61342d

- Commands / actions performed:
  Inspected the production provenance, QC summary, Gaussian optimization
  markers, vibrational frequencies, thermochemistry, and B3LYP checkpoint.

  Counted all reported vibrational frequencies programmatically and checked
  for negative frequencies.

- Files changed:
      run_log.tsv
      LAB_JOURNAL.md

  Production-generated records:

      calculations/phase1_dft/b3lyp/prov/B3LYP-GEFITINIB-001.prov
      calculations/phase1_dft/b3lyp/summaries/gefitinib_b3lyp_optfreq_v01.summary.txt

- Job IDs / run IDs:
      RUN_ID: B3LYP-GEFITINIB-001
      PBS job: 7712077.maple
      execution host: cn136

- Git commit:
      production input commit: 58199fe
      acceptance commit: pending

- Validation performed:
  Gaussian build:

      g16-c01-avx2

  Charge / multiplicity:

      0 1

  Atom count:

      55

  Gaussian termination:

      NORMAL

  Optimization:

      COMPLETED

  Stationary point:

      FOUND

  Expected vibrational modes for nonlinear 55-atom molecule:

      3N - 6 = 159

  Observed frequencies:

      159

  Imaginary frequencies:

      0

  Lowest frequency:

      15.9122 cm^-1

  Highest frequency:

      3643.7339 cm^-1

  Final B3LYP SCF energy:

      -1857.65516482 Hartree

  Zero-point correction:

      0.443494 Hartree

  Thermal correction to Gibbs Free Energy:

      0.382699 Hartree

  Sum of electronic and zero-point Energies:

      -1857.211671 Hartree

  Gibbs free energy:

      -1857.272466 Hartree

  Gaussian exit:

      0

  QC exit:

      0

  QC status:

      PASS

  Production Git provenance:

      git_commit = 58199fe
      git_dirty = no

  Output SHA256:

      ff33af5564e89743737835f13fccf64ad581bcc38da7899104d9a4656c6f70f5

  Checkpoint SHA256:

      e25c56576ab5bdfad14b8fd215c0005f8137ec767932f69007a2487e5fe7082d

- Result:
  Gefitinib B3LYP optimization and frequency analysis completed successfully.

  The optimized structure is a stationary point with no imaginary
  frequencies and therefore satisfies the isolated-species minimum-energy
  acceptance criterion for this stage.

- Problems encountered:
  None during production execution or scientific QC.

- Root cause:
  Not applicable.

- Correction:
  Not applicable.

- Why the correction was justified:
  Not applicable.

- Decision / advancement gate:
  PASS.

  B3LYP-GEFITINIB-001 is scientifically accepted.

  The isolated Gefitinib B3LYP baseline is complete and may be preserved as
  immutable archive artifacts.

- Archive / checksum status:
  Working log:

      archive/logs/gefitinib_b3lyp_optfreq_v01.log

  Log SHA256:

      ff33af5564e89743737835f13fccf64ad581bcc38da7899104d9a4656c6f70f5

  Working checkpoint:

      archive/chk/gefitinib_b3lyp_optfreq_v01.chk

  Checkpoint SHA256:

      e25c56576ab5bdfad14b8fd215c0005f8137ec767932f69007a2487e5fe7082d

  Permanent run-specific archive preservation pending.

- What remains:
  1. Rebuild run_log.tsv.
  2. Commit the Gefitinib B3LYP acceptance package.
  3. Create immutable run001 B3LYP log and checkpoint copies.
  4. Extend archive-manifest mapping for Gefitinib B3LYP.
  5. Verify the complete archive.
  6. Advance to the next isolated drug baseline after archive closure.

- Next action:
  Rebuild the run ledger and commit the B3LYP Gefitinib scientific-acceptance package.



