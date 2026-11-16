#!/usr/bin/env python3

from pathlib import Path
from cclib.io import ccread
import numpy as np
import csv

LOG = Path(
    "archive/logs/"
    "cooh_gqd_c1_erlotinib_edge_b3lyp_optfreq_v03.log"
)

OUT = Path(
    "calculations/phase1_dft/descriptors/results/"
    "erlotinib_edge_polar_contact.tsv"
)

RUN_ID = "B3LYP-COOH-GQD-ERLOTINIB-EDGE-003"

# 1-based controlled atom identifiers
H_ID = 75
ACCEPTOR_ID = 81

SYMBOL = {
    1: "H",
    6: "C",
    7: "N",
    8: "O",
}

data = ccread(str(LOG))

if data is None:
    raise SystemExit("ERROR: cclib could not parse Edge log")

xyz = np.asarray(data.atomcoords[-1], dtype=float)
z = np.asarray(data.atomnos, dtype=int)

if len(xyz) != 127:
    raise SystemExit(
        f"ERROR: expected 127 atoms; found {len(xyz)}"
    )

h = H_ID - 1
a = ACCEPTOR_ID - 1

if z[h] != 1:
    raise SystemExit(
        f"ERROR: atom {H_ID} is not hydrogen"
    )

if z[a] == 1:
    raise SystemExit(
        f"ERROR: acceptor {ACCEPTOR_ID} is hydrogen"
    )

# H75 belongs to the 75-atom GQD fragment.
# Identify its nearest heavy-atom parent within that fragment.
candidates = [
    i for i in range(75)
    if i != h and z[i] > 1
]

dist_to_h = sorted(
    (
        float(np.linalg.norm(xyz[i] - xyz[h])),
        i
    )
    for i in candidates
)

parent_distance, d = dist_to_h[0]

if parent_distance > 1.30:
    raise SystemExit(
        "ERROR: H75 has no plausible covalent "
        f"heavy-atom parent; nearest={parent_distance:.4f} Å"
    )

dh = float(
    np.linalg.norm(xyz[d] - xyz[h])
)

ha = float(
    np.linalg.norm(xyz[h] - xyz[a])
)

da = float(
    np.linalg.norm(xyz[d] - xyz[a])
)

v1 = xyz[d] - xyz[h]
v2 = xyz[a] - xyz[h]

cosang = np.dot(v1, v2) / (
    np.linalg.norm(v1)
    * np.linalg.norm(v2)
)

cosang = float(
    np.clip(cosang, -1.0, 1.0)
)

angle = float(
    np.degrees(np.arccos(cosang))
)

OUT.parent.mkdir(
    parents=True,
    exist_ok=True
)

row = {
    "run_id": RUN_ID,
    "donor_atom": f"{d+1}:{SYMBOL[int(z[d])]}",
    "hydrogen_atom": f"{H_ID}:H",
    "acceptor_atom": (
        f"{ACCEPTOR_ID}:{SYMBOL[int(z[a])]}"
    ),
    "donor_H_A": f"{dh:.6f}",
    "H_acceptor_A": f"{ha:.6f}",
    "donor_acceptor_A": f"{da:.6f}",
    "donor_H_acceptor_angle_deg": f"{angle:.3f}",
}

with OUT.open("w", newline="") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=row.keys(),
        delimiter="\t",
    )
    writer.writeheader()
    writer.writerow(row)

print("PASS: Edge polar-contact geometry resolved.")
print()
print("Nearest heavy atoms to H75:")

for dist, i in dist_to_h[:5]:
    print(
        f"  {i+1}:{SYMBOL[int(z[i])]} "
        f"{dist:.6f} Å"
    )

print()
print(
    "Candidate contact: "
    f'{row["donor_atom"]}-'
    f'{row["hydrogen_atom"]}...'
    f'{row["acceptor_atom"]}'
)
print(
    f'D-H       = {row["donor_H_A"]} Å'
)
print(
    f'H...A     = {row["H_acceptor_A"]} Å'
)
print(
    f'D...A     = {row["donor_acceptor_A"]} Å'
)
print(
    "D-H...A angle = "
    f'{row["donor_H_acceptor_angle_deg"]}°'
)
print()
print(f"Wrote: {OUT}")
