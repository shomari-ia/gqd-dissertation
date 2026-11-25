# Erlotinib scientific figure roadmap

Working design backlog; current source basis: journal through Entry 085, evidence SE-ERL-007 through SE-ERL-011 and accepted orbital QC. The journal and underlying accepted tables take precedence over this design brief.

| Panel | Figure direction | Evidence basis / caution |
|---|---|---|
| E01 | Three-pose adsorption energy comparison | B3LYP+gas-phase BSSE correction (SE-ERL-007) and M06-2X SP (SE-ERL-008), distinct series, kcal/mol, electronic energies not Gibbs |
| E02 | Pose contact geometry | Accepted Flat/Slipped/Edge geometry; 129/134/8 heavy contacts <=4 A, near-parallel vs edge; count not energy |
| E03 | Fragment charge redistribution | [Hirshfeld comparison](../../../calculations/phase1_dft/descriptors/results/erlotinib_hirshfeld_comparison.tsv), SE-ERL-009; distinguish Hirshfeld and Hirshfeld-I, avoid superseded Mulliken |
| E04 | NCI/RDG domains | [Three-pose NCI table](../../../calculations/phase1_dft/descriptors/critic2/nci/results/erlotinib_nci_three_pose_comparison.tsv), SE-ERL-010; 10831/11397/200 low-RDG samples at identical spacing, not energies; full-box normalization depends on bounding box; spatial location of strongest feature requires actual surfaces |
| E05 | QTAIM H75...N81 | [Accepted v04](../../../calculations/phase1_dft/descriptors/critic2/qtaim/results/edge_oh_n_target_v04.tsv), SE-ERL-011; CP 275, rho 0.0740003548, Laplacian +0.0855291841, ellipticity 0.0442019362; no pure-electrostatic or quantitative strength claim |
| E06 | Frontier orbital numerical QC | VE-001, six cubes, all deviations <0.05%; not evidence of fragment localization |
| E07 | Orbital localization method | VE-002 and F-002; results pending |
| E08 | Actual orbital surfaces | VE-005; use accepted cubes, matched absolute isovalues, both phases and consistent camera; assess localization only after analysis |
| E09 | Integrated mechanistic figure | Broad Flat/Slipped surface interactions vs localized Edge contact; evidence synthesis, not an energy decomposition or claim of experimental delivery |

Prioritize actual molecular imagery before final presentation. Preserve paired light and dark variants, source references, accessible legends, editable vectors and separate export masters. No fabricated molecular results.
