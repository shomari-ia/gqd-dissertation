#!/usr/bin/env python3

import argparse
import itertools
import sys

import numpy as np


COV = {
    "H": 0.31,
    "C": 0.76,
    "N": 0.71,
    "O": 0.66,
    "F": 0.57,
    "P": 1.07,
    "S": 1.05,
    "Cl": 0.99,
    "Br": 1.20,
}

BOND_TOL = 0.45


def normalize_element(e):
    if len(e) == 1:
        return e.upper()
    return e[0].upper() + e[1:].lower()


def read_xyz(path):
    with open(path) as f:
        lines = f.read().splitlines()

    if len(lines) < 2:
        sys.exit("ERROR: malformed XYZ: {}".format(path))

    n = int(lines[0].split()[0])

    if len(lines) < n + 2:
        sys.exit(
            "ERROR: XYZ declares {} atoms but contains too few coordinate lines".format(n)
        )

    elems = []
    coords = []

    for line in lines[2:2 + n]:
        p = line.split()

        if len(p) < 4:
            sys.exit("ERROR: malformed coordinate line: {}".format(line))

        elems.append(normalize_element(p[0]))
        coords.append([float(p[1]), float(p[2]), float(p[3])])

    return elems, np.array(coords, dtype=float)


def perceive_bonds(elems, coords):
    adj = {i: set() for i in range(len(elems))}

    for i, j in itertools.combinations(range(len(elems)), 2):
        ri = COV.get(elems[i], 0.77)
        rj = COV.get(elems[j], 0.77)
        d = float(np.linalg.norm(coords[i] - coords[j]))

        if 0.40 < d <= ri + rj + BOND_TOL:
            adj[i].add(j)
            adj[j].add(i)

    return adj


def rings_of_size(adj, allowed, size):
    found = set()

    def walk(start, current, path):
        if len(path) == size:
            if start in adj[current]:
                found.add(frozenset(path))
            return

        for nb in adj[current]:
            if nb not in allowed:
                continue
            if nb in path:
                continue
            walk(start, nb, path + [nb])

    for start in sorted(allowed):
        walk(start, start, [start])

    return found


def fmt_indices(indices):
    return " ".join(str(i + 1) for i in sorted(indices))


def main():
    ap = argparse.ArgumentParser(
        description="Inspect accepted drug XYZ and identify aromatic-core and polar-contact candidates."
    )
    ap.add_argument("xyz")
    args = ap.parse_args()

    elems, coords = read_xyz(args.xyz)
    adj = perceive_bonds(elems, coords)

    heavy = {i for i, e in enumerate(elems) if e != "H"}
    rings6 = rings_of_size(adj, heavy, 6)

    fused = {}

    for a, b in itertools.combinations(rings6, 2):
        if len(a & b) != 2:
            continue

        core = frozenset(a | b)

        if len(core) != 10:
            continue

        n_count = sum(1 for i in core if elems[i] == "N")
        fused[core] = n_count

    quinazoline = [
        core for core, n_count in fused.items()
        if n_count == 2
    ]

    print("===== DRUG INSPECTION =====")
    print("file              {}".format(args.xyz))
    print("atoms             {}".format(len(elems)))
    print("heavy_atoms       {}".format(len(heavy)))
    print("six_member_rings  {}".format(len(rings6)))
    print("fused_6_6_cores   {}".format(len(fused)))
    print("quinazoline_like  {}".format(len(quinazoline)))

    print()
    print("===== FUSED 6-6 CORE CANDIDATES =====")

    if not fused:
        print("NONE")
    else:
        for k, core in enumerate(
            sorted(fused, key=lambda x: tuple(sorted(x))), 1
        ):
            labels = " ".join(
                "{}{}".format(i + 1, elems[i])
                for i in sorted(core)
            )
            print(
                "core {}: N_count={} atoms={}".format(
                    k, fused[core], labels
                )
            )

    if len(quinazoline) == 1:
        core = quinazoline[0]
        print()
        print("===== UNIQUE QUINAZOLINE CORE =====")
        print("--drug-core {}".format(fmt_indices(core)))
    elif len(quinazoline) == 0:
        print()
        print("ERROR: no unique quinazoline-like fused 6-6 core detected.")
        sys.exit(2)
    else:
        print()
        print(
            "ERROR: multiple quinazoline-like cores detected; "
            "manual resolution required."
        )
        for core in sorted(
            quinazoline, key=lambda x: tuple(sorted(x))
        ):
            print("candidate --drug-core {}".format(fmt_indices(core)))
        sys.exit(2)

    print()
    print("===== N / O POLAR-CONTACT CANDIDATES =====")
    print(
        "index element location    heavy_neighbors     H_neighbors"
    )

    polar = []

    for i in sorted(heavy):
        if elems[i] not in ("N", "O"):
            continue

        heavy_nb = sorted(
            j for j in adj[i]
            if elems[j] != "H"
        )
        h_nb = sorted(
            j for j in adj[i]
            if elems[j] == "H"
        )

        location = "core" if i in core else "sidechain"

        heavy_text = ",".join(
            "{}{}".format(j + 1, elems[j])
            for j in heavy_nb
        ) or "-"

        h_text = ",".join(
            "{}H".format(j + 1)
            for j in h_nb
        ) or "-"

        print(
            "{:>5} {:>7} {:<11} {:<19} {}".format(
                i + 1,
                elems[i],
                location,
                heavy_text,
                h_text,
            )
        )

        polar.append(i)

    ring_n = sorted(
        i for i in core
        if elems[i] == "N"
    )

    print()
    print("===== EDGE-POLAR CANDIDATE FLAGS =====")

    if ring_n:
        for i in ring_n:
            print(
                "candidate --drug-polar {}   # quinazoline N; chemistry must be verified".format(
                    i + 1
                )
            )
    else:
        print("No quinazoline N candidates detected.")

    print()
    print(
        "IMPORTANT: --drug-core is a structural detection result. "
        "--drug-polar remains a chemical choice and must be verified "
        "from the actual connectivity/geometry before complex construction."
    )


if __name__ == "__main__":
    main()
