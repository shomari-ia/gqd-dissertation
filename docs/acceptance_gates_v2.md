# Acceptance Gates v2.0

## Controlling principle

A Gaussian job can be computationally successful without being scientifically acceptable.

Scientific acceptance requires the applicable model, topology, geometry, quantum-chemical, comparability, provenance, archive, and independent-validation gates to pass.

## Status and scientific disposition are separate

- **Execution/QC status** records what happened computationally in a specific run, for example `PASS` or `FAILED`.
- **Scientific disposition** records what the project is currently allowed to conclude from that run, for example `ACCEPTED_CURRENT`, `ACCEPTED_COMPARISON`, `SUPERSEDED_STRUCTURAL_MODEL`, or `RETAINED_INFRASTRUCTURE_FAILURE`.
- **Advancement decision** records whether the result may proceed to the next scientific stage: `RELEASE`, `RETAIN`, `HOLD`, `QUARANTINE`, or rejection for current scientific use.

A run may remain `status=PASS` while its scientific disposition is superseded.

## Core gates

| Gate | Control domain | Pass requirement | Hold/fail condition |
|---|---|---|---|
| G0 | Lineage and input identity | Unique run ID; intended sources identified; input identity/hash recorded; no reuse of quarantined/superseded coordinates | Source lineage ambiguous or historical evidence overwritten |
| G1 | Molecular identity | Expected formula, atom count, elements, charge, multiplicity, species/protonation state | Wrong composition, charge/multiplicity, missing or extra atoms |
| G2 | Graph/connectivity/topology | Intended covalent graph, scaffold invariants and functional-group attachment pass; no unintended bonding | Model does not represent the intended molecular graph |
| G3 | Geometry/pose plausibility | Physically plausible model; for complexes, accepted monomers, atom order, rigid-body identity, intended pose and clash limits pass | Severe distortion, unintended contacts, wrong fragment order, unsupported starting basin |
| G4 | Execution/numerical QC | Required normal termination, completed optimization/convergence, project QC PASS | Abnormal termination, incomplete optimization, unresolved resource/execution failure |
| G5 | Stationary point/frequency | Zero imaginary frequencies where a true minimum is required | One or more imaginary frequencies for a required minimum |
| G6 | Scientific comparability | Compatible method, basis, solvent, charge/protonation definitions, and correction protocol for compared energies | Incompatible energies subtracted or interpreted as directly comparable |
| G7 | Provenance/reproducibility | Git identity, scheduler/job ID, host, software build, input/output hashes, runtime metadata, QC summary and join key traceable | Missing or contradictory provenance prevents reconstruction |
| G8 | Archive integrity | Required artifacts inventoried and checksum-verified; failures preserved immutably | Missing evidence, overwrite, checksum mismatch or unassigned archive artifact |
| G9 | Independent scientific validation | Validation separate from the program's own success message confirms the intended scientific system and decision rule | Acceptance rests only on software success markers or a builder's own report |

## Stage-specific requirements

### Isolated corrected GQD

Mandatory: G0-G2, G4-G5, G7-G9.

The corrected COOH-GQD additionally requires deterministic circumcoronene graph validation plus independent post-PM6 and post-DFT topology/model audits.

### Isolated drug baseline

Mandatory: G0-G1, G4-G5, G7-G9.

Drug identity/protonation must be established independently. A correction to the separate GQD scaffold does not automatically invalidate an accepted isolated drug calculation.

### Complex starting geometry

Mandatory: G0-G3, G7, G9.

Only accepted monomers may be used. The GQD is written first and the drug second. Rigid-body preservation, fragment identity, intended pose, and clash gates must pass before submission.

### Optimized drug-GQD minimum

Mandatory: G0-G5, G7-G9.

Each pose is logged independently. If two poses converge to the same structure, that is recorded as a scientific result rather than deleted.

### Binding/BSSE/validation energy

Mandatory: G0-G1, G4, G6-G9.

Subtracted energies must use compatible method/basis/solvent/charge definitions. Counterpoise and M06-2X validation follow the controlled workflow.

### Platform migration validation

Mandatory: G0, G4, G7-G9.

Use an already accepted scientific control. Record software-build and scheduler differences and compare the accepted scientific quantities. Bit-for-bit identity is not required unless explicitly claimed.

## Controlled scientific dispositions

| Disposition | Meaning | Downstream use |
|---|---|---|
| ACCEPTED_CURRENT | Authoritative current baseline | Yes |
| ACCEPTED_COMPARISON | Valid comparison result, not production baseline | Comparison only |
| ACCEPTED_ISOLATED_BASELINE | Accepted isolated molecule | Yes |
| ACCEPTED_ADSORPTION_MINIMUM | Valid optimized adsorption minimum | Yes, for later controlled comparison |
| ACCEPTED_PLATFORM_VALIDATION | Platform continuity demonstrated | Releases platform |
| SUPERSEDED_STRUCTURAL_MODEL | Execution history retained but model no longer scientifically eligible | No |
| RETAINED_FREQUENCY_FAILURE | Completed run failed true-minimum gate | No |
| RETAINED_INPUT_FORMAT_FAILURE | Failure caused by input syntax/formatting | No; retry under new run ID |
| RETAINED_INFRASTRUCTURE_FAILURE | Execution/resource failure; no molecular conclusion | No; re-execute appropriately |
| QUARANTINED | Preserved artifact explicitly barred from reuse | No |

## Failure classification

Failures must be classified by cause before correction:

- structural/model failure → return to construction/model definition;
- frequency/true-minimum failure → diagnose mode and retry under new run ID;
- input-format failure → repair syntax without changing molecular science;
- infrastructure/resource failure → preserve evidence and rerun under suitable resources/platform;
- provenance/metadata defect → repair traceability without modifying scientific outputs;
- platform transition → validate against an accepted control before release.

A failed execution must not be converted into a chemical conclusion unless the calculation reached the scientific state required to support that conclusion.

## Supersession and immutability

Supersession never deletes history. The predecessor remains in the ledger/archive with its original execution facts. Its scientific disposition records why it is no longer eligible and identifies the replacement lineage. New retries require new run IDs. Historical inputs, logs, checkpoints, hashes and scheduler evidence are not overwritten.

## Current examples

| Run | QC | Scientific disposition | Decision |
|---|---|---|---|
| `B3LYP-COOH-GQD-001` | PASS; 0 imaginary frequencies | SUPERSEDED_STRUCTURAL_MODEL | Not a current GQD baseline |
| `B3LYP-COOH-GQD-C1-004` | PASS; 0 imaginary; model audit PASS | ACCEPTED_CURRENT | Authoritative GQD baseline / RELEASE |
| `B3LYP-COOH-GQD-C2-005` | PASS; 0 imaginary; model audit PASS | ACCEPTED_COMPARISON | Retain comparison minimum |
| `B3LYP-COOH-GQD-ERLOTINIB-EDGE-001` | FAILED; incomplete | RETAINED_INFRASTRUCTURE_FAILURE | No edge conclusion; rerun on Magnolia |
| `B3LYP-ERLOTINIB-MAGNOLIA-VALIDATION-001` | PASS; reproduced accepted control | ACCEPTED_PLATFORM_VALIDATION | Magnolia released |

## Governance

Changes to acceptance logic must be documented in `LAB_JOURNAL.md`, reflected in canonical scope/workflow documentation when applicable, committed to Git, and recorded in `supersession_register.tsv` when they change the scientific eligibility of an existing result.

The Scientific Evidence Register summarizes claims. It does not replace `run_log.tsv`, provenance records, QC summaries or `archive_manifest.tsv`.
