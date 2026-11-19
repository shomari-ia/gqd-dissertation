#!/usr/bin/env python3
"""Build deterministic GQD/Erlotinib XYZ fragments for Critic2 NCI analysis."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
from cclib.io import ccread

POSES = {
    "flat": Path("archive/logs/cooh_gqd_c1_erlotinib_flat_m062x_smd_sp_v01.log"),
    "slipped": Path("archive/logs/cooh_gqd_c1_erlotinib_slipped_m062x_smd_sp_v01.log"),
    "edge": Path("archive/logs/cooh_gqd_c1_erlotinib_edge_m062x_smd_sp_v01.log"),
}

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
    return "".join(
        f"{s}{counts[s] if counts[s] != 1 else ''}"
        for s in ("C", "H", "N", "O")
        if s in counts
    )


def write_xyz(path, atomnos, xyz, comment):
    with path.open("w") as f:
        f.write(f"{len(atomnos)}\n")
        f.write(comment + "\n")
        for z, (x, y, zc) in zip(atomnos, xyz):
            f.write(f"{SYMBOL[int(z)]:2s} {x: .10f} {y: .10f} {zc: .10f}\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pose", choices=sorted(POSES), required=True)
    args = ap.parse_args()

    source = POSES[args.pose]
    data = ccread(str(source))
    if data is None:
        raise SystemExit(f"ERROR: cclib could not parse {source}")

    xyz = np.asarray(data.atomcoords[-1], dtype=float)
    atomnos = np.asarray(data.atomnos, dtype=int)

    if len(atomnos) != EXPECTED_TOTAL:
        raise SystemExit(f"ERROR: expected {EXPECTED_TOTAL} atoms; found {len(atomnos)}")

    gqd_z = atomnos[:GQD_N]
    drug_z = atomnos[GQD_N:]

    if len(drug_z) != DRUG_N:
        raise SystemExit(f"ERROR: expected {DRUG_N} Erlotinib atoms; found {len(drug_z)}")
    if formula(gqd_z) != "C55H18O2":
        raise SystemExit(f"ERROR: unexpected GQD formula: {formula(gqd_z)}")
    if formula(drug_z) != "C22H23N3O4":
        raise SystemExit(f"ERROR: unexpected Erlotinib formula: {formula(drug_z)}")

    OUTDIR.mkdir(parents=True, exist_ok=True)
    gqd = OUTDIR / f"{args.pose}_gqd.xyz"
    drug = OUTDIR / f"{args.pose}_erlotinib.xyz"

    write_xyz(
        gqd, gqd_z, xyz[:GQD_N],
        f"{args.pose.title()} GQD fragment; atoms 1-75 from accepted M06-2X complex",
    )
    write_xyz(
        drug, drug_z, xyz[GQD_N:],
        f"{args.pose.title()} Erlotinib fragment; atoms 76-127 from accepted M06-2X complex",
    )

    print(f"PASS: {args.pose.title()} NCI fragments built.")
    print(f"GQD:       {gqd}  atoms={len(gqd_z)} formula={formula(gqd_z)}")
    print(f"Erlotinib: {drug}  atoms={len(drug_z)} formula={formula(drug_z)}")


if __name__ == "__main__":
    main()
