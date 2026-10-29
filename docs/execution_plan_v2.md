# GQD Dissertation Execution Plan v2.0

**Controlled date:** 2026-10-29  
**Purpose:** Gate-based execution plan coordinating computation, evidence control, writing, committee reporting, and dissertation completion.

This plan supersedes the earlier calendar-first execution plan. The three-phase scientific design remains unchanged, but execution now follows the corrected molecular baseline, Acceptance Gates v2.0, the validated Magnolia production environment, and the Scientific Evidence / Supersession control layer.

---

## 1. Dissertation objective

**Working title:** *Computational Investigation of Graphene Quantum Dot Anticancer Drug Interactions: A Multiscale Approach Using Density Functional Theory and Molecular Dynamics Simulations*

The dissertation tests a three-phase computational model:

1. **Phase I — DFT Drug Loading:** quantify and explain adsorption of erlotinib, gefitinib, venetoclax, and ABT-737 on a corrected monocarboxylated circumcoronene GQD.
2. **Phase II — pH-Responsive Release:** determine whether protonation-state changes alter carrier-drug energetics in a manner consistent with acidic-tumor release.
3. **Phase III — Biological Target Validation:** test whether released/free drug structures retain target-binding behavior against EGFR or Bcl-2 through docking and molecular dynamics.

The locked Phase I drug order is:

`Erlotinib → Gefitinib → Venetoclax → ABT-737`

---

## 2. Current controlled checkpoint

### Carrier

- Historical COOH-GQD v01 lineage: `SUPERSEDED_STRUCTURAL_MODEL`.
- Authoritative corrected carrier: `B3LYP-COOH-GQD-C1-004`.
- Formula: C55H18O2.
- Atom count: 75.
- Corrected Class-1/C1: accepted true minimum, 0 imaginary frequencies, post-DFT topology/model audit PASS.
- Corrected Class-2/C3: `B3LYP-COOH-GQD-C2-005`, retained valid comparison minimum.
- C1 is favored over C2 by approximately 3.2040 kcal/mol electronic energy and 3.0265 kcal/mol Gibbs free energy.

### Isolated drug baselines

Accepted and retained:

- `B3LYP-ERLOTINIB-001`
- `B3LYP-GEFITINIB-001`
- `B3LYP-VENETOCLAX-001`
- `B3LYP-ABT737-001`

The isolated drug calculations are independent of the historical malformed GQD lineage and remain scientifically valid.

### Corrected Erlotinib adsorption

- Flat: `B3LYP-COOH-GQD-ERLOTINIB-FLAT-001` — `ACCEPTED_ADSORPTION_MINIMUM`.
- Slipped: `B3LYP-COOH-GQD-ERLOTINIB-SLIPPED-001` — `ACCEPTED_ADSORPTION_MINIMUM`.
- Edge on Maple: `B3LYP-COOH-GQD-ERLOTINIB-EDGE-001` — `RETAINED_INFRASTRUCTURE_FAILURE`; no scientific edge conclusion.
- Immediate scientific requirement: fresh corrected edge execution on Magnolia under a new run ID.

### Active HPC platform

Magnolia / Slurm / Gaussian 16 C.02 is validated and released for new Gaussian production.

Validation control:

- `B3LYP-ERLOTINIB-MAGNOLIA-VALIDATION-001`
- Slurm job `320607`
- node `node019`
- 16 Gaussian shared cores
- 32 GB Gaussian memory
- 64 GB scheduler allocation
- local scratch
- QC/provenance/hash/archive integration
- reproduced accepted Maple Erlotinib baseline to the project-reported precision

Maple/OpenPBS/Gaussian 16 C.01 remains part of the historical record but is closed to new Gaussian production.

---

## 3. Execution-control rules

Every major result must move through:

`scientific input → Git commit → HPC execution → Gaussian output → QC → molecular/model validation → run ledger → provenance → checksum/archive → scientific disposition → evidence register → Lab Journal → dissertation/committee reporting`

A result does not advance because an output file exists.

Acceptance is governed by `docs/acceptance_gates_v2.md`:

- G0 lineage/input identity
- G1 molecular identity
- G2 graph/connectivity/topology
- G3 geometry/pose plausibility
- G4 execution/numerical QC
- G5 stationary point/frequency
- G6 scientific comparability
- G7 provenance/reproducibility
- G8 archive integrity
- G9 independent scientific validation

Execution/QC status and scientific disposition remain separate facts.

---

## 4. Phase I — DFT drug loading

### Scientific question

How favorably does each locked anticancer drug interact with the corrected COOH-GQD carrier, and what physical/electronic interactions explain the loading behavior?

### Primary level

`B3LYP-D3(BJ)/6-31G(d,p), SMD water`

### Validation level

`M06-2X/6-311+G(d,p), SMD water`

### Controlled complex-construction rule

Complexes are built only from accepted isolated B3LYP monomers.

- authoritative GQD first;
- drug second;
- atom order preserved;
- rigid-body transform only before optimization;
- deterministic flat / slipped / edge hypotheses;
- independent pose and clash validation before submission.

**PM6 is not used to choose adsorption basins or relative complex orientations.**

### Per-drug Phase I sequence

1. accepted isolated drug baseline;
2. deterministic flat/slipped/edge construction;
3. B3LYP-D3(BJ)/6-31G(d,p)/SMD optimization + frequency;
4. zero-imaginary-frequency and model/fragment validation;
5. pose comparison;
6. counterpoise BSSE-corrected binding energy;
7. M06-2X/6-311+G(d,p)/SMD validation;
8. electronic/NCI analyses according to the finalized analysis plan;
9. evidence package / results-table promotion only after all applicable gates pass.

### Current Phase I sequence

#### Erlotinib

Current:
- flat accepted;
- slipped accepted;
- edge unresolved.

Next:
- execute corrected edge on Magnolia;
- close the pose comparison;
- compute controlled binding/BSSE quantities;
- run M06-2X validation;
- complete selected electronic/NCI descriptors;
- populate Chapter 2 only from accepted evidence.

#### Gefitinib

Begin after Erlotinib pose-control logic is closed and reusable construction/QC procedures are confirmed.

#### Venetoclax

Proceed after Gefitinib using drug-specific core/polar-site mapping rather than reusing Erlotinib pose parameters.

#### ABT-737

Proceed after Venetoclax under the same controlled scientific gates.

---

## 5. Phase II — pH-responsive release

### Scientific question

Does changing the protonation state of the carrier and relevant drug sites alter drug-carrier binding sufficiently to support a pH-responsive release mechanism?

### Working states

Carrier:
- protonated `-COOH`
- deprotonated `-COO-`

Drug protonation states must be explicitly defined and charge-tracked before execution.

### Planned sequence

1. identify relevant protonation-state combinations;
2. construct state-specific complexes from accepted Phase I structures;
3. validate formula, charge, multiplicity, connectivity and proton placement;
4. B3LYP-D3(BJ)/6-31G(d,p)/SMD optimization + frequency;
5. state-specific energetic comparison;
6. Gibbs / ΔΔG interpretation;
7. relaxed dissociation/PES scans where supported;
8. release-mechanism interpretation.

Working study criterion retained from the scientific scope:

`ΔΔG > 5 kcal/mol`

This is an internal interpretation criterion within the computational model, not a clinical threshold.

---

## 6. Phase III — biological target validation

### Targets

- Erlotinib / Gefitinib → EGFR
- Venetoclax / ABT-737 → Bcl-2

### Docking

Current plan:
- AutoDock Vina;
- receptor preparation and grid definition;
- native/co-crystallized ligand redocking;
- working validation criterion: RMSD < 2.0 Å;
- compare free versus released drug structures.

### Molecular dynamics

The dissertation currently identifies GROMACS as the planned production MD engine. Before production MD begins, an implementation checkpoint will review:

- GROMACS production workflow;
- GPU-enabled GROMACS availability through MCSR;
- NAMD/VMD as a potential validation, visualization, or production option;
- committee expertise and reproducibility considerations.

This review is an implementation decision, not a change to the dissertation's scientific question.

Planned endpoints:
- RMSD
- RMSF
- hydrogen-bond persistence
- contact behavior
- structural stability
- MM/PBSA and/or MM/GBSA
- replica agreement / uncertainty where applicable

Working retained-efficacy comparison from the scientific scope:

`|ΔΔG_bind| < 2 kcal/mol`

This is a study interpretation rule, not proof of therapeutic or clinical efficacy.

---

## 7. Evidence and documentation deliverables

### Canonical computational controls

- `SCIENTIFIC_STATUS.md`
- `scientific_evidence_register.tsv`
- `supersession_register.tsv`
- `docs/acceptance_gates_v2.md`
- `docs/scientific_scope.md`
- `docs/computational_workflow.md`
- `run_log.tsv`
- `run_notes.tsv`
- `archive_manifest.tsv`
- `LAB_JOURNAL.md`

### Committee-facing evidence series

- SEP-001 — COOH-GQD Correction & Validation
- SEP-002 — Isolated Drug Baselines
- SEP-003 — Erlotinib Adsorption
- SEP-004 — Gefitinib Adsorption
- SEP-005 — Venetoclax Adsorption
- SEP-006 — ABT-737 Adsorption

### Publication / defense record

A curated Research Journal Publication Edition will be maintained separately from the audit journal. It will summarize major questions, evidence, decisions, corrections, defining principles, and accepted results without replacing `LAB_JOURNAL.md`.

---

## 8. Storage and source-of-truth architecture

### GitHub

Holds:
- inputs
- scripts
- configuration
- provenance
- QC summaries
- ledgers/registers
- scope/workflow/control documents
- derived text tables and reproducible figures

### MCSR / execution archive

Holds the active computational execution state and the full Gaussian artifacts generated on the HPC system.

### Google Drive

Current scientific archive root:

`CDSE / GQD Dissertation /`

Key folders:
- `00_CURRENT_STATUS/`
- `01_SCIENTIFIC_EVIDENCE/`
- `04_RUN_ARCHIVE/<RUN_ID>/`
- `06_COMMITTEE_REPORTS/`
- `07_DISSERTATION_CHAPTERS/`
- `08_METHODS_REPRODUCIBILITY/`
- `09_MANIFESTS_AND_INDEXES/`

The intended run-archive unit is one controlled folder per `RUN_ID`.

---

## 9. Gate-based working forecast

This is a working execution forecast, not a guarantee. Advancement is controlled by scientific gates, HPC throughput, and the size/convergence behavior of the remaining systems.

| Window | Primary objective | Advancement condition |
|---|---|---|
| Oct 29–Nov 7, 2026 | Re-execute Erlotinib edge on Magnolia; close corrected pose set | Edge reaches a scientifically interpretable result or is reclassified with evidence |
| Nov 1–Nov 14 | Erlotinib BSSE/binding and M06-2X validation; begin descriptor package | Accepted pose set + compatible energy records |
| Nov 8–Nov 21 | Gefitinib complex construction and B3LYP pose optimization | Accepted isolated monomers + pose gates |
| Nov 15–Dec 2 | Venetoclax pose workflow | Same |
| Nov 22–Dec 10 | ABT-737 pose workflow | Same |
| Dec 1–Dec 15 | Phase I evidence closure, comparison tables, Chapter 2 results/discussion | SEP-003–006 and Phase I table gates |
| Dec 8–Dec 22 | Phase II protonation-state construction and first state calculations | Phase I structures released |
| Dec 15–Jan 8 | Phase II energetic/release analysis | State-specific minima and comparable energies |
| Late Dec–Jan | Docking preparation/validation and free-vs-released comparison | Phase II released drug structures |
| Jan 2027 onward | MD production and trajectory analysis; integration | Validated MD engine/resource checkpoint |

### Completion objective

- **Stretch objective:** complete the major Phase I/II computational dataset by late December 2026.
- **Controlled objective:** complete the major computational dataset and docking/MD transition during January 2027.
- **Final defense-readiness timing:** depends primarily on MD throughput, analysis, committee review, and dissertation integration.

The schedule must be updated when a gate materially changes the critical path.

---

## 10. Writing plan

Writing proceeds in parallel with validated computation.

- Chapter 1: citation/context audit and final synthesis.
- Chapter 2: Methods locked to the validated Phase I workflow; Results populated only from accepted evidence.
- Chapter 3: Phase II methods/results as state models are released.
- Chapter 4: docking/MD workflow and results after engine/resource validation.
- Chapter 5: cross-phase integration after accepted evidence exists across phases.

No anticipated result is written as if it were an accepted result.

---

## 11. Advancement rule

The project advances by **evidence gates, not calendar pressure**.

When a problem is encountered:

1. classify the failure;
2. preserve the original evidence;
3. identify root cause;
4. correct only what the evidence justifies;
5. issue a new run ID where execution is repeated;
6. revalidate;
7. update the journal/ledger/registers;
8. commit and push;
9. only then advance or report the result as accepted.
