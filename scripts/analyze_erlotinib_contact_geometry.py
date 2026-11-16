#!/usr/bin/env python3

from pathlib import Path
from cclib.io import ccread
import numpy as np
import csv

CASES = [
    (
        "Flat",
        "B3LYP-COOH-GQD-ERLOTINIB-FLAT-001",
        Path("archive/logs/cooh_gqd_c1_erlotinib_flat_b3lyp_optfreq_v01.log"),
    ),
    (
        "Slipped",
        "B3LYP-COOH-GQD-ERLOTINIB-SLIPPED-001",
        Path("archive/logs/cooh_gqd_c1_erlotinib_slipped_b3lyp_optfreq_v01.log"),
    ),
    (
        "Edge",
        "B3LYP-COOH-GQD-ERLOTINIB-EDGE-003",
        Path("archive/logs/cooh_gqd_c1_erlotinib_edge_b3lyp_optfreq_v03.log"),
    ),
]

SYMBOL = {
    1: "H",
    6: "C",
    7: "N",
    8: "O",
}

def fit_plane(xyz):
    center = xyz.mean(axis=0)
    shifted = xyz - center

    _, _, vh = np.linalg.svd(
        shifted,
        full_matrices=False,
    )

    normal = vh[-1]
    distances = shifted @ normal
    rms = np.sqrt(np.mean(distances ** 2))

    return center, normal, rms

rows = []

for pose, run_id, log in CASES:

    data = ccread(str(log))

    if data is None:
        raise SystemExit(f"ERROR: cannot parse {log}")

    xyz = np.asarray(data.atomcoords[-1], dtype=float)
    z = np.asarray(data.atomnos, dtype=int)

    if len(xyz) != 127:
        raise SystemExit(
            f"ERROR: {pose} has {len(xyz)} atoms"
        )

    gxyz = xyz[:75]
    gz = z[:75]

    dxyz = xyz[75:]
    dz = z[75:]

    delta = (
        gxyz[:, None, :]
        - dxyz[None, :, :]
    )

    dist = np.linalg.norm(
        delta,
        axis=2,
    )

    i, j = np.unravel_index(
        np.argmin(dist),
        dist.shape,
    )

    min_all = float(dist[i, j])

    heavy_g = np.where(gz > 1)[0]
    heavy_d = np.where(dz > 1)[0]

    heavy_dist = dist[
        np.ix_(heavy_g, heavy_d)
    ]

    hi, hj = np.unravel_index(
        np.argmin(heavy_dist),
        heavy_dist.shape,
    )

    gi = heavy_g[hi]
    dj = heavy_d[hj]

    min_heavy = float(heavy_dist[hi, hj])

    gqd_carbons = gxyz[gz == 6]
    drug_heavy = dxyz[dz > 1]

    gc, gn, g_rms = fit_plane(gqd_carbons)
    dc, dn, d_rms = fit_plane(drug_heavy)

    cosang = np.clip(
        abs(np.dot(gn, dn)),
        0.0,
        1.0,
    )

    angle = np.degrees(np.arccos(cosang))

    heights = np.abs(
        (drug_heavy - gc) @ gn
    )

    rows.append({
        "pose": pose,
        "run_id": run_id,
        "min_all_distance_A": f"{min_all:.4f}",
        "closest_all_pair": (
            f"{i+1}:{SYMBOL[gz[i]]}-"
            f"{75+j+1}:{SYMBOL[dz[j]]}"
        ),
        "min_heavy_distance_A": f"{min_heavy:.4f}",
        "closest_heavy_pair": (
            f"{gi+1}:{SYMBOL[gz[gi]]}-"
            f"{75+dj+1}:{SYMBOL[dz[dj]]}"
        ),
        "heavy_pairs_le_3.5A":
            int(np.sum(heavy_dist <= 3.5)),
        "heavy_pairs_le_4.0A":
            int(np.sum(heavy_dist <= 4.0)),
        "gqd_carbon_plane_rms_A":
            f"{g_rms:.4f}",
        "drug_heavy_principal_plane_rms_A":
            f"{d_rms:.4f}",
        "principal_plane_angle_deg":
            f"{angle:.3f}",
        "drug_heavy_centroid_height_A":
            f"{abs(np.dot(dc-gc, gn)):.4f}",
        "drug_heavy_mean_height_A":
            f"{heights.mean():.4f}",
        "drug_heavy_median_height_A":
            f"{np.median(heights):.4f}",
    })

out = Path(
    "calculations/phase1_dft/descriptors/results/"
    "erlotinib_contact_geometry.tsv"
)

with out.open("w", newline="") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=rows[0].keys(),
        delimiter="\t",
    )

    writer.writeheader()
    writer.writerows(rows)

print("PASS: contact-geometry descriptors generated.")
print(f"Wrote: {out}")

for row in rows:
    print(
        f'{row["pose"]:8s} '
        f'min={row["min_all_distance_A"]} Å '
        f'heavy={row["min_heavy_distance_A"]} Å '
        f'angle={row["principal_plane_angle_deg"]}° '
        f'contacts4A={row["heavy_pairs_le_4.0A"]}'
    )
