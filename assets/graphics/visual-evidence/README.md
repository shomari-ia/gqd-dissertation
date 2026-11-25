# GQD Visual Evidence Archive — launch collection

Shared handoff between **GQD Workflow & Journal** (scientific authority) and **Create Creative Workspace** (visual design). Initiated 2026-11-25. The archive is a source-controlled reference, not an automatic chat-to-chat sync.

## Asset register

| ID | Asset | Class / status | Source and intended use |
|---|---|---|---|
| VE-001 | [Orbital normalization chart](erlotinib_fmo_normalization.svg) | Data-derived QC figure; design draft | [Six-orbital QC TSV](../../../calculations/phase1_dft/descriptors/orbitals/results/erlotinib_fmo_cube_qc_comparison.tsv); Entry 085; slides 40–46 / validation appendix |
| VE-002 | [Geometric orbital partition](orbital_partition_concept.svg) | Concept schematic; design draft | Gate 6C; method explanation only; no computed orbital surface |
| VE-003 | [Formula and terminology library](formula_library.md) | Teaching/method reference | Methods and oral defense; check final notation against methods chapter |
| VE-004 | [Erlotinib data and figure roadmap](erlotinib_figure_roadmap.md) | Evidence-linked design queue | Energetics, contacts, charge, NCI/RDG, QTAIM, orbital QC and future spatial surfaces |
| VE-005 | Actual three-pose HOMO/LUMO surfaces | Pending source-derived rendering | Six accepted cubes on Magnolia; matched absolute isovalue, sign colors, camera and representation; no fabricated surfaces |
| VE-006 | Actual NCI scatter and isosurfaces | Pending source-derived rendering | Critic2 .dat and cubes; matched RDG isovalue and signed-density scale; no synthetic plot |

| VE-007 | [Frontier orbital spatial distribution](erlotinib_fmo_spatial_distribution.svg) | Data-derived design draft | [Accepted numerical localization table](../../../calculations/phase1_dft/descriptors/orbitals/results/erlotinib_fmo_localization_accepted_v01.tsv); SE-ERL-012 / Entry 086; 0–100% scale |
| VE-008 | [Erlotinib-domain orbital contribution](erlotinib_fmo_drug_region.svg) | Data-derived design draft | Same source; expanded 0–2% scale; geometric fraction, not charge transfer |

## Handoff rules

- Scientific claims are controlled by the lab journal, scientific evidence register and acceptance gates, not presentation styling.
- Retain exact source path, commit or analysis ID, caption, units, version, status and limitation for each asset.
- Concept illustrations must carry a visible conceptual label. Data-derived charts are not automatically committee-ready.
- Use SVG masters for editing and export PNG/PDF or slide-ready variants in Creative Workspace. Never substitute generated artwork for computed molecular geometry.
- Use graphite, charcoal, silver, cool gray and coral-peach; Georgia working typography. Scientific color conventions can override branding where necessary.
- Keep large wavefunction/cube artifacts in the scientific archive; use small derived figures and source hashes in Git.
- On each major scientific closure, add or update the corresponding visual-evidence record, then share this index in Creative Workspace. Creative edits must not overwrite raw data or alter scientific conclusions.
- Previous inline conversation graphics cannot be imported byte-for-byte here. VE-001 and VE-002 are recreated editable SVG masters based on the preceding chat; older figures are a backfill queue, not a claim of complete archival.

## Creative Workspace entry point

Read this index and [the cross-workspace handoff](../../../docs/design/visual_evidence_handoff.md). Start with VE-001 and VE-002, then develop the roadmap with source-linked figures. Gate 6C numerical localization is accepted (Entry 086); actual surfaces VE-005 and final integrated review remain pending.
