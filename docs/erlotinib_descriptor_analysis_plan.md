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
