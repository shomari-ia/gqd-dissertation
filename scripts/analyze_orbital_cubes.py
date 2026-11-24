#!/usr/bin/env python3
"""QC for single-orbital Gaussian cubegen HOMO/LUMO cube files."""
from __future__ import annotations

import argparse
from pathlib import Path
import numpy as np


def read_cube(path: Path):
    with path.open() as f:
        f.readline()
        f.readline()
        p = f.readline().split()
        signed_nat = int(p[0])
        if signed_nat >= 0:
            raise SystemExit(f"ERROR: {path}: expected negative NATOMS for Gaussian MO cube")
        nat = abs(signed_nat)
        origin = np.array(p[1:4], dtype=float)
        dims, vecs = [], []
        for _ in range(3):
            q = f.readline().split()
            dims.append(int(q[0]))
            vecs.append(np.array(q[1:4], dtype=float))
        if min(dims) <= 0:
            raise SystemExit(f"ERROR: {path}: invalid output grid dimensions")
        atoms = np.array([f.readline().split() for _ in range(nat)], dtype=float)
        if atoms.shape != (nat, 5) or not np.isfinite(atoms).all():
            raise SystemExit(f"ERROR: {path}: invalid atom records")
        # Gaussian MO cubes have NMO followed by NMO orbital indices.
        # The workflow produces one orbital per file; reject other formats.
        mo_record = f.readline().split()
        if len(mo_record) != 2 or int(mo_record[0]) != 1:
            raise SystemExit(f"ERROR: {path}: expected single-MO metadata record; found {mo_record}")
        mo_index = int(mo_record[1])
        if mo_index <= 0:
            raise SystemExit(f"ERROR: {path}: invalid MO index {mo_index}")
        vals = np.array(f.read().replace('D', 'E').replace('d', 'e').split(), dtype=float)
    expected = dims[0] * dims[1] * dims[2]
    if vals.size != expected:
        raise SystemExit(f"ERROR: {path} has {vals.size} grid values, expected {expected}")
    voxel = abs(np.linalg.det(np.vstack(vecs)))
    norm2 = float(np.dot(vals, vals) * voxel)
    if not np.isfinite(vals).all() or not np.isfinite(norm2) or voxel <= 0 or norm2 <= 0:
        raise SystemExit(f"ERROR: {path}: invalid grid or orbital amplitudes")
    return dict(nat=nat, atoms=atoms, origin=origin, dims=tuple(dims), vecs=vecs,
                voxel_bohr3=voxel, values=vals, norm2=norm2, mo_index=mo_index)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('homo', type=Path)
    ap.add_argument('lumo', type=Path)
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--expected-atoms', type=int)
    ap.add_argument('--expected-homo-index', type=int)
    args = ap.parse_args()
    h, l = read_cube(args.homo), read_cube(args.lumo)
    if h['nat'] != l['nat'] or (args.expected_atoms is not None and h['nat'] != args.expected_atoms):
        raise SystemExit('ERROR: unexpected HOMO/LUMO atom counts')
    if h['dims'] != l['dims']:
        raise SystemExit('ERROR: HOMO/LUMO grid dimensions differ')
    for key in ('atoms', 'origin', 'vecs'):
        if not np.allclose(h[key], l[key], atol=1e-10, rtol=0):
            raise SystemExit(f'ERROR: HOMO/LUMO {key} differ')
    if l['mo_index'] != h['mo_index'] + 1 or (args.expected_homo_index is not None and h['mo_index'] != args.expected_homo_index):
        raise SystemExit('ERROR: unexpected HOMO/LUMO orbital indices')
    rows = []
    for name, d, path in (('HOMO', h, args.homo), ('LUMO', l, args.lumo)):
        vals = d['values']
        rows.append(dict(orbital=name, mo_index=d['mo_index'], atoms=d['nat'], nx=d['dims'][0],
                         ny=d['dims'][1], nz=d['dims'][2], grid_values=vals.size,
                         voxel_bohr3=d['voxel_bohr3'], value_min=float(vals.min()),
                         value_max=float(vals.max()), abs_max=float(np.max(np.abs(vals))),
                         psi2_integral_approx=d['norm2'], voxels_abs_ge_0_02=int(np.count_nonzero(np.abs(vals)>=0.02)),
                         bytes=path.stat().st_size, qc_status='PASS'))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0])
    with args.out.open('x') as f:
        f.write('\t'.join(fields)+'\n')
        for r in rows:
            f.write('\t'.join(str(r[k]) for k in fields)+'\n')
    print('PASS: HOMO/LUMO cube QC complete.')
    print(f"Atoms: {h['nat']}; MO indices: {h['mo_index']}, {l['mo_index']}")
    print(f"Grid: {h['dims']}; values per cube: {h['values'].size}")
    print(f"HOMO approx integral psi^2: {h['norm2']:.8f}")
    print(f"LUMO approx integral psi^2: {l['norm2']:.8f}")
    print(f'Wrote: {args.out}')


if __name__ == '__main__':
    main()
