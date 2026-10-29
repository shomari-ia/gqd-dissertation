# Computational Workflow v2.0 — Phase I DFT Drug Loading

**Controlled date:** 2026-10-29  
**Status:** Canonical Phase I workflow.  
**Active Gaussian platform:** Magnolia / Slurm / Gaussian 16 C.02.

This document supersedes the earlier Phase I workflow presentation while preserving its scientifically valid history. It integrates the corrected GQD lineage, Acceptance Gates v2.0, status-versus-disposition semantics, the validated Magnolia execution layer, and the Scientific Evidence / Supersession control system.

Phases II and III are governed by the Execution Plan and Scientific Scope until they enter production. Their detailed computational workflows will be added when those phases begin.

---

## 1. Governing principle

A result advances only when its **applicable scientific gates pass**.

Gaussian normal termination, optimization completion, and zero imaginary frequencies are necessary for many calculations but are not sufficient by themselves to establish molecular-model validity or scientific acceptance.

Acceptance is governed by `docs/acceptance_gates_v2.md`.

### Gate map

- **G0** — lineage and input identity
- **G1** — molecular identity
- **G2** — graph / connectivity / topology
- **G3** — geometry / pose plausibility
- **G4** — execution / numerical QC
- **G5** — stationary point / frequency
- **G6** — scientific comparability
- **G7** — provenance / reproducibility
- **G8** — archive integrity
- **G9** — independent scientific validation

---

## 2. Execution status, scientific disposition, advancement

These are separate fields.

### Execution / QC status

Examples:
- `PASS`
- `FAILED`
- `MISSING_LOG`

### Scientific disposition

Examples:
- `ACCEPTED_CURRENT`
- `ACCEPTED_COMPARISON`
- `ACCEPTED_ISOLATED_BASELINE`
- `ACCEPTED_ADSORPTION_MINIMUM`
- `ACCEPTED_PLATFORM_VALIDATION`
- `SUPERSEDED_STRUCTURAL_MODEL`
- `RETAINED_FREQUENCY_FAILURE`
- `RETAINED_INPUT_FORMAT_FAILURE`
- `RETAINED_INFRASTRUCTURE_FAILURE`
- `QUARANTINED`

A calculation may remain `PASS` as an execution fact while being scientifically superseded.

---

## 3. Platform control

### Historical execution layer

Maple / OpenPBS / Gaussian 16 C.01 is retained for provenance.

Accepted Maple results remain scientifically valid according to their individual dispositions.

No new Gaussian production work should be launched on Maple.

### Active production layer

Magnolia / Slurm / Gaussian 16 C.02 is the active Gaussian production environment.

Validated control:
- `B3LYP-ERLOTINIB-MAGNOLIA-VALIDATION-001`
- Slurm job `320607`
- node `node019`
- 16 Gaussian shared cores
- 32 GB Gaussian memory
- 64 GB scheduler allocation
- local scratch
- runtime Git identity
- output/checkpoint hashing
- QC summary
- provenance and ledger integration

The validation reproduced the accepted Maple Erlotinib baseline to the project-reported precision.

Submission wrapper:
- historical: `scripts/run_gaussian.pbs`
- active: `scripts/run_gaussian_magnolia.slurm`

The historical PBS wrapper must not be overwritten.

---

## 4. Step 1 — deterministic structure preparation

### Corrected COOH-GQD

Input:
- deterministically rebuilt circumcoronene parent.

Tools:
- `scripts/build_circumcoronene.py`
- `scripts/hydrogenate_circumcoronene.py`
- `scripts/functionalize_circumcoronene_cooh.py`

Required corrected-carrier identity:
- C55H18O2
- 75 atoms
- intact C54 circumcoronene scaffold
- 72 scaffold C-C edges
- 18 degree-2 carbons
- 36 degree-3 carbons
- 19 six-membered cycles
- one COOH substituent
- standardized C72/O73/O74/H75 functional-group mapping
- charge 0
- multiplicity 1

**Gates:** G0-G3, G9 as applicable.

On failure:
- return to deterministic construction;
- identify the structural defect;
- do not hand-repair a malformed carrier merely to make a Gaussian input run.

Historical v01 GQD artifacts remain preserved but are scientifically `SUPERSEDED_STRUCTURAL_MODEL`.

### Drugs

Raw PubChem structures remain immutable.

Prepared drug structures follow the documented preparation route and must pass identity/protonation/atom-order checks before quantum-chemical advancement.

---

## 5. Step 2 — isolated-species PM6 preparation

PM6 remains part of the isolated-monomer preparation history and corrected isolated GQD workflow.

PM6 is **not** a scientific adsorption-basin selector and is **not** used to choose complex pose orientations.

For corrected isolated GQD candidates, the final PM6 geometry must independently retain:
- C55H18O2 identity;
- intended scaffold topology;
- one COOH attachment;
- absence of unintended bonding;
- absence of severe scaffold distortion.

PM6 energy is recorded but is not compared directly with DFT energy and never enters the final DFT binding-energy expression.

**Gates:** G0-G2, G4, G7-G9 as applicable.

---

## 6. Step 3 — isolated B3LYP optimization and frequency

Primary level:

`B3LYP-D3(BJ)/6-31G(d,p), SMD water`

Standard isolated-species gate:
- normal termination;
- optimization completed;
- 0 imaginary frequencies for an accepted minimum;
- molecular/model identity retained;
- provenance complete;
- archive/checksum complete;
- independent scientific validation where required.

### Corrected GQD lineage

Accepted:
- `B3LYP-COOH-GQD-C1-004` — authoritative current baseline.
- `B3LYP-COOH-GQD-C2-005` — accepted comparison minimum.

Retained frequency-failure history:
- `B3LYP-COOH-GQD-C1-002`
- `B3LYP-COOH-GQD-C2-003`

The v02 failures remain evidence. The v03 retries used validated imaginary-mode displacement and fresh checkpoints.

### Isolated drug baselines

Accepted:
- `B3LYP-ERLOTINIB-001`
- `B3LYP-GEFITINIB-001`
- `B3LYP-VENETOCLAX-001`
- `B3LYP-ABT737-001`

These are not invalidated by the separate GQD structural correction.

### Restart rule

`guess=read` is permitted only for a same-level restart with compatible checkpoint content.

Do not carry a PM6 wavefunction into a DFT calculation.

---

## 7. Step 4 — deterministic complex construction

Complexes are constructed only from accepted isolated B3LYP monomers.

### Fragment order

1. authoritative GQD
2. accepted drug

Atom order is preserved.

The drug may undergo rigid-body translation/rotation for pose construction. Its internal geometry must not be altered before complex optimization.

### Required starting hypotheses

- **Flat:** drug aromatic/core plane approximately parallel to the corrected GQD basal plane.
- **Slipped:** distinct parallel basal pose with controlled in-plane displacement.
- **Edge:** chemically directed edge interaction involving the functionalized GQD edge and a documented drug polar-contact site.

These are reproducible starting basins, not assumed equilibrium structures.

### Pre-submission gates

- source monomer identity/checksum;
- expected total formula and atom count;
- exact preservation of authoritative GQD coordinates and atom order;
- preserved drug element order and rigid-body internal distances;
- intended plane/orientation geometry;
- interfragment heavy-atom minimum >= 2.0 Å;
- interfragment all-atom minimum >= 2.0 Å for basal poses;
- documented exception for intentional donor-H...acceptor contact in a chemically directed edge pose;
- independent post-write validation.

**Mandatory:** G0-G3, G7, G9.

### No PM6 complex decision point

PM6 is not used to choose, pre-optimize, deduplicate, or rank complex adsorption basins.

All scientific basin decisions begin from the accepted B3LYP monomers and are resolved at the dispersion-corrected DFT level.

This is a reproducibility and scientific-method refinement, not an arbitrary method change.

---

## 8. Step 5 — B3LYP complex optimization and frequency

Primary level:

`B3LYP-D3(BJ)/6-31G(d,p), SMD water`

Current validated Magnolia DFT resource profile:
- one Slurm node;
- 16 Gaussian shared cores;
- 32 GB Gaussian memory;
- 64 GB scheduler allocation;
- local scratch.

### Acceptance

Each optimized pose is independently recorded.

For an accepted adsorption minimum:
- G0-G5 and G7-G9 must pass;
- normal termination;
- completed optimization;
- 0 imaginary frequencies;
- fragments remain scientifically interpretable;
- no hidden molecular-model failure;
- archive/provenance closure.

If two starting poses converge to the same minimum, record the degeneracy. Do not delete one lineage to make the dataset look cleaner.

### Current Erlotinib results

Accepted:
- `B3LYP-COOH-GQD-ERLOTINIB-FLAT-001`
- `B3LYP-COOH-GQD-ERLOTINIB-SLIPPED-001`

Unresolved:
- `B3LYP-COOH-GQD-ERLOTINIB-EDGE-001`

The Maple edge execution is `RETAINED_INFRASTRUCTURE_FAILURE`; it does not reject the edge adsorption hypothesis.

The next edge calculation must use a **new run ID** on Magnolia.

---

## 9. Failure classification and retry policy

Before changing a calculation, classify the failure.

### Structural/model failure

Return to structure construction or scientific model definition.

Example:
- historical malformed COOH-GQD lineage.

### True-minimum / frequency failure

Retain the run.
Diagnose the imaginary mode.
Create a new run ID for any retry.

### Input-format failure

Retain the failed run.
Repair only the syntactic defect.
Use a new run ID.

Examples:
- missing terminal Gaussian blank record.

### Infrastructure/resource failure

Preserve scheduler/log/checkpoint evidence.
Do not interpret the incomplete run chemically.
Change platform/resources only as justified.

Example:
- Maple Erlotinib edge memory-envelope failure.

### Provenance/metadata defect

Repair traceability without altering accepted scientific output.

### Platform transition

Validate against an accepted control before releasing the new environment.

---

## 10. Step 6 — pose comparison

A pose comparison is scientifically authorized only after the required basins are resolved.

Do not declare the global/retained pose from an incomplete basin set unless the missing basin has been scientifically excluded for a documented reason.

Current Erlotinib state:
- flat accepted;
- slipped accepted;
- edge unresolved.

Therefore the current flat/slipped energy ordering is an intermediate result, not the final complete adsorption conclusion.

---

## 11. Step 7 — binding energy and BSSE

Electronic binding energy:

`E_bind = E_complex - (E_GQD + E_drug)`

Negative values indicate favorable association under the defined model.

### Counterpoise

Use `Counterpoise=2` with controlled fragment labels and compatible charge/multiplicity definitions.

### Scientific-comparability gate

Before subtraction:
- same functional;
- same basis;
- same solvent definition;
- same intended charge/protonation state;
- compatible correction protocol.

If these conditions fail, the energy difference is not used as a binding energy.

**Mandatory:** G0-G1, G4, G6-G9.

---

## 12. Step 8 — M06-2X validation

Validation level:

`M06-2X/6-311+G(d,p), SMD water`

Use the accepted B3LYP optimized geometry.

Under the current protocol, do not add `EmpiricalDispersion=GD3BJ` to the M06-2X validation calculation.

Validation results are recorded separately from the primary B3LYP result.

---

## 13. Step 9 — electronic / noncovalent interaction analysis

Planned analyses, subject to the finalized analysis plan and available evidence:

- HOMO-LUMO quantities
- charge-transfer descriptors
- QTAIM
- NCI / RDG
- ELF
- DOS
- Fukui indices
- TDDFT / UV-Vis where justified

Wavefunction/analysis files must trace to the accepted complex run.

Derived figures and tables should be reproducible from scripts when feasible.

No descriptor enters the dissertation without an identifiable source run.

---

## 14. Step 10 — evidence promotion and results table

For every reported scientific value:

`reported value → evidence/register row → run_id → provenance/QC → input/output hash → archive artifact`

A result enters a dissertation table only when:
- its applicable gates pass;
- its scientific disposition allows use;
- the value traces to a run ID;
- archive/provenance integrity is closed.

Committee-facing promotion occurs through the Scientific Evidence Register and the appropriate SEP package.

---

## 15. Storage architecture

### GitHub

Version-controlled text/reproducibility layer:
- inputs;
- scripts;
- provenance;
- QC summaries;
- ledgers/registers;
- scope/workflow/gates;
- results tables and reproducible final figures.

### Full Gaussian artifacts

Full `.log`, `.chk`, `.fchk`, `.wfx`, cube and related large scientific artifacts remain outside Git and are indexed by `archive_manifest.tsv`.

### Google Drive scientific mirror

Authoritative project root:

`CDSE / GQD Dissertation /`

Large run artifacts should map to:

`04_RUN_ARCHIVE/<RUN_ID>/`

Recommended internal structure:

- `input/`
- `log/`
- `checkpoint/`
- `geometry/`
- `provenance/`
- `QC/`
- `MANIFEST.txt`

Scientific evidence packages live under:

`01_SCIENTIFIC_EVIDENCE/SEP-###_...`

Current committee-facing status lives under:

`00_CURRENT_STATUS/`

---

## 16. Operating loop

For every new production calculation:

1. pull / verify repository state;
2. validate scientific input;
3. assign new run ID;
4. commit the input;
5. submit through the correct platform wrapper;
6. capture scheduler/build/host/runtime provenance;
7. preserve output/checkpoint;
8. run QC;
9. perform applicable independent scientific/model validation;
10. classify execution status and scientific disposition;
11. update `run_notes.tsv` and rebuild `run_log.tsv`;
12. update archive manifest and verify hashes;
13. update `LAB_JOURNAL.md`;
14. update Scientific Evidence / Supersession control when the scientific state changes;
15. inspect Git diff;
16. commit, push, and verify remote closure;
17. only then release the result for the next scientific stage.

---

## 17. Current advancement point

The corrected GQD carrier is released.

All four isolated drug baselines are released.

Erlotinib flat and slipped adsorption minima are accepted.

The next authorized scientific execution is the corrected Erlotinib edge calculation on Magnolia under a new run ID, followed by completion of the Erlotinib pose comparison and controlled energetic validation.
