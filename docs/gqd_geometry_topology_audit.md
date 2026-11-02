# GQD Geometry / Topology Audit

**Canonical tool:** `scripts/audit_gqd_geometry_topology.py`  
**Established:** 2026-11-02

## Purpose

This script consolidates the geometry/topology checks that were previously documented across the Lab Journal and deterministic GQD-construction scripts into one standalone audit tool.

It independently audits the monocarboxylated circumcoronene GQD model from:

- repository-controlled XYZ coordinates; or
- Gaussian `.log` / `.out` files parsed with cclib.

The tool does **not** use Open Babel, RDKit, or NetworkX for the GQD structural decision.

## What it calculates

For the default project mapping:

- first 75 atoms = GQD fragment;
- first 54 GQD atoms = C1-C54 graphene scaffold.

The audit reports:

- full-input atom count and formula;
- GQD-fragment formula;
- distance-derived total GQD bond count;
- scaffold C-C edge count;
- scaffold degree distribution;
- graph connectivity;
- cycle rank;
- six-membered-cycle count;
- best-fit-plane RMS deviation;
- best-fit-plane span;
- maximum absolute plane deviation;
- COOH attachment and O-H connectivity;
- individual topology / geometry / formula / COOH gates;
- final `GQD MODEL AUDIT = PASS|FAIL`.

Optional outputs:

- JSON report;
- inferred bond-list TSV;
- reproducible side-profile figure.

## Reference circumcoronene invariants

The corrected C54 circumcoronene scaffold is expected to satisfy:

- 54 scaffold carbons;
- 72 scaffold C-C edges;
- 18 degree-2 carbons;
- 36 degree-3 carbons;
- connected graph;
- cycle rank = 19;
- 19 six-membered cycles.

The isolated monocarboxylated GQD is expected to be:

- C55H18O2;
- 75 atoms;
- 93 inferred molecular bonds under the project distance-derived bond rule;
- one COOH group attached to one scaffold carbon.

## Planarity screening

The tool computes a least-squares best-fit plane to C1-C54 using singular-value decomposition.

Current configurable project screening defaults:

- scaffold plane RMS <= 0.25 A;
- scaffold plane span <= 0.75 A.

These are reproducibility screening limits for severe deformation, not universal graphene constants. They are intentionally much looser than the accepted C1 baseline and are exposed as command-line options.

Accepted C1 reference:

- RMS = 0.008792 A;
- span = 0.047391 A;
- max |deviation| = 0.027413 A.

Historical final B3LYP XYZ reference:

- RMS = 1.688714 A;
- span = 6.105481 A;
- max |deviation| = 3.849276 A.

## Example commands

### Historical final B3LYP XYZ

```bash
python scripts/audit_gqd_geometry_topology.py \
  structures/accepted/cooh_gqd_b3lyp_accepted.xyz \
  --json results/tables/sep001_historical_gqd_audit.json \
  --bonds-tsv results/tables/sep001_historical_gqd_bonds.tsv \
  --figure results/figures/sep001_historical_gqd_side_profile.png \
  --figure-title "Historical COOH-GQD v01 — side-profile audit"
```

Expected scientific result: **FAIL**.

The repository-controlled final historical XYZ retains 72 distance-derived scaffold edges but has only 16 six-membered scaffold cycles under the canonical audit and is severely nonplanar. This is sufficient to fail the intended circumcoronene model.

### Corrected authoritative C1 XYZ

```bash
python scripts/audit_gqd_geometry_topology.py \
  structures/optimized/cooh_gqd_class1_c1_b3lyp_optfreq_v03.xyz \
  --json results/tables/sep001_corrected_c1_gqd_audit.json \
  --bonds-tsv results/tables/sep001_corrected_c1_gqd_bonds.tsv \
  --figure results/figures/sep001_corrected_c1_gqd_side_profile.png \
  --figure-title "Corrected Class-1/C1 COOH-GQD — side-profile audit"
```

Expected scientific result: **PASS**.

Reference corrected C1 results:

- C55H18O2 / 75 atoms;
- 93 inferred GQD bonds;
- 72 scaffold C-C edges;
- degree distribution: 18 degree-2 / 36 degree-3;
- connected graph;
- cycle rank 19;
- 19 six-membered cycles;
- plane RMS 0.008792 A;
- plane span 0.047391 A;
- max |deviation| 0.027413 A;
- COOH connectivity PASS.

### Historical Gaussian optimization trajectory

When the full historical Gaussian output is present in the local scientific archive:

```bash
python scripts/audit_gqd_geometry_topology.py \
  archive/logs/cooh_gqd_b3lyp_optfreq_v01.log \
  --geometry first
```

and:

```bash
python scripts/audit_gqd_geometry_topology.py \
  archive/logs/cooh_gqd_b3lyp_optfreq_v01.log \
  --geometry last
```

allow the starting and final geometries to be audited separately.

## Important historical nuance

Lab Journal Entry 041 records the **original/source historical geometry** as having 73 perceived scaffold C-C edges, two degree-4 carbons, and cycle rank 20, along with severe nonplanarity.

The repository-controlled **final historical B3LYP XYZ** does not need to reproduce every one of those original-source distance classifications. Under the canonical standalone audit it has 72 scaffold edges and the nominal 18/36 degree counts, but only 16 six-membered cycles and a 6.105481 A best-fit-plane span. It therefore still fails independently and decisively.

This distinction prevents a later audit of the final XYZ from being incorrectly described as contradictory to Entry 041.

## Relationship to existing scripts

The standalone audit consolidates and reuses the scientific logic already established by:

- `scripts/build_circumcoronene.py` — deterministic ideal C54 graph and reference invariants;
- `scripts/hydrogenate_circumcoronene.py` — distance-derived reconstruction of the parent C54 graph;
- `scripts/functionalize_circumcoronene_cooh.py` — corrected C55H18O2 construction, atom-order, COOH, contact, and planarity gates;
- `scripts/export_final_xyz.py` — export of accepted Gaussian final coordinates.

The new audit is intentionally separate from the structure builders so that a structure is not accepted solely by the code that generated it.

## Acceptance-Gate role

This tool supports:

- G1 — molecular identity;
- G2 — graph / connectivity / topology;
- G3 — geometry plausibility;
- G9 — independent scientific validation.

It does not replace Gaussian QC, frequency analysis, provenance, or archive-integrity controls.
