# GQD Dissertation — Current Scientific Status

**Controlled date:** 2026-11-13

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
| Edge | `B3LYP-COOH-GQD-ERLOTINIB-EDGE-003` | PASS; 0 imaginary frequencies | ACCEPTED_ADSORPTION_MINIMUM | Valid corrected adsorption minimum; Edge-001/002 retained separately as infrastructure-failure evidence |

Current B3LYP values:

- Flat: SCF = -3575.30485771 Hartree; Gibbs = -3574.426086 Hartree.
- Slipped: SCF = -3575.30729853 Hartree; Gibbs = -3574.428296 Hartree.
- Edge: SCF = -3575.25578701 Hartree; ZPE = 0.969539 Hartree; Gibbs = -3574.387683 Hartree.

All three required corrected Erlotinib adsorption basins are now resolved as true minima. At the current B3LYP-D3(BJ)/6-31G(d,p), SMD-water level, slipped is lower than flat by approximately 1.532 kcal/mol electronically and 1.387 kcal/mol in Gibbs free energy. Edge is higher than slipped by approximately 32.324 kcal/mol electronically and 25.485 kcal/mol in Gibbs free energy.

These are relative total-system energies for equal-composition adsorption minima. The controlled BSSE gate is now closed; M06-2X validation and planned descriptor analyses remain pending before the final Phase I Erlotinib conclusion.

## Erlotinib BSSE energetic validation

Gas-phase Boys-Bernardi Counterpoise calculations were performed at B3LYP-D3(BJ)/6-31G(d,p) on the frozen accepted SMD-water optimized geometries because Gaussian 16 does not permit automated Counterpoise with SCRF.

The primary adsorption model remains SMD water. The reported corrected estimate is therefore explicitly:

`E_bind,SMD+BSSE = E_bind,raw,SMD + BSSE_gas`

| Pose | Raw SMD binding (kcal/mol) | Gas BSSE (kcal/mol) | SMD + gas-BSSE estimate (kcal/mol) | Δ vs lowest |
|---|---:|---:|---:|---:|
| Slipped | -45.712 | +11.572 | -34.140 | 0.000 |
| Flat | -44.180 | +11.026 | -33.154 | +0.986 |
| Edge | -13.388 | +3.316 | -10.072 | +24.068 |

The BSSE correction preserves Slipped as the nominal lowest-energy pose but reduces the Slipped-versus-Flat separation to 0.986 kcal/mol. The independent gas-phase Counterpoise corrected interaction values are -34.71 kcal/mol for Slipped and -34.63 kcal/mol for Flat, a difference of only 0.08 kcal/mol. Accordingly, Flat and Slipped are treated as a near-degenerate low-energy adsorption pair. Edge remains clearly less favorable.

## Erlotinib M06-2X validation

Independent higher-level single-point validation was completed at M06-2X/6-311+G(d,p), SMD water on the accepted B3LYP geometries.

Method-matched electronic reference energies:

- C1 COOH-GQD: -2257.21308993 Ha.
- Erlotinib: -1317.09055446 Ha.

| Pose | M06-2X electronic binding (kcal/mol) | Δ vs Slipped (kcal/mol) |
|---|---:|---:|
| Slipped | -37.074 | 0.000 |
| Flat | -36.029 | +1.044 |
| Edge | -8.335 | +28.739 |

M06-2X independently reproduces the B3LYP+BSSE interpretation. Flat and Slipped form a near-degenerate low-energy adsorption pair, with Slipped nominally favored by approximately 1 kcal/mol. Edge remains substantially less favorable.

These are electronic single-point binding energies evaluated on accepted B3LYP geometries. They are not M06-2X Gibbs free energies and are not M06-2X BSSE-corrected values.


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

- Run ledger: 33 runs at the Erlotinib BSSE closure; execution/QC status remains separated from scientific disposition.
- Archive: 87 physical scientific files inventoried in `archive_manifest.tsv`; checksum verification PASS at the Erlotinib BSSE closure.
- Lab Journal: Entries 001-074; Entry 074 records the accepted Erlotinib BSSE energetic validation.
- Historical malformed-GQD Erlotinib complexes: QUARANTINED / NOT ELIGIBLE FOR REUSE.
- Acceptance logic: governed by `docs/acceptance_gates_v2.md`.
- Execution strategy / forecast: `docs/execution_plan_v2.md`.
- Canonical Phase I workflow: `docs/computational_workflow.md` (v2.0).
- Storage / full-calculation map: `docs/storage_map.md` (v2.0).
- Publication / defense journal design: `docs/research_journal_publication_edition.md`.
- Scientific evidence index: `scientific_evidence_register.tsv`.
- Supersession/change-control index: `supersession_register.tsv`.

## Immediate authorized work

1. Complete the Erlotinib flat/slipped/edge pose comparison using the three accepted adsorption minima.
2. Advance the accepted Erlotinib minima into controlled binding-energy/BSSE and M06-2X validation under the canonical workflow.
3. Record descriptor/interaction analyses required for the final Erlotinib adsorption conclusion.
4. Continue the locked Phase I sequence with Gefitinib after the Erlotinib validation gates are closed.
5. Apply Acceptance Gates v2.0 to every promotion, hold, failure, supersession, and committee-facing claim.

## Committee-facing interpretation

The earlier structural criticism applied to the historical GQD lineage and was scientifically valid. That lineage is no longer used as the current carrier model. The underlying structure was rebuilt deterministically, the corrected alternatives were independently validated and recomputed, and Class-1/C1 was selected as the authoritative production baseline.

**Working completion objective:** major computational work targeted for December 2026–January 2027, subject to convergence behavior and the remaining adsorption, pH-response, docking, and molecular-dynamics workloads.
