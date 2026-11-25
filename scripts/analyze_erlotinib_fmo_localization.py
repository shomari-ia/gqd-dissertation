#!/usr/bin/env python3
"""Geometric orbital localization proxy; not a QTAIM/Hirshfeld or AO population."""
import argparse
import csv
import hashlib
from collections import Counter
from pathlib import Path
import numpy as np
from analyze_orbital_cubes import read_cube

BASE = Path("calculations/phase1_dft/descriptors/orbitals")
POSES = {
    "flat": "CUBEGEN-ERLOTINIB-FLAT-FMO-PILOT-001",
    "slipped": "CUBEGEN-ERLOTINIB-SLIPPED-FMO-001",
    "edge": "CUBEGEN-ERLOTINIB-EDGE-FMO-001",
}

def digest(path):
    with path.open("rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest() if hasattr(hashlib, "file_digest") else old_digest(f)

def old_digest(f):
    h = hashlib.sha256()
    for block in iter(lambda: f.read(1048576), b""):
        h.update(block)
    return h.hexdigest()

def nearest_squared(points, atoms):
    return np.min(np.sum((points[:, None, :] - atoms[None, :, :])**2, axis=2), axis=1)

def weights(points, gqd, drug):
    dg = nearest_squared(points, gqd)
    dd = nearest_squared(points, drug)
    return np.where(dg < dd, 1.0, np.where(dg > dd, 0.0, 0.5))

def points_at(indices, dims, origin, vecs):
    # Gaussian cube order: first axis outermost, third axis innermost.
    ijk = np.column_stack(np.unravel_index(indices, dims, order="C"))
    return origin + ijk @ np.asarray(vecs)

def self_test():
    g = np.array([[0., 0., 0.]])
    d = np.array([[2., 0., 0.]])
    pts = np.array([[0., 0., 0.], [1., 0., 0.], [2., 0., 0.]])
    assert np.array_equal(weights(pts, g, d), [1., .5, 0.])
    pts = points_at(np.array([0, 1, 2, 4]), (2, 2, 2), np.zeros(3), np.eye(3))
    assert np.array_equal(pts, [[0,0,0],[0,0,1],[0,1,0],[1,0,0]])

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    if args.out.exists():
        raise SystemExit(f"Refusing to overwrite {args.out}")
    self_test()
    rows = []
    for pose, aid in POSES.items():
        prov = dict(line.split("=", 1) for line in (BASE / "prov" / f"{aid}.prov").read_text().splitlines() if "=" in line)
        if prov.get("return_code") != "0":
            raise SystemExit(f"{pose}: unsuccessful provenance")
        pair = []
        for orb, idx in (("homo", 286), ("lumo", 287)):
            path = BASE / "results" / aid / f"erlotinib_{pose}_m062x_{orb}.cube"
            if digest(path) != prov[f"{orb}_sha256"]:
                raise SystemExit(f"{pose}: {orb} hash mismatch")
            data = read_cube(path)
            if data["nat"] != 127 or data["mo_index"] != idx or abs(data["norm2"]-1) > 0.01:
                raise SystemExit(f"{pose}: {orb} fails orbital QC")
            pair.append(data)
        h, l = pair
        if h["dims"] != l["dims"] or any(not np.allclose(h[k], l[k], atol=1e-10, rtol=0) for k in ("atoms","origin","vecs")):
            raise SystemExit(f"{pose}: inconsistent cube geometries")
        z = h["atoms"][:,0].astype(int)
        if Counter(z[:75]) != Counter({6:55,1:18,8:2}) or Counter(z[75:]) != Counter({6:22,1:23,7:3,8:4}):
            raise SystemExit(f"{pose}: fragment formula/order check failed")
        xyz = h["atoms"][:,2:5]
        g, d = xyz[:75], xyz[75:]
        gh, dh = g[z[:75]>1], d[z[75:]>1]
        sums = np.zeros((2,2))
        total = np.zeros(2)
        for start in range(0, h["values"].size, 4096):
            stop = min(start+4096, h["values"].size)
            pts = points_at(np.arange(start, stop), h["dims"], h["origin"], h["vecs"])
            w = np.vstack([weights(pts, g, d), weights(pts, gh, dh)])
            sq = np.vstack([v["values"][start:stop]**2 for v in pair])
            sums += sq @ w.T
            total += sq.sum(axis=1)
        for i, orb in enumerate(("HOMO","LUMO")):
            a, b = 100*sums[i]/total[i]
            norm = total[i]*pair[i]["voxel_bohr3"]
            if not np.isclose(norm, pair[i]["norm2"], rtol=1e-10):
                raise SystemExit(f"{pose}: integration discrepancy")
            rows.append(dict(pose=pose,orbital=orb,mo_index=pair[i]["mo_index"],
                psi2_integral=norm,gqd_nearest_all_pct=a,drug_nearest_all_pct=100-a,
                gqd_nearest_heavy_pct=b,drug_nearest_heavy_pct=100-b,
                sensitivity_pp=abs(a-b),cube_sha256=prov[f"{orb.lower()}_sha256"],
                qc_status="PASS"))
        print(f"PASS: {pose} — hashes, formula split, matched grids, spatial integration")
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("x", newline="") as f:
        writer=csv.DictWriter(f, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote: {args.out}")

if __name__ == "__main__":
    main()
