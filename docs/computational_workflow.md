# Computational Workflow — Phase I

Written to the level Chapter 2 needs. Phases II and III get their own sections
of this file when they begin; do not scaffold them now.

Every step states its input, its gate, and what happens when the gate fails.
A result advances only when its gate passes — not because an output file exists.

---

## Step 1 — Structure preparation

| | |
|---|---|
| **Input** | PubChem SDFs (CIDs in `config/systems.yml`) |
| **Tools** | Avogadro 1.2 (COOH addition, MMFF94 clean-up), Open Babel (format conversion) |
| **Output** | `structures/prepared/*.mol`, `calculations/phase1_dft/pm6/inputs/*.com` |
| **Gate** | COOH carbon has exactly three connections: ring bond, `=O`, `–OH`. Atom count is 75 for COOH-GQD. Charge 0, multiplicity 1 on every input. |
| **On failure** | Re-open in Avogadro, fix connectivity, re-optimize with MMFF94. Do not proceed with a dangling hydrogen — it produces a valid-looking calculation of the wrong molecule. |

Structures are prepared on Windows and committed as text. Nothing here needs
the cluster.

---

## Step 2 — PM6 pre-optimization

| | |
|---|---|
| **Input** | `pm6/inputs/<system>_pm6_opt_v01.com`, `%chk=archive/chk/<system>_pm6_opt_v01.chk` |
| **Resources** | 8 cores, 8 GB, ≤4 h |
| **Output** | `archive/logs/<system>_pm6_opt_v01.log`, checkpoint in `archive/chk/` |
| **Gate** | `scripts/verify_gaussian.sh` exits 0: normal termination **and** "Optimization completed". |
| **On failure** | Inspect the last geometry in the log. Most PM6 failures on these systems are bad starting connectivity — go back to Step 1 rather than adding convergence keywords. |

The checkpoint is the deliverable here, not the energy. PM6 energies are
recorded for completeness but are **not comparable** to DFT energies and never
enter a binding-energy expression.

---

## Step 3 — B3LYP optimization + frequencies

| | |
|---|---|
| **Input** | `b3lyp/inputs/<system>_b3lyp_optfreq_v01.com` with `%oldchk=` PM6 checkpoint and `geom=check` |
| **Level** | B3LYP-D3(BJ)/6-31G(d,p), SMD water |
| **Resources** | 16 cores, 32 GB, one node |
| **Output** | optimized geometry, SCF energy, thermal free-energy correction |
| **Gate** | normal termination, optimization completed, **zero imaginary frequencies** |
| **On failure — imaginary mode** | Displace the geometry along the imaginary mode and re-optimize as a new `run_id`. Record the original as `FAILED` with the mode frequency in `run_notes.tsv`; never delete it. |
| **On failure — walltime** | Resubmit with `geom=check guess=read` from the *same-level* checkpoint (valid here: same method, same basis). Expected for venetoclax and ABT-737. |
| **On failure — SCF convergence** | `scf=xqc`, or `scf=(maxcycle=256)`. New `run_id`; note the reason. |

Submission order is deliberate: COOH-GQD first as the pilot, then erlotinib and
gefitinib, then venetoclax and ABT-737 last.

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
