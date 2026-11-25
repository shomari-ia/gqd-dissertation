# Erlotinib Descriptor Analysis Plan — Gate 1

## Scientific purpose

The descriptor stage must explain the accepted energetic result rather than
generate an unrestricted catalog of properties.

Current energetic conclusion:

- Flat and Slipped form a near-degenerate low-energy adsorption pair.
- Slipped is nominally favored.
- Edge is substantially less favorable.

The descriptor questions are therefore:

1. What intermolecular contacts stabilize Flat and Slipped?
2. Why are Flat and Slipped energetically similar?
3. Why is Edge substantially weaker despite its short polar contact?
4. Is adsorption accompanied by reproducible drug-to-GQD charge redistribution?
5. Where are the frontier orbitals localized after adsorption?

## Authoritative source hierarchy

### Geometry descriptors

Use the accepted B3LYP-D3(BJ)/6-31G(d,p), SMD-water optimized minima:

- B3LYP-COOH-GQD-ERLOTINIB-FLAT-001
- B3LYP-COOH-GQD-ERLOTINIB-SLIPPED-001
- B3LYP-COOH-GQD-ERLOTINIB-EDGE-003

These remain the authoritative optimized geometries.

### Electronic-density descriptors

Use the accepted method-matched M06-2X/6-311+G(d,p), SMD-water
single-point wavefunctions:

- M062X-COOH-GQD-C1-001
- M062X-ERLOTINIB-001
- M062X-COOH-GQD-ERLOTINIB-FLAT-001
- M062X-COOH-GQD-ERLOTINIB-SLIPPED-001
- M062X-COOH-GQD-ERLOTINIB-EDGE-001

The existing binary checkpoints have been converted with Gaussian formchk
to formatted checkpoints for post-processing. No new SCF calculation is
required for the core descriptor package.

## Core descriptor package

### Tier 1 — accepted existing evidence / direct post-processing

1. Interfragment and pose geometry
   - minimum heavy-atom distance
   - contact counts
   - GQD/drug plane relationship
   - surface separation
   - targeted polar-contact geometry

2. Frontier orbital energies
   - HOMO
   - LUMO
   - HOMO-LUMO gap

3. Frontier orbital spatial distributions
   - HOMO cube
   - LUMO cube
   - qualitative fragment localization

4. Charge redistribution
   - Mulliken fragment charges retained only as preliminary evidence
   - Hirshfeld and Hirshfeld-I fragment charges used for controlled interpretation

5. Noncovalent interaction analysis
   - NCI/RDG restricted to GQD-drug interfragment regions
   - comparison of Flat, Slipped, and Edge

### Tier 2 — conditional

6. QTAIM
   - perform after NCI/RDG validation
   - focus on interfragment bond critical points and the Edge polar contact
   - do not interpret absence of a bond critical point as absence of interaction

## Deferred analyses

The following are not authorized at Gate 1:

- Fukui indices
- TDDFT/UV-Vis
- difference-density calculations requiring new fragment single points
- ELF
- DOS

They may be added only if a specific dissertation question requires them.

## Gate-1 findings

M06-2X HOMO-LUMO gaps:

- C1: 4.1293 eV
- Erlotinib: 6.2646 eV
- Flat: 4.1168 eV
- Slipped: 4.1261 eV
- Edge: 4.1685 eV

Preliminary Mulliken fragment charges:

- Flat: GQD -0.6487 e; Erlotinib +0.6487 e
- Slipped: GQD -0.6351 e; Erlotinib +0.6351 e
- Edge: GQD +0.0063 e; Erlotinib -0.0063 e

These Mulliken values are provisional and are not final charge-transfer claims.

Accepted-geometry contact metrics:

- Flat: heavy minimum 3.2568 Å; principal-plane angle 8.733°;
  129 heavy-atom pairs <= 4.0 Å.
- Slipped: heavy minimum 3.2757 Å; principal-plane angle 7.974°;
  134 heavy-atom pairs <= 4.0 Å.
- Edge: heavy minimum 2.6104 Å; principal-plane angle 32.175°;
  8 heavy-atom pairs <= 4.0 Å.

Edge also contains H75-N81 = 1.5689 Å and O74-N81 = 2.6104 Å.
Hydrogen-bond assignment is withheld pending donor-parent and angular validation.

## Gate decision

PASS.

No new Gaussian electronic-structure calculation is required for the
core Erlotinib descriptor package.

Next controlled stage:

- validate the Edge polar contact;
- establish Critic2 as the real-space analysis tool;
- calculate Hirshfeld/Hirshfeld-I fragment charges;
- generate interfragment NCI/RDG analyses;
- generate HOMO/LUMO spatial surfaces;
- evaluate targeted QTAIM only after the real-space workflow is validated.


## Gate 2 — real-space charge-partition closure

Status: PASS.

Critic2 analytical-wavefunction post-processing was validated on the accepted
Flat M06-2X formatted checkpoint and then applied without methodological change
to Slipped and Edge. All three analyses completed with zero Critic2 warnings,
zero comments, and Hirshfeld-I convergence in 45 iterations.

Accepted fragment charges (GQD / Erlotinib, e):

- Flat:
  - Hirshfeld: +0.047092 / -0.047107
  - Hirshfeld-I: +0.020731 / -0.020746
- Slipped:
  - Hirshfeld: +0.054966 / -0.054821
  - Hirshfeld-I: +0.031690 / -0.031545
- Edge:
  - Hirshfeld: -0.221890 / +0.222348
  - Hirshfeld-I: -0.170826 / +0.171283

Interpretation:

- Flat and Slipped show only small apparent GQD-to-Erlotinib redistribution.
- Edge shows substantially larger apparent Erlotinib-to-GQD redistribution.
- The preliminary Mulliken pattern from Gate 1 is not reproduced and is
  superseded for charge-transfer interpretation.
- Net charge transfer therefore does not explain why Flat and Slipped are the
  preferred adsorption pair.
- The combined energetic, geometric, and charge-partition evidence supports
  testing distributed interfragment pi/dispersion interactions as the principal
  stabilizing feature of Flat and Slipped.

The initial Hirshfeld-I zero-charge TSVs were a parser artifact caused by reading
the Z column instead of N_HI. Raw Critic2 results were valid and were not rerun.
The corrected parser uses table-specific column mappings and verifies
q_HI = Z - N_HI atom by atom.

Next controlled stage:

1. Validate one interfragment NCI/RDG analysis using the accepted Flat
   M06-2X wavefunction.
2. Apply the identical validated NCI/RDG workflow to Slipped and Edge.
3. Compare the spatial extent and sign(lambda2)rho character of the
   interfragment interaction domains.
4. Generate HOMO/LUMO spatial surfaces.
5. Use targeted QTAIM only after NCI/RDG validation.


## Gate 3 — Flat NCI/RDG pilot

Status: PASS.

The Flat interfragment NCI/RDG pilot validated the Critic2 workflow using the
accepted analytical M06-2X wavefunction and explicit 75-atom GQD / 52-atom
Erlotinib fragments.

Locked parameters:

- CUTOFFS 0.2 2.0
- CUTPLOT 0.05 0.5
- RTHRES 2.0 A
- RHOPARAM 0.95
- RHOPARAM2 0.75
- INCREMENTS 0.10 0.10 0.10 A
- NOCHK

Flat pilot QC:

- Critic2: 0 warnings, 0 comments
- grid: 206 x 181 x 101
- .dat rows: 119493
- sign(lambda2)rho: -0.028380452 to +0.02309261
- RDG: 0.012962228 to 1.9999521
- RDG <= 0.5 points: 10831
- negative signed-density low-RDG points: 3280
- positive signed-density low-RDG points: 7551
- density/RDG/promolecular-density cubes: 127 atoms and identical grids
- expected NCI artifacts: PASS

Interpretive constraint:

The NCI grid-point counts are spatial samples, not interaction energies.
Negative sign(lambda2)rho identifies attractive regions, positive values
repulsive/steric regions, and values close to zero weak/dispersive regions.
Comparative mechanistic conclusions require identical Slipped and Edge analyses.

Advancement:

- RELEASE Slipped and Edge NCI/RDG using the locked Flat-pilot parameters.
- HOLD final NCI interpretation until all three poses pass quantitative QC.
- HOLD targeted QTAIM until the three-pose NCI comparison is complete.


## Gate 4 — three-pose NCI/RDG comparison

Status: PASS.

Identical fragment-restricted NCI/RDG settings were applied to Flat, Slipped,
and Edge. All analyses passed quantitative QC.

Grid-normalized low-RDG fractions:

- Flat: 0.2876%
- Slipped: 0.2760%
- Edge: 0.002445%

The Flat and Slipped low-RDG interaction domains are therefore approximately
118x and 113x more spatially extensive than the Edge domain under the same
spacing and thresholds.

The minimum sign(lambda2)rho values are:

- Flat: -0.02838
- Slipped: -0.02893
- Edge: -0.19803

Thus Edge contains a much stronger localized attractive-density feature but a
far smaller overall intermolecular interaction domain.

Accepted interpretation:

- Flat and Slipped: broad, distributed surface interaction consistent with
  extensive pi/dispersion contact.
- Edge: localized strong polar interaction consistent with the O-H...N
  hydrogen-bond candidate, but insufficient spatial contact to compete
  energetically with Flat/Slipped.

NCI point counts are not treated as energies.

Next controlled stages:

1. targeted QTAIM of the Edge O74-H75...N81 region;
2. HOMO/LUMO spatial localization for the accepted complexes;
3. final integrated Erlotinib descriptor-package closure.


## Gate 5 — targeted Edge QTAIM

Status: PASS.

The accepted Edge M06-2X wavefunction contains a `(3,-1)` bond critical point
directly connecting H75 and N81 (CP 275).

Target BCP properties:

- H75-to-BCP distance: 0.4610 A
- N81-to-BCP distance: 1.1080 A
- H75-BCP-N81 angle: 179.79 degrees
- rho_BCP: 0.0740003548 a.u.
- Laplacian: +0.0855291841 a.u.
- ellipticity: 0.0442019362

Accepted interpretation:

- the H75...N81 BCP provides direct topological support for the localized
  O-H...N interaction identified by geometry and NCI/RDG;
- the positive Laplacian and rho<0.1 a.u. are consistent with closed-shell /
  noncovalent QTAIM character;
- no stronger covalency classification is made without the local total energy
  density H(r).

Parser-control note:

The earlier v01-v03 target tables are superseded parser artifacts. Critic2's
native bond-table format separates each endpoint label from its parenthesized
atom index. The corrected parser resolves CP 275 as H75 (75) -- N81 (81)
without rerunning Critic2.

Next controlled stage:

1. generate HOMO and LUMO cube files from the accepted M06-2X formatted
   checkpoints;
2. evaluate orbital localization on GQD versus Erlotinib for Flat, Slipped,
   and Edge, with isolated C1/Erlotinib available as references;
3. integrate geometry, energetics, charge, NCI/RDG, QTAIM, and orbital
   localization into the final Erlotinib descriptor-package conclusion.


## Gate 6A — Flat frontier-orbital cube pilot
Status: PASS (generation and grid QC; localization pending).

Job 356034 generated HOMO 286 and LUMO 287 on matched 99 x 89 x 58 grids, 127 atoms, 511038 samples each. Corrected MO-header parser at e4ed8315ef116df8df577527db434f58ca6053f2 validated the existing cubes. Approximate squared-amplitude integrals: HOMO 1.00022131, LUMO 1.00028826. See Entry 084 and flat_fmo_pilot_qc_v02.tsv.

RELEASE Slipped/Edge production cube generation using unchanged cubegen settings and corrected analyzer. Verify source electron counts, orbital indices, hashes, matching within-pose grids and normalization. Automatic grid dimensions may differ between poses. HOLD fragment localization and final descriptor closure until spatial comparison; grid integrals are QC, not fragment populations.


## Gate 6B — Three-pose frontier-orbital cube generation
Status: PASS. Slipped/Edge job 373879/373880 completed with valid provenance and matching hashes; all six cubes pass QC with normalization within 0.05% of unity. See Entry 085 and erlotinib_fmo_cube_qc_comparison.tsv. Different automatic voxel volumes are expected.

## Gate 6C — Orbital spatial localization
Status: RELEASED, results pending. Integrate squared orbital amplitudes on existing grids using nearest-nucleus GQD/drug spatial domains, with all-atom and heavy-atom partitions for sensitivity. Treat as a geometric localization proxy, not an atomic-orbital population or charge-transfer measure. Compare with matched-isovalue molecular surfaces before interpretation. No new Gaussian runs.
