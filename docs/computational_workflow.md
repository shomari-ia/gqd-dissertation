# Computational Workflow — Phase I

Written to the level Chapter 2 needs. Phases II and III get their own sections
of this file when they begin; do not scaffold them now.

Every step states its input, its gate, and what happens when the gate fails.
A result advances only when its gate passes — not because an output file exists.

---

## Step 1 — Structure preparation

| | |
|---|---|
| **Input** | Deterministically rebuilt circumcoronene parent for COOH-GQD; PubChem SDFs for the locked drug set |
| **Tools** | `scripts/build_circumcoronene.py`, `scripts/hydrogenate_circumcoronene.py`, `scripts/functionalize_circumcoronene_cooh.py` for corrected GQD construction; Open Babel for documented drug preparation |
| **Output** | validated text structures in `structures/prepared/`; Gaussian inputs in `calculations/phase1_dft/pm6/inputs/` |
| **Gate** | For COOH-GQD: C55H18O2, 75 atoms, intact C54 circumcoronene scaffold with 72 C-C edges, 18 degree-2 carbons, 36 degree-3 carbons, 19 six-membered cycles, exactly one COOH substituent, standardized C72/O73/O74/H75 functional-group mapping, charge 0, multiplicity 1. |
| **On failure** | Return to the deterministic preparation step and identify the construction defect. Do not hand-repair a malformed GQD geometry or advance a structure merely because a quantum-chemistry input can be generated. |

Structures are prepared using the appropriate reproducible preparation route.

Corrected COOH-GQD preparation is deterministic and script-based. The
historical v01 GQD lineage is retained for provenance but is
not reused as the corrected structural baseline.

PubChem drug preparation uses the documented Open Babel/MMFF94 route.

Raw PubChem files remain immutable.
Prepared structures are independently validated and committed as text before
Gaussian work.

---

## Step 2 — PM6 pre-optimization

| | |
|---|---|
| **Input** | `pm6/inputs/<system>_pm6_opt_<version>.com`; corrected COOH-GQD symmetry-class candidates use the new v02 lineage |
| **Resources** | 8 cores, 8 GB, ≤4 h |
| **Output** | run-specific PM6 log and checkpoint in `archive/logs/` and `archive/chk/` |
| **Gate** | `scripts/verify_gaussian.sh` exits 0 with normal termination and "Optimization completed". For corrected COOH-GQD, the final PM6 geometry must additionally pass an independent topology/geometry audit before B3LYP advancement. |
| **On failure** | Inspect the final geometry and determine whether the problem is convergence or molecular-model integrity. A topology/connectivity failure returns to Step 1; it is not corrected by adding convergence keywords. |

For corrected COOH-GQD, the post-PM6 audit must confirm the intended
C55H18O2 composition, intact C54 circumcoronene scaffold, single COOH
attachment, and absence of unintended bonding or severe scaffold distortion.

The checkpoint is the deliverable here, not the energy. PM6 energies are
recorded for completeness but are **not comparable** to DFT energies and never
enter a binding-energy expression.

---

## Step 3 — B3LYP optimization + frequencies

| | |
|---|---|
| **Input** | `b3lyp/inputs/<system>_b3lyp_optfreq_<version>.com` with `%oldchk=` from the corresponding PM6 checkpoint and `geom=check`; corrected COOH-GQD symmetry-class candidates use the new v02 lineage |
| **Level** | B3LYP-D3(BJ)/6-31G(d,p), SMD water |
| **Resources** | 16 cores, 32 GB, one node |
| **Output** | optimized geometry, SCF energy, thermal free-energy correction |
| **Gate** | normal termination, optimization completed, **zero imaginary frequencies**. Corrected COOH-GQD candidates must also pass a post-DFT molecular-model audit before scientific acceptance. |
| **On failure — imaginary mode** | Displace the geometry along the imaginary mode and re-optimize as a new `run_id`. Record the original as `FAILED` with the mode frequency in `run_notes.tsv`; never delete it. |
| **On failure — walltime** | Resubmit with `geom=check guess=read` from the *same-level* checkpoint (valid here: same method, same basis). Expected for venetoclax and ABT-737. |
| **On failure — SCF convergence** | `scf=xqc`, or `scf=(maxcycle=256)`. New `run_id`; note the reason. |

The corrected isolated COOH-GQD rebuild is evaluated as a controlled comparison
between the validated Class-1 and Class-2 symmetry representatives. Neither
candidate becomes the authoritative GQD baseline until its PM6 and B3LYP gates
pass and the two corrected candidates have been compared.

The previously accepted isolated drug baselines remain valid and are not
recomputed solely because the GQD structural model was rebuilt.

**Do not carry `guess=read` across a method change.** A PM6 wavefunction is not
a valid starting guess for a DFT calculation, and reading one across differing
basis sets is invalid regardless of method. `geom=check` alone is correct for
every stage transition in this project except a same-level restart.

---

## Step 4 — Complex construction and optimization

| | |
|---|---|
| **Input** | optimized GQD + optimized drug, assembled in three poses (flat, slipped, edge) |
| **Level** | same as Step 3 — this is what makes the energies subtractable |
| **Output** | three optimized complexes per drug; lowest-energy converged pose retained |
| **Gate** | each retained pose passes the Step 3 gate. All three poses are logged even though one is retained. |
| **On failure** | If two poses converge to the same structure, record it — pose degeneracy is a result, not a problem. |

Twelve complex optimizations (4 drugs × 3 poses) plus restarts. This is the bulk
of the phase's compute.

---

## Step 5 — Binding energies

E_bind = E_complex − (E_GQD + E_drug), negative meaning favorable.

| | |
|---|---|
| **BSSE** | counterpoise, one Gaussian job with `Counterpoise=2` and fragment labels; charge/mult line `0 1 0 1 0 1` |
| **Validation** | M06-2X/6-311+G(d,p)/SMD single point on the B3LYP geometry — **no** `EmpiricalDispersion` keyword (M06-2X includes it) |
| **Gate** | both numbers exist for every pair; sign and magnitude physically sensible (dispersion-dominated π-stacking on this system should be tens of kcal/mol, not hundreds) |
| **Reported in** | kcal/mol (Hartree × 627.5095) |

Comparability check before subtracting any two energies: same functional, same
basis, same solvent, same charge state. If any differ, the difference is
meaningless.

---

## Step 6 — Electronic-structure analysis

Generate `output=wfx` from the optimized complex, then extract with Multiwfn
and NCIPLOT: HOMO–LUMO gaps (eV), QTAIM bond critical points between fragments,
NCI/RDG isosurfaces, ELF, DOS, condensed Fukui indices, TDDFT UV-Vis.

| | |
|---|---|
| **Gate** | the `.wfx` loads in Multiwfn and the atom count matches the complex |
| **Output** | descriptor values into `results/tables/`, figures into `results/figures/` |
| **Rule** | every figure is regenerated by a script in `scripts/analysis/`, never edited by hand into its final form |

---

## Step 7 — Descriptor table

One row per drug–GQD pair: BSSE-corrected E_bind, M06-2X validation E_bind,
HOMO–LUMO gap of complex vs. isolated species, net charge transfer, dominant
NCI interaction type.

**Gate:** every cell traces to a `run_id` in `run_log.tsv`. A number with no
`run_id` does not go in the table.
