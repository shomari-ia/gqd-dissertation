#!/usr/bin/env python3
"""QC summary for Critic2 NCIPLOT outputs.

This script is descriptive only. It does not assign interaction energies.
The NCIPLOT .dat first column is sign(lambda2)*rho and the second is RDG.
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path

import numpy as np


def read_dat(path: Path) -> np.ndarray:
    rows = []
    with path.open() as f:
        for line in f:
            s = line.strip()
            if not s or s.startswith("#"):
                continue
            parts = s.split()
            if len(parts) < 2:
                continue
            try:
                rows.append((float(parts[0]), float(parts[1])))
            except ValueError:
                continue
    if not rows:
        raise SystemExit(f"ERROR: no numeric NCI rows parsed from {path}")
    return np.asarray(rows, dtype=float)


def cube_header(path: Path):
    with path.open() as f:
        f.readline()
        f.readline()
        atom_line = f.readline().split()
        if len(atom_line) < 4:
            raise SystemExit(f"ERROR: malformed cube atom/origin line: {path}")
        nat = abs(int(atom_line[0]))
        axes = []
        dims = []
        for _ in range(3):
            p = f.readline().split()
            dims.append(abs(int(p[0])))
            axes.append(tuple(float(x) for x in p[1:4]))
    norms_bohr = [math.sqrt(sum(x*x for x in a)) for a in axes]
    return nat, tuple(dims), tuple(norms_bohr)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("result_dir", type=Path)
    ap.add_argument("--root", required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()

    r = args.result_dir
    dat = r / f"{args.root}.dat"
    dens = r / f"{args.root}-dens.cube"
    grad = r / f"{args.root}-grad.cube"
    pdens = r / f"{args.root}-pdens.cube"
    vmd = r / f"{args.root}.vmd"

    for p in (dat, dens, grad, pdens, vmd):
        if not p.is_file() or p.stat().st_size == 0:
            raise SystemExit(f"ERROR: missing/empty expected NCI artifact: {p}")

    a = read_dat(dat)
    srho = a[:, 0]
    rdg = a[:, 1]

    low = rdg <= 0.5
    low_srho = srho[low]

    nat_d, dims_d, step_d = cube_header(dens)
    nat_g, dims_g, step_g = cube_header(grad)
    nat_p, dims_p, step_p = cube_header(pdens)

    if not (nat_d == nat_g == nat_p == 127):
        raise SystemExit(
            f"ERROR: cube atom count mismatch: dens={nat_d}, grad={nat_g}, pdens={nat_p}"
        )
    if not (dims_d == dims_g == dims_p):
        raise SystemExit(
            f"ERROR: cube grid mismatch: dens={dims_d}, grad={dims_g}, pdens={dims_p}"
        )

    fields = [
        ("dat_rows", len(a)),
        ("signed_rho_min", float(np.min(srho))),
        ("signed_rho_max", float(np.max(srho))),
        ("rdg_min", float(np.min(rdg))),
        ("rdg_max", float(np.max(rdg))),
        ("low_rdg_le_0.5_points", int(np.count_nonzero(low))),
        ("low_rdg_negative_srho_points", int(np.count_nonzero(low_srho < 0))),
        ("low_rdg_positive_srho_points", int(np.count_nonzero(low_srho > 0))),
        ("low_rdg_zero_srho_points", int(np.count_nonzero(low_srho == 0))),
        ("low_rdg_signed_rho_p05", float(np.quantile(low_srho, 0.05)) if len(low_srho) else math.nan),
        ("low_rdg_signed_rho_p50", float(np.quantile(low_srho, 0.50)) if len(low_srho) else math.nan),
        ("low_rdg_signed_rho_p95", float(np.quantile(low_srho, 0.95)) if len(low_srho) else math.nan),
        ("cube_atoms", nat_d),
        ("cube_nx", dims_d[0]),
        ("cube_ny", dims_d[1]),
        ("cube_nz", dims_d[2]),
        ("cube_step_x_bohr", step_d[0]),
        ("cube_step_y_bohr", step_d[1]),
        ("cube_step_z_bohr", step_d[2]),
        ("dat_bytes", dat.stat().st_size),
        ("dens_cube_bytes", dens.stat().st_size),
        ("grad_cube_bytes", grad.stat().st_size),
        ("pdens_cube_bytes", pdens.stat().st_size),
        ("vmd_bytes", vmd.stat().st_size),
        ("qc_status", "PASS"),
    ]

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w") as f:
        f.write("metric\tvalue\n")
        for k, v in fields:
            f.write(f"{k}\t{v}\n")

    print("PASS: Critic2 NCI/RDG QC summary complete.")
    print(f"Rows: {len(a)}")
    print(f"sign(lambda2)*rho range: {srho.min():+.8f} to {srho.max():+.8f}")
    print(f"RDG range: {rdg.min():.8f} to {rdg.max():.8f}")
    print(f"RDG <= 0.5 points: {np.count_nonzero(low)}")
    print(
        "Low-RDG signed-rho counts: "
        f"negative={np.count_nonzero(low_srho < 0)} "
        f"positive={np.count_nonzero(low_srho > 0)}"
    )
    print(f"Cube grid: {dims_d[0]} x {dims_d[1]} x {dims_d[2]}")
    print(f"Wrote: {args.out}")


if __name__ == "__main__":
    main()
