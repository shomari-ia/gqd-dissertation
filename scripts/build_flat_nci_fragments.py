#!/usr/bin/env python3
"""Build deterministic GQD/Erlotinib XYZ fragments for Critic2 NCI analysis."""

from pathlib import Path
from cclib.io import ccread
import numpy as np

SOURCE = Path("archive/logs/cooh_gqd_c1_erlotinib_flat_m062x_smd_sp_v01.log")
OUTDIR = Path("calculations/phase1_dft/descriptors/critic2/nci/fragments")

EXPECTED_TOTAL = 127
GQD_N = 75
DRUG_N = 52

SYMBOL = {1: "H", 6: "C", 7: "N", 8: "O"}


def formula(atomnos):
    counts = {}
    for z in atomnos:
        s = SYMBOL[int(z)]
        counts[s] = counts.get(s, 0) + 1
    return "".join(f"{s}{counts[s] if counts[s] != 1 else ''}" for s in ("C", "H", "N", "O") if s in counts)


def write_xyz(path, atomnos, xyz, comment):
    with path.open("w") as f:
        f.write(f"{len(atomnos)}\n")
        f.write(comment + "\n")
        for z, (x, y, zc) in zip(atomnos, xyz):
            f.write(f"{SYMBOL[int(z)]:2s} {x: .10f} {y: .10f} {zc: .10f}\n")


data = ccread(str(SOURCE))
if data is None:
    raise SystemExit("ERROR: cclib could not parse source M06-2X Flat log")

xyz = np.asarray(data.atomcoords[-1], dtype=float)
atomnos = np.asarray(data.atomnos, dtype=int)

if len(atomnos) != EXPECTED_TOTAL:
    raise SystemExit(f"ERROR: expected {EXPECTED_TOTAL} atoms; found {len(atomnos)}")

gqd_z = atomnos[:GQD_N]
drug_z = atomnos[GQD_N:]

if len(drug_z) != DRUG_N:
    raise SystemExit(f"ERROR: expected {DRUG_N} drug atoms; found {len(drug_z)}")

if formula(gqd_z) != "C55H18O2":
    raise SystemExit(f"ERROR: unexpected GQD formula: {formula(gqd_z)}")

if formula(drug_z) != "C22H23N3O4":
    raise SystemExit(f"ERROR: unexpected Erlotinib formula: {formula(drug_z)}")

OUTDIR.mkdir(parents=True, exist_ok=True)

gqd = OUTDIR / "flat_gqd.xyz"
drug = OUTDIR / "flat_erlotinib.xyz"

write_xyz(
    gqd,
    gqd_z,
    xyz[:GQD_N],
    "Flat GQD fragment; atoms 1-75 from M062X-COOH-GQD-ERLOTINIB-FLAT-001",
)
write_xyz(
    drug,
    drug_z,
    xyz[GQD_N:],
    "Flat Erlotinib fragment; atoms 76-127 from M062X-COOH-GQD-ERLOTINIB-FLAT-001",
)

print("PASS: Flat NCI fragments built.")
print(f"GQD:       {gqd}  atoms={len(gqd_z)} formula={formula(gqd_z)}")
print(f"Erlotinib: {drug}  atoms={len(drug_z)} formula={formula(drug_z)}")
