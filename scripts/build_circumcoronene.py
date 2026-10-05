#!/usr/bin/env python3

import argparse
import math
from collections import Counter
from pathlib import Path


BOND = 1.42
RADIUS = 2

EXPECTED = {
    "cells": 19,
    "carbons": 54,
    "edges": 72,
    "degree2": 18,
    "degree3": 36,
    "boundary": 18,
    "cycle_rank": 19,
    "six_cycles": 19,
}


def canonical_cycle(cycle):
    forms = []

    for seq in (
        list(cycle),
        list(reversed(cycle)),
    ):
        for k in range(len(seq)):
            forms.append(
                tuple(seq[k:] + seq[:k])
            )

    return min(forms)


def build_cells():
    cells = []

    for q in range(-RADIUS, RADIUS + 1):
        for r in range(-RADIUS, RADIUS + 1):

            if max(
                abs(q),
                abs(r),
                abs(q + r),
            ) <= RADIUS:
                cells.append((q, r))

    return sorted(cells)


def build_raw_vertices(cells):
    vertices = set()
    ring_coords = []

    for q, r in cells:

        cx = 1.5 * BOND * q
        cy = math.sqrt(3.0) * BOND * (
            r + q / 2.0
        )

        ring = []

        for k in range(6):

            angle = math.radians(
                60.0 * k
            )

            x = cx + BOND * math.cos(angle)
            y = cy + BOND * math.sin(angle)

            key = (
                round(x, 8),
                round(y, 8),
            )

            vertices.add(key)
            ring.append(key)

        ring_coords.append(ring)

    return vertices, ring_coords


def canonicalize_vertices(vertices):
    # Recenter exactly on the arithmetic centroid.
    xs = [x for x, y in vertices]
    ys = [y for x, y in vertices]

    x0 = sum(xs) / len(xs)
    y0 = sum(ys) / len(ys)

    centered = []

    for x, y in vertices:
        centered.append(
            (
                round(x - x0, 8),
                round(y - y0, 8),
            )
        )

    # Deterministic atom order:
    # bottom-to-top, then left-to-right.
    centered = sorted(
        centered,
        key=lambda p: (
            round(p[1], 8),
            round(p[0], 8),
        ),
    )

    return centered, x0, y0


def remap_ring_coords(ring_coords, x0, y0, index):
    remapped = []

    for ring in ring_coords:
        ids = []

        for x, y in ring:

            key = (
                round(x - x0, 8),
                round(y - y0, 8),
            )

            ids.append(index[key])

        remapped.append(ids)

    return remapped


def build_graph(coords, ring_ids):
    edges = set()

    for ring in ring_ids:

        for k in range(6):

            i = ring[k]
            j = ring[(k + 1) % 6]

            edges.add(
                tuple(sorted((i, j)))
            )

    adj = {
        i: set()
        for i in range(len(coords))
    }

    for i, j in edges:
        adj[i].add(j)
        adj[j].add(i)

    return edges, adj


def count_six_cycles(adj):
    cycles = set()

    def walk(start, current, path):

        if len(path) == 6:

            if start in adj[current]:
                cycles.add(
                    canonical_cycle(path)
                )

            return

        for nb in adj[current]:

            if nb in path:
                continue

            walk(
                start,
                nb,
                path + [nb],
            )

    for start in sorted(adj):
        walk(
            start,
            start,
            [start],
        )

    return cycles


def distance(coords, i, j):
    xi, yi, zi = coords[i]
    xj, yj, zj = coords[j]

    return math.sqrt(
        (xi - xj) ** 2
        + (yi - yj) ** 2
        + (zi - zj) ** 2
    )


def validate(cells, coords, edges, adj):
    degrees = Counter(
        len(adj[i])
        for i in adj
    )

    boundary = [
        i for i in adj
        if len(adj[i]) == 2
    ]

    six_cycles = count_six_cycles(adj)

    edge_lengths = [
        distance(coords, i, j)
        for i, j in sorted(edges)
    ]

    max_span = 0.0

    for i in range(len(coords)):
        for j in range(i):

            max_span = max(
                max_span,
                distance(coords, i, j),
            )

    V = len(coords)
    E = len(edges)

    connected = False

    if V:

        seen = {0}
        stack = [0]

        while stack:

            i = stack.pop()

            for j in adj[i]:

                if j not in seen:
                    seen.add(j)
                    stack.append(j)

        connected = (
            len(seen) == V
        )

    cycle_rank = (
        E - V + 1
        if connected
        else None
    )

    z_values = [
        z for x, y, z in coords
    ]

    report = {
        "cells": len(cells),
        "carbons": V,
        "edges": E,
        "degree2": degrees[2],
        "degree3": degrees[3],
        "degree_keys": sorted(degrees),
        "boundary": len(boundary),
        "cycle_rank": cycle_rank,
        "six_cycles": len(six_cycles),
        "connected": connected,
        "edge_min": min(edge_lengths),
        "edge_max": max(edge_lengths),
        "z_span": max(z_values) - min(z_values),
        "max_span": max_span,
    }

    gate = (
        report["cells"] == EXPECTED["cells"]
        and report["carbons"] == EXPECTED["carbons"]
        and report["edges"] == EXPECTED["edges"]
        and report["degree2"] == EXPECTED["degree2"]
        and report["degree3"] == EXPECTED["degree3"]
        and report["degree_keys"] == [2, 3]
        and report["boundary"] == EXPECTED["boundary"]
        and report["cycle_rank"] == EXPECTED["cycle_rank"]
        and report["six_cycles"] == EXPECTED["six_cycles"]
        and report["connected"]
        and max(
            abs(d - BOND)
            for d in edge_lengths
        ) < 1.0e-6
        and report["z_span"] < 1.0e-12
    )

    return gate, report, boundary


def write_xyz(path, coords):
    if path.exists():
        raise RuntimeError(
            "Refusing to overwrite existing file: {}".format(
                path
            )
        )

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with path.open("w") as handle:

        handle.write(
            "{}\n".format(
                len(coords)
            )
        )

        handle.write(
            "Deterministic ideal circumcoronene C54 carbon scaffold; "
            "C-C = {:.2f} A; planar graphene lattice\n".format(
                BOND
            )
        )

        for x, y, z in coords:

            handle.write(
                "C  {: .8f}  {: .8f}  {: .8f}\n".format(
                    x,
                    y,
                    z,
                )
            )


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Build and validate the ideal C54 carbon framework "
            "of circumcoronene."
        )
    )

    parser.add_argument(
        "--write",
        action="store_true",
        help=(
            "Write the validated scaffold XYZ. "
            "Without this flag, validation only is performed."
        ),
    )

    parser.add_argument(
        "--output",
        default=(
            "structures/prepared/"
            "circumcoronene_c54_scaffold_v01.xyz"
        ),
        help="XYZ output path used with --write.",
    )

    args = parser.parse_args()

    cells = build_cells()

    raw_vertices, ring_coords = build_raw_vertices(
        cells
    )

    ordered_xy, x0, y0 = canonicalize_vertices(
        raw_vertices
    )

    index = {
        xy: i
        for i, xy in enumerate(ordered_xy)
    }

    ring_ids = remap_ring_coords(
        ring_coords,
        x0,
        y0,
        index,
    )

    coords = [
        (x, y, 0.0)
        for x, y in ordered_xy
    ]

    edges, adj = build_graph(
        coords,
        ring_ids,
    )

    gate, report, boundary = validate(
        cells,
        coords,
        edges,
        adj,
    )

    print("===== CIRCUMCORONENE C54 VALIDATION =====")
    print(
        "hexagonal cells = {}".format(
            report["cells"]
        )
    )
    print(
        "carbon vertices = {}".format(
            report["carbons"]
        )
    )
    print(
        "C-C edges = {}".format(
            report["edges"]
        )
    )

    print()
    print("degree distribution:")
    print(
        "  degree 2 -> {}".format(
            report["degree2"]
        )
    )
    print(
        "  degree 3 -> {}".format(
            report["degree3"]
        )
    )

    print()
    print(
        "boundary carbons = {}".format(
            report["boundary"]
        )
    )
    print(
        "connected = {}".format(
            report["connected"]
        )
    )
    print(
        "cycle rank = {}".format(
            report["cycle_rank"]
        )
    )
    print(
        "six-membered cycles = {}".format(
            report["six_cycles"]
        )
    )

    print()
    print(
        "C-C edge length min = {:.6f} A".format(
            report["edge_min"]
        )
    )
    print(
        "C-C edge length max = {:.6f} A".format(
            report["edge_max"]
        )
    )
    print(
        "z span = {:.6f} A".format(
            report["z_span"]
        )
    )
    print(
        "maximum C...C span = {:.6f} A".format(
            report["max_span"]
        )
    )

    print()
    print(
        "boundary atom indices = {}".format(
            " ".join(
                str(i + 1)
                for i in boundary
            )
        )
    )

    print()
    print(
        "C54 GRAPH/LATTICE GATE = {}".format(
            "PASS" if gate else "FAIL"
        )
    )

    if not gate:
        raise SystemExit(
            "Validation failed; no output will be written."
        )

    if args.write:

        output = Path(args.output)

        write_xyz(
            output,
            coords,
        )

        print()
        print(
            "WROTE = {}".format(
                output
            )
        )

    else:

        print()
        print(
            "VALIDATION ONLY: no structure file written."
        )


if __name__ == "__main__":
    main()
