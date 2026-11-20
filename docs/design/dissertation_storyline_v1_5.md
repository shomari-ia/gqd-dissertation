# GQD Dissertation — Full Research Story v1.5 (56-slide Google Slides working edition)

**Visual language:** Graphite / silver / luminous coral-peach (`#FF8975`); no maroon/dark-red accents.  
**Typography:** Georgia used as editable working type; Sage and Mumbai remain display-font candidates pending exact family and licensing.  
**Authority:** Scientific claims are governed by `SCIENTIFIC_STATUS.md`, `docs/scientific_scope.md`, `docs/acceptance_gates_v2.md`, `docs/computational_workflow.md`, and `docs/execution_plan_v2.md`.  
**Current scientific-status basis:** Controlled 2026-11-13. Refresh before committee circulation.

## Narrative logic

**Why this research exists → where the intellectual training and infrastructure come from → what model was selected and why → which computational tools and gates are used → what has been demonstrated → what remains planned → what the work contributes.**

### Act I — Institution, problem and interdisciplinary research (slides 1–11)

1. Formal title
2. One Scientific Question, Several Scales
3. Jackson State University: The Setting
4. CDSE Is an Interdisciplinary PhD
5. Where Bioinformatics Enters the Story
6. ICN: Nanoscience and Responsibility
7. DAIR³: Rigor Is a Method
8. The Challenge: Anticancer Therapeutics
9. Drug Discovery Is Not Drug Delivery
10. Drug Delivery Is More Than Drug Potency
11. One Project, Four Scientific Languages

### Act II — Quantum-mechanical and molecular model rationale (slides 12–24)

12. What Quantum Mechanics Adds
13. Why a Finite Circumcoronene GQD?
14. Why a Carboxyl-Functionalized GQD?
15. GQD Is Not a Generic GOQD Model
16. A Carrier with a Defined Identity
17. **Accepted C1 Gaussian geometry: source-derived XY projection**
18. Why Protonation Can Change the Story
19. Four Drugs / Two Biological Target Classes
20. Why Four Anticancer Compounds?
21. Erlotinib and Gefitinib
22. Venetoclax and ABT-737
23. EGFR and Bcl-2 Are Not the Same Target
24. Three Scientific Questions Across Scales

### Act III — Computational design, tools, HPC and reproducibility (slides 25–36)

25. Research Architecture
26. Methodological Framework
27. Tools Turn a Model Into Evidence
28. MCSR and Magnolia: Where DFT Runs
29. Python Is the Workflow's Connective Tissue
30. Where Statistics and R Can Contribute
31. Reproducibility Is a Chain of Custody
32. Commands Behind the Scientific Record
33. An Execution Plan, Not a Date Promise
34. Construct → Audit → Optimize → Re-Audit
35. Three Starting-Orientation Families
36. Scientific Evidence & Acceptance

### Act IV — Current verified Phase I evidence (slides 37–46)

37. The Correction Was Part of the Scientific Progress
38. All Four Isolated Drugs: Accepted
39. What Can We Claim at Each Scale?
40. Three Corrected Erlotinib Adsorption Minima Accepted
41. Slipped and Flat Are Close at the B3LYP Level
42. Counterpoise Adjustment Narrows the Difference
43. M06-2X Reproduces the Main Pose Ordering
44. Energetics Need Scientific Context
45. From a Successful Job to an Accepted Result
46. Magnolia Validates the Production Environment

### Act V — Explicitly planned phases, research outlook and defense (slides 47–56)

47. What a pH-Response Result Must Show
48. Modeling pH-Dependent Interactions
49. Docking Must Be Validated Before Use
50. Molecular Dynamics Tests Behavior in Time
51. From Released Drug to Target-Relevant Modeling
52. From Chemical Schematics to Real Structures (figure production roadmap)
53. What the Evidence Supports—and What Comes Next
54. What This Dissertation Can Contribute
55. The Future Work Is Explicitly Gated
56. Explore the Evidence / Q&A

## Scientific figure provenance

The new Slide 17 shows the corrected Class-1/C1 carrier from accepted Gaussian log `cooh_gqd_class1_c1_b3lyp_optfreq_v03.log`, run `B3LYP-COOH-GQD-C1-004`. The last `Input orientation` block has **75 atoms (55 carbon, 18 hydrogen, 2 oxygen)**. The rendering is an **XY projection of the actual output coordinates**, with visualization-only bonds inferred by plausible interatomic distances. The carbon scaffold visualization includes 72 inferred C–C bonds. The independent post-DFT topology audit, frequency results and scientific disposition—not the graphic alone—control acceptance. The figure does not depict a drug adsorption pose.

The figure is sourced from a read-only Google Drive copy of the Gaussian log, linked in the slide's presenter notes. Additional source-derived figures for drugs, Erlotinib complexes, and validated receptor structures remain to be produced; no unverified schematic is labeled a Gaussian result.

## External institutional references

- [JSU CDSE program](https://www.jsums.edu/gip/cdese/) — program and concentrations.
- [JSU CSET](https://www.jsums.edu/cset2/) — institutional college context.
- [JSU computational chemistry / ICN](https://www.jsucompchem.org/others/icn) — center background.
- [DAIR³](https://midas.umich.edu/training/dair-3/) — institutional collaboration in rigor/reproducibility; no claim of personal participation.
- [MCSR Magnolia](https://mcsr.olemiss.edu/supercomputers/magnolia/) — HPC setting.

## Editorial and scientific boundaries

- The publicly verified academic unit is the interdisciplinary CDSE PhD within CSET; do not invent an official departmental label “Department of Data Science.”
- R is an optional future statistical/visual analysis pathway, not documented as a completed production analysis.
- Phase II and III slides are **planned-study and proposed-result structures**, not completed calculation findings.
- DFT energies are defined by method, basis, solvent, geometry, reference, and correction; no clinical benefit is claimed.
- Presenter notes have been added to all 29 new story slides, and original technical slide notes are preserved from v1.4.
- All 56 slides and numeric footers have been verified in the native Google Slides working edition.
