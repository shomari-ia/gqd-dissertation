#!/usr/bin/env python3
"""Basic QC for Gaussian cubegen HOMO/LUMO cube files."""

from __future__ import annotations

import argparse
import math
from pathlib import Path

import numpy as np


def read_cube(path: Path):
    with path.open() as f:
        comment1 = f.readline().rstrip("\n")
        comment2 = f.readline().rstrip("\n")

        p = f.readline().split()
        nat = abs(int(p[0]))
        origin = np.array([float(x) for x in p[1:4]], dtype=float)

        dims = []
        vecs = []
        for _ in range(3):
            q = f.readline().split()
            dims.append(abs(int(q[0])))
            vecs.append(np.array([float(x) for x in q[1:4]], dtype=float))

        for _ in range(nat):
            f.readline()

        vals = np.fromstring(f.read(), sep=" ")

    expected = dims[0] * dims[1] * dims[2]
    if vals.size != expected:
        raise SystemExit(
            f"ERROR: {path} has {vals.size} grid values, expected {expected}"
        )

    voxel = abs(np.linalg.det(np.vstack(vecs)))
    norm2 = float(np.sum(vals * vals) * voxel)

    return {
        "comment1": comment1,
        "comment2": comment2,
        "nat": nat,
        "origin": origin,
        "dims": tuple(dims),
        "vecs": tuple(vecs),
        "voxel_bohr3": voxel,
        "values": vals,
        "norm2": norm2,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("homo", type=Path)
    ap.add_argument("lumo", type=Path)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()

    h = read_cube(args.homo)
    l = read_cube(args.lumo)

    if h["nat"] != l["nat"]:
        raise SystemExit("ERROR: HOMO/LUMO cube atom counts differ")
    if h["dims"] != l["dims"]:
        raise SystemExit("ERROR: HOMO/LUMO cube grid dimensions differ")
    if any(not np.allclose(a, b, atol=1e-10) for a, b in zip(h["vecs"], l["vecs"])):
        raise SystemExit("ERROR: HOMO/LUMO cube grid vectors differ")
    if not np.allclose(h["origin"], l["origin"], atol=1e-10):
        raise SystemExit("ERROR: HOMO/LUMO cube origins differ")

    rows = []
    for name, d, path in (("HOMO", h, args.homo), ("LUMO", l, args.lumo)):
        vals = d["values"]
        rows.append({
            "orbital": name,
            "atoms": d["nat"],
            "nx": d["dims"][0],
            "ny": d["dims"][1],
            "nz": d["dims"][2],
            "voxel_bohr3": d["voxel_bohr3"],
            "value_min": float(vals.min()),
            "value_max": float(vals.max()),
            "abs_max": float(np.max(np.abs(vals))),
            "psi2_integral_approx": d["norm2"],
            "voxels_abs_ge_0.02": int(np.count_nonzero(np.abs(vals) >= 0.02)),
            "bytes": path.stat().st_size,
            "qc_status": "PASS",
        })

    args.out.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0].keys())
    with args.out.open("w") as f:
        f.write("\t".join(fields) + "\n")
        for r in rows:
            f.write("\t".join(str(r[k]) for k in fields) + "\n")

    print("PASS: HOMO/LUMO cube QC complete.")
    print(f"Atoms: {h['nat']}")
    print(f"Grid: {h['dims'][0]} x {h['dims'][1]} x {h['dims'][2]}")
    print(f"HOMO approx integral psi^2: {h['norm2']:.8f}")
    print(f"LUMO approx integral psi^2: {l['norm2']:.8f}")
    print(f"Wrote: {args.out}")


if __name__ == "__main__":
    main()
