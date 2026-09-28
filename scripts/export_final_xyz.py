#!/usr/bin/env python3

import argparse
import hashlib
import os
import sys

import cclib
from cclib.parser.utils import PeriodicTable


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser(
        description="Export the final optimized geometry from an accepted Gaussian log to XYZ while preserving atom order."
    )
    ap.add_argument("input_log")
    ap.add_argument("output_xyz")
    ap.add_argument("--expected-atoms", type=int, default=None)
    args = ap.parse_args()

    if not os.path.isfile(args.input_log):
        sys.exit("ERROR: input log not found: {}".format(args.input_log))

    parser = cclib.io.ccopen(args.input_log)
    if parser is None:
        sys.exit("ERROR: cclib could not identify the Gaussian log")

    data = parser.parse()

    if not hasattr(data, "atomcoords") or len(data.atomcoords) == 0:
        sys.exit("ERROR: no atomic coordinates found")

    if not hasattr(data, "atomnos"):
        sys.exit("ERROR: no atomic numbers found")

    coords = data.atomcoords[-1]
    atomnos = data.atomnos
    n_atoms = len(atomnos)

    if len(coords) != n_atoms:
        sys.exit(
            "ERROR: coordinate/atom-number mismatch: {} vs {}".format(
                len(coords), n_atoms
            )
        )

    if args.expected_atoms is not None and n_atoms != args.expected_atoms:
        sys.exit(
            "ERROR: expected {} atoms but parsed {}".format(
                args.expected_atoms, n_atoms
            )
        )

    pt = PeriodicTable()
    source_sha = sha256_file(args.input_log)

    with open(args.output_xyz, "w") as f:
        f.write("{}\n".format(n_atoms))
        f.write(
            "final geometry from {}; sha256={}; atom_order=preserved\n".format(
                args.input_log, source_sha
            )
        )
        for z, xyz in zip(atomnos, coords):
            symbol = pt.element[int(z)]
            f.write(
                "{:<3s} {:15.8f} {:15.8f} {:15.8f}\n".format(
                    symbol, xyz[0], xyz[1], xyz[2]
                )
            )

    print("source_log      {}".format(args.input_log))
    print("source_sha256   {}".format(source_sha))
    print("output_xyz      {}".format(args.output_xyz))
    print("atoms           {}".format(n_atoms))
    print("geometry_index  final")
    print("atom_order      preserved")


if __name__ == "__main__":
    main()
