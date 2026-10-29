# GQD Dissertation — Current Scientific Status

**Controlled date:** 2026-10-28  
**Purpose:** Canonical current-state summary for scientific decisions, committee reporting, and evidence-package generation.

This file summarizes the current scientific state. Detailed execution history remains in `LAB_JOURNAL.md`; machine-level run facts remain in `run_log.tsv`; supersession history remains in `supersession_register.tsv`.

## Current scientific baseline

| Component | Current status | Authoritative evidence |
|---|---|---|
| COOH-GQD carrier | ACCEPTED / RELEASED | `B3LYP-COOH-GQD-C1-004`; C55H18O2; 75 atoms; 0 imaginary frequencies; post-DFT molecular-model/topology audit PASS |
| COOH-GQD comparison | RETAINED COMPARISON | `B3LYP-COOH-GQD-C2-005`; valid corrected true minimum |
| Historical COOH-GQD v01 | SUPERSEDED_STRUCTURAL_MODEL | Historical execution retained; not eligible for current downstream scientific use |
| Isolated drug baselines | COMPLETE / ACCEPTED | `B3LYP-ERLOTINIB-001`, `B3LYP-GEFITINIB-001`, `B3LYP-VENETOCLAX-001`, `B3LYP-ABT737-001` |

## Corrected Erlotinib adsorption status

| Pose | Run ID | QC status | Scientific disposition | Current interpretation |
|---|---|---|---|---|
| Flat | `B3LYP-COOH-GQD-ERLOTINIB-FLAT-001` | PASS; 0 imaginary frequencies | ACCEPTED_ADSORPTION_MINIMUM | Valid corrected adsorption minimum |
| Slipped | `B3LYP-COOH-GQD-ERLOTINIB-SLIPPED-001` | PASS; 0 imaginary frequencies | ACCEPTED_ADSORPTION_MINIMUM | Valid corrected adsorption minimum; lower than flat at the current B3LYP SCF/Gibbs level |
| Edge | `B3LYP-COOH-GQD-ERLOTINIB-EDGE-001` | FAILED; incomplete | RETAINED_INFRASTRUCTURE_FAILURE | No scientific conclusion on the edge hypothesis; rerun on Magnolia |

Current B3LYP values:

- Flat: SCF = -3575.30485771 Hartree; Gibbs = -3574.426086 Hartree.
- Slipped: SCF = -3575.30729853 Hartree; Gibbs = -3574.428296 Hartree.

These values do not yet constitute the final adsorption/binding-energy conclusion because the edge basin remains unresolved and the controlled BSSE/M06-2X/descriptor analyses are pending.

## Active HPC platform

Magnolia / Slurm / Gaussian 16 C.02 is validated and released for new Gaussian production.

Controlled validation:

- Run ID: `B3LYP-ERLOTINIB-MAGNOLIA-VALIDATION-001`
- Slurm job: `320607`
- Node: `node019`
- Scientific disposition: `ACCEPTED_PLATFORM_VALIDATION`
- SCF = -1317.40085224 Hartree
- ZPE = 0.420518 Hartree
- Gibbs = -1317.040903 Hartree
- optimization completed
- 0 imaginary frequencies
- QC PASS

The Magnolia result reproduced the accepted Maple Gaussian 16 C.01 Erlotinib baseline exactly to the precision reported by the project QC summaries.

Maple is closed to new Gaussian production work. Historical Maple results remain valid according to their scientific dispositions.

## Evidence-control state

- Run ledger: 25 runs at the post-Entry-061 reconciliation checkpoint; execution/QC status is separated from scientific disposition.
- Archive: 71 physical scientific files; checksum verification PASS for all 71 at the reconciliation checkpoint.
- Lab Journal: Entries 001-062; Entry 062 repairs the `PM6-ABT737-001` failed-run ledger classification.
- Historical malformed-GQD Erlotinib complexes: QUARANTINED / NOT ELIGIBLE FOR REUSE.
- Acceptance logic: governed by `docs/acceptance_gates_v2.md`.
- Execution strategy / forecast: `docs/execution_plan_v2.md`.
- Canonical Phase I workflow: `docs/computational_workflow.md` (v2.0).
- Storage / full-calculation map: `docs/storage_map.md` (v2.0).
- Publication / defense journal design: `docs/research_journal_publication_edition.md`.
- Scientific evidence index: `scientific_evidence_register.tsv`.
- Supersession/change-control index: `supersession_register.tsv`.

## Immediate authorized work

1. Execute a fresh corrected Erlotinib edge calculation on Magnolia under a new run ID. Do not infer a scientific result from the failed Maple execution.
2. Complete the Erlotinib pose comparison only after the scientifically required adsorption basins are resolved.
3. Advance accepted Erlotinib minima into binding-energy/BSSE and M06-2X validation under the canonical workflow.
4. Continue the locked Phase I order: Erlotinib → Gefitinib → Venetoclax → ABT-737.
5. Apply Acceptance Gates v2.0 to every promotion, hold, failure, supersession, and committee-facing claim.

## Committee-facing interpretation

The earlier structural criticism applied to the historical GQD lineage and was scientifically valid. That lineage is no longer used as the current carrier model. The underlying structure was rebuilt deterministically, the corrected alternatives were independently validated and recomputed, and Class-1/C1 was selected as the authoritative production baseline.

**Working completion objective:** major computational work targeted for December 2026–January 2027, subject to convergence behavior and the remaining adsorption, pH-response, docking, and molecular-dynamics workloads.
