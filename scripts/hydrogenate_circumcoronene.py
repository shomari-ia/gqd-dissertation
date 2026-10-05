#!/usr/bin/env python3

import argparse
import hashlib
import math
from collections import Counter
from pathlib import Path


DEFAULT_INPUT = (
    "structures/prepared/"
    "circumcoronene_c54_scaffold_v01.xyz"
)

DEFAULT_OUTPUT = (
    "structures/prepared/"
    "circumcoronene_c54h18_v01.xyz"
)

EXPECTED_INPUT_SHA256 = (
    "c48d2b9c3f7ac58d59cbda613d3304c9"
    "b823737f551aa2179bb341bf9de0203f"
)

CC_MIN = 1.20
CC_MAX = 1.60
CH_BOND = 1.09


def sha256_file(path):
    h = hashlib.sha256()

    with path.open("rb") as handle:
        for block in iter(
            lambda: handle.read(1024 * 1024),
            b"",
        ):
            h.update(block)

    return h.hexdigest()


def distance(a, b):
    return math.sqrt(
        sum(
            (a[k] - b[k]) ** 2
            for k in range(3)
        )
    )


def unit(vector):
    norm = math.sqrt(
        sum(
            value * value
            for value in vector
        )
    )

    if norm < 1.0e-12:
        raise RuntimeError(
            "Cannot normalize zero-length vector."
        )

    return tuple(
        value / norm
        for value in vector
    )


def angle_deg(v1, v2):
    dot = sum(
        v1[k] * v2[k]
        for k in range(3)
    )

    n1 = math.sqrt(
        sum(
            x * x
            for x in v1
        )
    )

    n2 = math.sqrt(
        sum(
            x * x
            for x in v2
        )
    )

    cosine = dot / (n1 * n2)

    cosine = max(
        -1.0,
        min(1.0, cosine),
    )

    return math.degrees(
        math.acos(cosine)
    )


def read_xyz(path):
    lines = path.read_text().splitlines()

    if len(lines) < 2:
        raise RuntimeError(
            "XYZ file is incomplete."
        )

    declared = int(
        lines[0].strip()
    )

    elements = []
    coords = []

    for line in lines[2:]:

        fields = line.split()

        if len(fields) != 4:
            raise RuntimeError(
                "Malformed XYZ coordinate line: {}".format(
                    line
                )
            )

        elements.append(
            fields[0]
        )

        coords.append(
            (
                float(fields[1]),
                float(fields[2]),
                float(fields[3]),
            )
        )

    if declared != len(coords):
        raise RuntimeError(
            "Declared atom count {} != parsed atom count {}".format(
                declared,
                len(coords),
            )
        )

    return elements, coords


def infer_carbon_graph(elements, coords):
    if Counter(elements) != Counter({"C": 54}):
        raise RuntimeError(
            "Input must contain exactly C54."
        )

    adjacency = {
        i: set()
        for i in range(54)
    }

    edges = []

    for i in range(54):
        for j in range(i + 1, 54):

            d = distance(
                coords[i],
                coords[j],
            )

            if CC_MIN <= d <= CC_MAX:

                adjacency[i].add(j)
                adjacency[j].add(i)

                edges.append(
                    (i, j)
                )

    return adjacency, edges


def validate_c54(adjacency, edges):
    degree_counts = Counter(
        len(adjacency[i])
        for i in adjacency
    )

    boundary = sorted(
        i
        for i in adjacency
        if len(adjacency[i]) == 2
    )

    interior = sorted(
        i
        for i in adjacency
        if len(adjacency[i]) == 3
    )

    seen = {0}
    stack = [0]

    while stack:

        i = stack.pop()

        for j in adjacency[i]:

            if j not in seen:
                seen.add(j)
                stack.append(j)

    connected = (
        len(seen) == 54
    )

    cycle_rank = (
        len(edges) - 54 + 1
        if connected
        else None
    )

    gate = (
        len(edges) == 72
        and degree_counts[2] == 18
        and degree_counts[3] == 36
        and sorted(degree_counts) == [2, 3]
        and len(boundary) == 18
        and len(interior) == 36
        and connected
        and cycle_rank == 19
    )

    if not gate:
        raise RuntimeError(
            "Input C54 scaffold topology validation failed."
        )

    return boundary, interior


def add_hydrogens(coords, adjacency, boundary):
    hydrogens = []
    parent_map = []

    for carbon in boundary:

        carbon_xyz = coords[carbon]

        neighbors = sorted(
            adjacency[carbon]
        )

        if len(neighbors) != 2:
            raise RuntimeError(
                "Boundary carbon C{} does not have "
                "exactly two carbon neighbors.".format(
                    carbon + 1
                )
            )

        directions = []

        for neighbor in neighbors:

            vector = tuple(
                coords[neighbor][k]
                - carbon_xyz[k]
                for k in range(3)
            )

            directions.append(
                unit(vector)
            )

        inward = tuple(
            directions[0][k]
            + directions[1][k]
            for k in range(3)
        )

        outward = unit(
            tuple(
                -value
                for value in inward
            )
        )

        hydrogen_xyz = tuple(
            carbon_xyz[k]
            + CH_BOND * outward[k]
            for k in range(3)
        )

        hydrogens.append(
            hydrogen_xyz
        )

        parent_map.append(
            (
                carbon,
                neighbors,
            )
        )

    return hydrogens, parent_map


def validate_hydrogenation(
    carbon_coords,
    hydrogens,
    parent_map,
):
    combined_elements = (
        ["C"] * 54
        + ["H"] * len(hydrogens)
    )

    combined_coords = (
        carbon_coords
        + hydrogens
    )

    ch_lengths = []
    hcc_angles = []

    nearest_parent_pass = True
    nearest_nonparent_c = float("inf")

    for h_local, (carbon, neighbors) in enumerate(
        parent_map
    ):

        hydrogen_xyz = hydrogens[h_local]
        carbon_xyz = carbon_coords[carbon]

        ch_lengths.append(
            distance(
                carbon_xyz,
                hydrogen_xyz,
            )
        )

        vh = tuple(
            hydrogen_xyz[k]
            - carbon_xyz[k]
            for k in range(3)
        )

        for neighbor in neighbors:

            vc = tuple(
                carbon_coords[neighbor][k]
                - carbon_xyz[k]
                for k in range(3)
            )

            hcc_angles.append(
                angle_deg(
                    vh,
                    vc,
                )
            )

        carbon_distances = sorted(
            (
                distance(
                    hydrogen_xyz,
                    carbon_coords[c],
                ),
                c,
            )
            for c in range(54)
        )

        nearest_distance, nearest_carbon = (
            carbon_distances[0]
        )

        if nearest_carbon != carbon:
            nearest_parent_pass = False

        if abs(
            nearest_distance - CH_BOND
        ) > 1.0e-8:
            nearest_parent_pass = False

        for d, c in carbon_distances:

            if c != carbon:
                nearest_nonparent_c = min(
                    nearest_nonparent_c,
                    d,
                )

    min_hh = float("inf")

    for i in range(len(hydrogens)):
        for j in range(i + 1, len(hydrogens)):

            min_hh = min(
                min_hh,
                distance(
                    hydrogens[i],
                    hydrogens[j],
                ),
            )

    z_values = [
        xyz[2]
        for xyz in combined_coords
    ]

    z_span = (
        max(z_values)
        - min(z_values)
    )

    coordinate_set = {
        (
            element,
            round(x, 8),
            round(y, 8),
            round(z, 8),
        )
        for element, (x, y, z)
        in zip(
            combined_elements,
            combined_coords,
        )
    }

    centrosymmetric = all(
        (
            element,
            round(-x, 8),
            round(-y, 8),
            round(-z, 8),
        )
        in coordinate_set
        for element, (x, y, z)
        in zip(
            combined_elements,
            combined_coords,
        )
    )

    formula = Counter(
        combined_elements
    )

    gate = (
        len(hydrogens) == 18
        and len(combined_coords) == 72
        and formula == Counter({
            "C": 54,
            "H": 18,
        })
        and max(
            abs(d - CH_BOND)
            for d in ch_lengths
        ) < 1.0e-8
        and min(hcc_angles) > 119.999
        and max(hcc_angles) < 120.001
        and nearest_parent_pass
        and nearest_nonparent_c > 1.70
        and min_hh > 1.50
        and z_span < 1.0e-10
        and centrosymmetric
    )

    report = {
        "formula": formula,
        "total_atoms": len(combined_coords),
        "hydrogens": len(hydrogens),
        "ch_min": min(ch_lengths),
        "ch_max": max(ch_lengths),
        "angle_min": min(hcc_angles),
        "angle_max": max(hcc_angles),
        "nearest_parent_pass": nearest_parent_pass,
        "nearest_nonparent_c": nearest_nonparent_c,
        "min_hh": min_hh,
        "z_span": z_span,
        "centrosymmetric": centrosymmetric,
    }

    return (
        gate,
        report,
        combined_elements,
        combined_coords,
    )


def write_xyz(
    path,
    elements,
    coords,
    source_sha,
):
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
            "Deterministic ideal circumcoronene C54H18; "
            "source C54 SHA256={}; "
            "initial C-H={:.2f} A; planar\n".format(
                source_sha,
                CH_BOND,
            )
        )

        for element, (x, y, z) in zip(
            elements,
            coords,
        ):

            handle.write(
                "{}  {: .8f}  {: .8f}  {: .8f}\n".format(
                    element,
                    x,
                    y,
                    z,
                )
            )


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Deterministically hydrogenate a validated "
            "circumcoronene C54 carbon scaffold to C54H18."
        )
    )

    parser.add_argument(
        "--input",
        default=DEFAULT_INPUT,
        help="Validated C54 XYZ source.",
    )

    parser.add_argument(
        "--output",
        default=DEFAULT_OUTPUT,
        help="C54H18 XYZ output used with --write.",
    )

    parser.add_argument(
        "--write",
        action="store_true",
        help=(
            "Write the validated C54H18 XYZ. "
            "Without this flag, validation only is performed."
        ),
    )

    args = parser.parse_args()

    input_path = Path(
        args.input
    )

    output_path = Path(
        args.output
    )

    if not input_path.exists():
        raise RuntimeError(
            "Input does not exist: {}".format(
                input_path
            )
        )

    source_sha = sha256_file(
        input_path
    )

    if (
        str(input_path) == DEFAULT_INPUT
        and source_sha != EXPECTED_INPUT_SHA256
    ):
        raise RuntimeError(
            "Default C54 scaffold checksum mismatch.\n"
            "Expected: {}\n"
            "Observed: {}".format(
                EXPECTED_INPUT_SHA256,
                source_sha,
            )
        )

    elements, carbon_coords = read_xyz(
        input_path
    )

    adjacency, edges = infer_carbon_graph(
        elements,
        carbon_coords,
    )

    boundary, interior = validate_c54(
        adjacency,
        edges,
    )

    hydrogens, parent_map = add_hydrogens(
        carbon_coords,
        adjacency,
        boundary,
    )

    (
        gate,
        report,
        combined_elements,
        combined_coords,
    ) = validate_hydrogenation(
        carbon_coords,
        hydrogens,
        parent_map,
    )

    print("===== CIRCUMCORONENE C54H18 VALIDATION =====")
    print(
        "source = {}".format(
            input_path
        )
    )
    print(
        "source SHA256 = {}".format(
            source_sha
        )
    )

    print()
    print(
        "input carbons = {}".format(
            len(carbon_coords)
        )
    )
    print(
        "C-C edges = {}".format(
            len(edges)
        )
    )
    print(
        "boundary carbons = {}".format(
            len(boundary)
        )
    )
    print(
        "interior carbons = {}".format(
            len(interior)
        )
    )
    print(
        "hydrogens generated = {}".format(
            report["hydrogens"]
        )
    )
    print(
        "total atoms = {}".format(
            report["total_atoms"]
        )
    )
    print(
        "formula = {}".format(
            dict(report["formula"])
        )
    )

    print()
    print(
        "C-H min = {:.8f} A".format(
            report["ch_min"]
        )
    )
    print(
        "C-H max = {:.8f} A".format(
            report["ch_max"]
        )
    )
    print(
        "H-C-C angle min = {:.6f} deg".format(
            report["angle_min"]
        )
    )
    print(
        "H-C-C angle max = {:.6f} deg".format(
            report["angle_max"]
        )
    )

    print()
    print(
        "nearest-H-parent check = {}".format(
            report["nearest_parent_pass"]
        )
    )
    print(
        "nearest non-parent H...C = {:.6f} A".format(
            report["nearest_nonparent_c"]
        )
    )
    print(
        "minimum H...H = {:.6f} A".format(
            report["min_hh"]
        )
    )

    print()
    print(
        "z span = {:.8f} A".format(
            report["z_span"]
        )
    )
    print(
        "centrosymmetric coordinates = {}".format(
            report["centrosymmetric"]
        )
    )

    print()
    print("hydrogen parent mapping:")

    for h_index, (carbon, neighbors) in enumerate(
        parent_map,
        start=55,
    ):

        print(
            "  H{:>2} -> C{:>2}  "
            "(C neighbors: C{:>2}, C{:>2})".format(
                h_index,
                carbon + 1,
                neighbors[0] + 1,
                neighbors[1] + 1,
            )
        )

    print()
    print(
        "C54H18 HYDROGENATION GATE = {}".format(
            "PASS" if gate else "FAIL"
        )
    )

    if not gate:
        raise SystemExit(
            "Hydrogenation validation failed; "
            "no output will be written."
        )

    if args.write:

        write_xyz(
            output_path,
            combined_elements,
            combined_coords,
            source_sha,
        )

        print()
        print(
            "WROTE = {}".format(
                output_path
            )
        )

    else:

        print()
        print(
            "VALIDATION ONLY: no C54H18 structure file written."
        )


if __name__ == "__main__":
    main()
