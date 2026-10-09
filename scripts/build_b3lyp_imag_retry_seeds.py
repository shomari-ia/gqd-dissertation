#!/usr/bin/env python3

from pathlib import Path
from collections import Counter
import hashlib

import cclib
import numpy as np


MAX_DISPLACEMENT = 0.10

SYSTEMS = [
    {
        "label": "CLASS 1 / C1",
        "log": Path(
            "archive/logs/"
            "cooh_gqd_class1_c1_b3lyp_optfreq_v02.log"
        ),
        "stem": "cooh_gqd_class1_c1_b3lyp_v02_imag",
    },
    {
        "label": "CLASS 2 / C3",
        "log": Path(
            "archive/logs/"
            "cooh_gqd_class2_c3_b3lyp_optfreq_v02.log"
        ),
        "stem": "cooh_gqd_class2_c3_b3lyp_v02_imag",
    },
]

OUTDIR = Path("structures/prepared")

SYMBOLS = {
    1: "H",
    6: "C",
    8: "O",
}

RADII = {
    "H": 0.31,
    "C": 0.76,
    "O": 0.66,
}

BOND_TOL = 0.45


def sha256(path):
    h = hashlib.sha256()

    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)

    return h.hexdigest()


def inferred_bonds(symbols, xyz):
    bonds = set()

    for i in range(len(symbols)):
        for j in range(i + 1, len(symbols)):
            cutoff = (
                RADII[symbols[i]]
                + RADII[symbols[j]]
                + BOND_TOL
            )

            distance = np.linalg.norm(xyz[i] - xyz[j])

            if distance <= cutoff:
                bonds.add((i + 1, j + 1))

    return bonds


def write_xyz(path, symbols, xyz, comment):
    with path.open("w") as handle:
        handle.write("{}\n".format(len(symbols)))
        handle.write("{}\n".format(comment))

        for symbol, coord in zip(symbols, xyz):
            handle.write(
                "{:<2s} {: .10f} {: .10f} {: .10f}\n".format(
                    symbol,
                    coord[0],
                    coord[1],
                    coord[2],
                )
            )


OUTDIR.mkdir(parents=True, exist_ok=True)

print("===== B3LYP IMAGINARY-MODE RETRY SEED BUILD =====")
print("MAX_ATOM_DISPLACEMENT={:.3f} A".format(MAX_DISPLACEMENT))

for system in SYSTEMS:
    print()
    print("=" * 72)
    print(system["label"])
    print("=" * 72)

    data = cclib.io.ccread(str(system["log"]))

    if data is None:
        raise SystemExit(
            "ERROR: cclib could not parse {}".format(system["log"])
        )

    atomnos = np.asarray(data.atomnos, dtype=int)
    coords = np.asarray(data.atomcoords[-1], dtype=float)
    freqs = np.asarray(data.vibfreqs, dtype=float)
    disps = np.asarray(data.vibdisps, dtype=float)

    if len(atomnos) != 75:
        raise SystemExit(
            "ERROR: expected 75 atoms; found {}".format(len(atomnos))
        )

    if len(freqs) != 219:
        raise SystemExit(
            "ERROR: expected 219 modes; found {}".format(len(freqs))
        )

    negative = np.where(freqs < 0.0)[0]

    if len(negative) != 1:
        raise SystemExit(
            "ERROR: expected exactly one imaginary mode; found {}".format(
                len(negative)
            )
        )

    symbols = [SYMBOLS[int(z)] for z in atomnos]

    formula = Counter(symbols)

    if formula != Counter({"C": 55, "H": 18, "O": 2}):
        raise SystemExit(
            "ERROR: unexpected formula {}".format(dict(formula))
        )

    mode_index = negative[0]
    mode = disps[mode_index]

    amplitudes = np.linalg.norm(mode, axis=1)
    mode_max = float(np.max(amplitudes))

    if mode_max <= 0.0:
        raise SystemExit("ERROR: zero imaginary-mode amplitude")

    delta = mode * (MAX_DISPLACEMENT / mode_max)

    reference_bonds = inferred_bonds(symbols, coords)

    print("SOURCE_LOG={}".format(system["log"]))
    print("N_ATOMS={}".format(len(atomnos)))
    print("FORMULA=C55H18O2")
    print("N_MODES={}".format(len(freqs)))
    print(
        "IMAGINARY_FREQUENCY_CM-1={:.4f}".format(
            freqs[mode_index]
        )
    )
    print(
        "REFERENCE_INFERRED_BONDS={}".format(
            len(reference_bonds)
        )
    )

    if len(reference_bonds) != 93:
        print(
            "WARNING: reference inferred bond count is {}, expected 93".format(
                len(reference_bonds)
            )
        )

    for sign, direction in (
        (1.0, "plus"),
        (-1.0, "minus"),
    ):
        displaced = coords + sign * delta

        out = OUTDIR / (
            "{}_{}_010A.xyz".format(
                system["stem"],
                direction,
            )
        )

        comment = (
            "{} | source={} | mode={} | freq={:.4f} cm-1 | "
            "{} imaginary-mode displacement | max_atom=0.10 A"
        ).format(
            system["label"],
            system["log"],
            mode_index + 1,
            freqs[mode_index],
            direction.upper(),
        )

        write_xyz(
            out,
            symbols,
            displaced,
            comment,
        )

        new_bonds = inferred_bonds(symbols, displaced)

        lost = sorted(reference_bonds - new_bonds)
        gained = sorted(new_bonds - reference_bonds)

        actual_max = float(
            np.max(
                np.linalg.norm(
                    displaced - coords,
                    axis=1,
                )
            )
        )

        print()
        print("DIRECTION={}".format(direction.upper()))
        print("FILE={}".format(out))
        print(
            "MAX_ATOM_DISPLACEMENT_A={:.6f}".format(
                actual_max
            )
        )
        print(
            "INFERRED_BONDS={}".format(
                len(new_bonds)
            )
        )
        print(
            "BONDS_LOST={}".format(
                len(lost)
            )
        )
        print(
            "BONDS_GAINED={}".format(
                len(gained)
            )
        )

        if lost:
            print("LOST_BOND_PAIRS={}".format(lost))

        if gained:
            print("GAINED_BOND_PAIRS={}".format(gained))

        if new_bonds != reference_bonds:
            raise SystemExit(
                "ERROR: connectivity changed in {}".format(out)
            )

        print("GRAPH_PRESERVED=PASS")
        print("SHA256={}".format(sha256(out)))

print()
print("ALL_RETRY_SEEDS=PASS")
