#!/usr/bin/env python3

import argparse
import hashlib
import math
from collections import Counter
from pathlib import Path


DEFAULT_INPUT = (
    "structures/prepared/"
    "circumcoronene_c54h18_v01.xyz"
)

EXPECTED_INPUT_SHA256 = (
    "226f0401e0a690645ca9d5d85304ebac"
    "51da41321fc953c5148a74ab938b072b"
)

DEFAULT_OUTPUTS = {
    "class1": (
        "structures/prepared/"
        "cooh_gqd_class1_c1_v01.xyz"
    ),
    "class2": (
        "structures/prepared/"
        "cooh_gqd_class2_c3_v01.xyz"
    ),
}

# Deterministic representative of each symmetry class.
#
# Indices below are zero-based source indices.
#
# Class 1:
#   source C1 / H55
#
# Class 2:
#   source C3 / H57
SITES = {
    "class1": {
        "parent_c": 0,
        "replaced_h": 54,
        "label": "Class 1 representative C1/H55",
    },
    "class2": {
        "parent_c": 2,
        "replaced_h": 56,
        "label": "Class 2 representative C3/H57",
    },
}


# Parent connectivity perception.
CC_MIN = 1.20
CC_MAX = 1.60

CH_MIN = 0.90
CH_MAX = 1.20


# Deterministic initial COOH geometry.
ARYL_C_COOH = 1.49
CO_DOUBLE = 1.23
CO_SINGLE = 1.36
OH_BOND = 0.97

COH_ANGLE = 108.0

# The prior clearance scan found +90 and 270 degrees
# to be mirror-related maxima. +90 is the deterministic
# construction convention.
COOH_TORSION = 90.0


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


def add(a, b):
    return tuple(
        a[k] + b[k]
        for k in range(3)
    )


def subtract(a, b):
    return tuple(
        a[k] - b[k]
        for k in range(3)
    )


def scale(v, scalar):
    return tuple(
        x * scalar
        for x in v
    )


def dot(a, b):
    return sum(
        a[k] * b[k]
        for k in range(3)
    )


def cross(a, b):
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )


def norm(v):
    return math.sqrt(
        dot(v, v)
    )


def unit(v):
    n = norm(v)

    if n < 1.0e-12:
        raise RuntimeError(
            "Cannot normalize zero-length vector."
        )

    return scale(
        v,
        1.0 / n,
    )


def angle_deg(v1, v2):
    cosine = (
        dot(v1, v2)
        / (
            norm(v1)
            * norm(v2)
        )
    )

    cosine = max(
        -1.0,
        min(1.0, cosine),
    )

    return math.degrees(
        math.acos(cosine)
    )


def rotate_xy(v, angle_deg_value):
    theta = math.radians(
        angle_deg_value
    )

    x, y, z = v

    return (
        x * math.cos(theta)
        - y * math.sin(theta),
        x * math.sin(theta)
        + y * math.cos(theta),
        z,
    )


def rotate_about_axis(
    point,
    origin,
    axis,
    angle_deg_value,
):
    theta = math.radians(
        angle_deg_value
    )

    vector = subtract(
        point,
        origin,
    )

    axis_unit = unit(
        axis
    )

    term1 = scale(
        vector,
        math.cos(theta),
    )

    term2 = scale(
        cross(
            axis_unit,
            vector,
        ),
        math.sin(theta),
    )

    term3 = scale(
        axis_unit,
        dot(
            axis_unit,
            vector,
        )
        * (
            1.0
            - math.cos(theta)
        ),
    )

    return add(
        origin,
        add(
            add(
                term1,
                term2,
            ),
            term3,
        ),
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


def validate_parent(elements, coords):
    if len(coords) != 72:
        raise RuntimeError(
            "Parent must contain 72 atoms."
        )

    if Counter(elements) != Counter({
        "C": 54,
        "H": 18,
    }):
        raise RuntimeError(
            "Parent formula is not C54H18."
        )

    if elements[:54] != ["C"] * 54:
        raise RuntimeError(
            "Parent C1-C54 ordering is invalid."
        )

    if elements[54:] != ["H"] * 18:
        raise RuntimeError(
            "Parent H55-H72 ordering is invalid."
        )

    carbon_indices = list(
        range(54)
    )

    hydrogen_indices = list(
        range(54, 72)
    )

    adjacency = {
        i: set()
        for i in carbon_indices
    }

    edges = []

    for i in carbon_indices:
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

    degree_counts = Counter(
        len(adjacency[i])
        for i in carbon_indices
    )

    boundary = sorted(
        i
        for i in carbon_indices
        if len(adjacency[i]) == 2
    )

    interior = sorted(
        i
        for i in carbon_indices
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

    if not (
        len(edges) == 72
        and degree_counts[2] == 18
        and degree_counts[3] == 36
        and sorted(degree_counts) == [2, 3]
        and len(boundary) == 18
        and len(interior) == 36
        and connected
        and cycle_rank == 19
    ):
        raise RuntimeError(
            "Parent carbon topology validation failed."
        )

    h_parent = {}

    for h in hydrogen_indices:

        candidates = []

        for c in boundary:

            d = distance(
                coords[h],
                coords[c],
            )

            if CH_MIN <= d <= CH_MAX:

                candidates.append(
                    (
                        d,
                        c,
                    )
                )

        if len(candidates) != 1:
            raise RuntimeError(
                "Parent H{} does not have exactly "
                "one boundary-carbon parent.".format(
                    h + 1
                )
            )

        h_parent[h] = (
            candidates[0][1]
        )

    parent_counts = Counter(
        h_parent.values()
    )

    if not all(
        parent_counts[c] == 1
        for c in boundary
    ):
        raise RuntimeError(
            "Boundary C-H mapping is incomplete."
        )

    if not all(
        parent_counts[c] == 0
        for c in interior
    ):
        raise RuntimeError(
            "An interior carbon is hydrogenated."
        )

    return {
        "adjacency": adjacency,
        "edges": edges,
        "boundary": boundary,
        "interior": interior,
        "h_parent": h_parent,
    }


def construct_candidate(
    site_name,
    elements,
    coords,
    parent_info,
):
    site = SITES[
        site_name
    ]

    parent_c = site[
        "parent_c"
    ]

    replaced_h = site[
        "replaced_h"
    ]

    h_parent = parent_info[
        "h_parent"
    ]

    if replaced_h not in h_parent:
        raise RuntimeError(
            "{} source H is not mapped.".format(
                site_name
            )
        )

    if h_parent[
        replaced_h
    ] != parent_c:
        raise RuntimeError(
            "{} source H/C mapping mismatch.".format(
                site_name
            )
        )

    if parent_c not in parent_info[
        "boundary"
    ]:
        raise RuntimeError(
            "{} parent carbon is not a boundary carbon.".format(
                site_name
            )
        )

    c_parent = coords[
        parent_c
    ]

    h_old = coords[
        replaced_h
    ]

    outward = unit(
        subtract(
            h_old,
            c_parent,
        )
    )

    c_cooh = add(
        c_parent,
        scale(
            outward,
            ARYL_C_COOH,
        ),
    )

    to_parent = scale(
        outward,
        -1.0,
    )

    carbonyl_dir = unit(
        rotate_xy(
            to_parent,
            +120.0,
        )
    )

    hydroxyl_dir = unit(
        rotate_xy(
            to_parent,
            -120.0,
        )
    )

    o_carbonyl_planar = add(
        c_cooh,
        scale(
            carbonyl_dir,
            CO_DOUBLE,
        ),
    )

    o_hydroxyl_planar = add(
        c_cooh,
        scale(
            hydroxyl_dir,
            CO_SINGLE,
        ),
    )

    oh_to_c = unit(
        subtract(
            c_cooh,
            o_hydroxyl_planar,
        )
    )

    scaffold_center = tuple(
        sum(
            coords[i][k]
            for i in range(54)
        ) / 54.0
        for k in range(3)
    )

    acid_h_candidates = []

    for sign in (
        -1.0,
        +1.0,
    ):

        h_dir = unit(
            rotate_xy(
                oh_to_c,
                sign * COH_ANGLE,
            )
        )

        h_candidate = add(
            o_hydroxyl_planar,
            scale(
                h_dir,
                OH_BOND,
            ),
        )

        acid_h_candidates.append(
            (
                distance(
                    h_candidate,
                    scaffold_center,
                ),
                h_candidate,
            )
        )

    acid_h_candidates.sort(
        key=lambda row: row[0],
        reverse=True,
    )

    h_acid_planar = (
        acid_h_candidates[0][1]
    )

    # Rotate the complete O/O/H portion rigidly around
    # the parent-C--C(COOH) axis.
    o_carbonyl = rotate_about_axis(
        o_carbonyl_planar,
        c_cooh,
        outward,
        COOH_TORSION,
    )

    o_hydroxyl = rotate_about_axis(
        o_hydroxyl_planar,
        c_cooh,
        outward,
        COOH_TORSION,
    )

    h_acid = rotate_about_axis(
        h_acid_planar,
        c_cooh,
        outward,
        COOH_TORSION,
    )


    # Standardized output ordering:
    #
    # C1-C54  = source scaffold C1-C54 unchanged
    # H55-H71 = retained source hydrogens in ascending
    #           source-index order
    # C72      = carboxyl carbon
    # O73      = carbonyl oxygen
    # O74      = hydroxyl oxygen
    # H75      = acidic hydrogen

    retained_h_source = [
        h
        for h in range(54, 72)
        if h != replaced_h
    ]

    output_elements = (
        ["C"] * 54
        + ["H"] * 17
        + ["C", "O", "O", "H"]
    )

    output_coords = (
        [
            coords[i]
            for i in range(54)
        ]
        + [
            coords[h]
            for h in retained_h_source
        ]
        + [
            c_cooh,
            o_carbonyl,
            o_hydroxyl,
            h_acid,
        ]
    )

    source_h_mapping = []

    for output_index, source_h in enumerate(
        retained_h_source,
        start=55,
    ):

        source_h_mapping.append(
            (
                output_index,
                source_h + 1,
            )
        )

    return {
        "site_name": site_name,
        "site_label": site[
            "label"
        ],
        "parent_c": parent_c,
        "replaced_h": replaced_h,
        "retained_h_source": retained_h_source,
        "source_h_mapping": source_h_mapping,
        "elements": output_elements,
        "coords": output_coords,
        "c_parent": c_parent,
        "c_cooh": c_cooh,
        "o_carbonyl": o_carbonyl,
        "o_hydroxyl": o_hydroxyl,
        "h_acid": h_acid,
    }


def validate_candidate(
    candidate,
    source_elements,
    source_coords,
):
    elements = candidate[
        "elements"
    ]

    coords = candidate[
        "coords"
    ]

    parent_c = candidate[
        "parent_c"
    ]

    replaced_h = candidate[
        "replaced_h"
    ]

    c_parent = candidate[
        "c_parent"
    ]

    c_cooh = candidate[
        "c_cooh"
    ]

    o_carbonyl = candidate[
        "o_carbonyl"
    ]

    o_hydroxyl = candidate[
        "o_hydroxyl"
    ]

    h_acid = candidate[
        "h_acid"
    ]

    retained_h_source = candidate[
        "retained_h_source"
    ]


    formula = Counter(
        elements
    )

    ordering_pass = (
        elements[:54] == ["C"] * 54
        and elements[54:71] == ["H"] * 17
        and elements[71:] == [
            "C",
            "O",
            "O",
            "H",
        ]
    )


    scaffold_unchanged = all(
        distance(
            coords[i],
            source_coords[i],
        ) < 1.0e-12
        for i in range(54)
    )


    retained_h_unchanged = True

    for output_zero_index, source_h in enumerate(
        retained_h_source,
        start=54,
    ):

        if distance(
            coords[output_zero_index],
            source_coords[source_h],
        ) >= 1.0e-12:

            retained_h_unchanged = False


    # Internal COOH geometry.
    parent_cc = distance(
        c_parent,
        c_cooh,
    )

    co_double = distance(
        c_cooh,
        o_carbonyl,
    )

    co_single = distance(
        c_cooh,
        o_hydroxyl,
    )

    oh = distance(
        o_hydroxyl,
        h_acid,
    )


    v_parent = subtract(
        c_parent,
        c_cooh,
    )

    v_carbonyl = subtract(
        o_carbonyl,
        c_cooh,
    )

    v_hydroxyl = subtract(
        o_hydroxyl,
        c_cooh,
    )

    v_oh_c = subtract(
        c_cooh,
        o_hydroxyl,
    )

    v_oh_h = subtract(
        h_acid,
        o_hydroxyl,
    )


    parent_o1_angle = angle_deg(
        v_parent,
        v_carbonyl,
    )

    parent_o2_angle = angle_deg(
        v_parent,
        v_hydroxyl,
    )

    oco_angle = angle_deg(
        v_carbonyl,
        v_hydroxyl,
    )

    coh_angle = angle_deg(
        v_oh_c,
        v_oh_h,
    )


    # Group-plane relationship to the graphene xy plane.
    group_normal = unit(
        cross(
            subtract(
                c_parent,
                c_cooh,
            ),
            subtract(
                o_carbonyl,
                c_cooh,
            ),
        )
    )

    scaffold_normal = (
        0.0,
        0.0,
        1.0,
    )

    normal_angle = angle_deg(
        group_normal,
        scaffold_normal,
    )

    plane_angle = min(
        normal_angle,
        180.0 - normal_angle,
    )


    # Retained source structure:
    # all source atoms except the replaced edge H.
    retained_source = [
        (
            i,
            source_elements[i],
            source_coords[i],
        )
        for i in range(
            len(source_coords)
        )
        if i != replaced_h
    ]


    # Steric/contact diagnostics.
    ccooh_contacts = []

    for i, el, xyz in retained_source:

        if i == parent_c:
            continue

        ccooh_contacts.append(
            (
                distance(
                    c_cooh,
                    xyz,
                ),
                i,
                el,
            )
        )

    ccooh_contacts.sort()

    ccooh_min = (
        ccooh_contacts[0]
    )


    oxygen_contacts = []

    for name, oxygen_xyz in (
        ("O73", o_carbonyl),
        ("O74", o_hydroxyl),
    ):

        for i, el, xyz in retained_source:

            # Parent carbon is a 1,3 intramolecular relation
            # through the carboxyl carbon and is therefore
            # not used as the edge-clearance discriminator.
            if i == parent_c:
                continue

            oxygen_contacts.append(
                (
                    distance(
                        oxygen_xyz,
                        xyz,
                    ),
                    name,
                    i,
                    el,
                )
            )

    oxygen_contacts.sort()

    oxygen_min = (
        oxygen_contacts[0]
    )


    acid_h_contacts = []

    for i, el, xyz in retained_source:

        acid_h_contacts.append(
            (
                distance(
                    h_acid,
                    xyz,
                ),
                i,
                el,
            )
        )

    acid_h_contacts.sort()

    acid_h_min = (
        acid_h_contacts[0]
    )


    # Carbon scaffold must remain exactly planar.
    scaffold_z = [
        coords[i][2]
        for i in range(54)
    ]

    scaffold_z_span = (
        max(scaffold_z)
        - min(scaffold_z)
    )


    # The +90-degree construction must place the
    # COOH O/O/H atoms out of the parent plane.
    group_abs_z_max = max(
        abs(
            o_carbonyl[2]
        ),
        abs(
            o_hydroxyl[2]
        ),
        abs(
            h_acid[2]
        ),
    )


    gate = (
        len(coords) == 75
        and formula == Counter({
            "C": 55,
            "H": 18,
            "O": 2,
        })
        and ordering_pass
        and scaffold_unchanged
        and retained_h_unchanged
        and len(
            retained_h_source
        ) == 17
        and abs(
            parent_cc
            - ARYL_C_COOH
        ) < 1.0e-8
        and abs(
            co_double
            - CO_DOUBLE
        ) < 1.0e-8
        and abs(
            co_single
            - CO_SINGLE
        ) < 1.0e-8
        and abs(
            oh
            - OH_BOND
        ) < 1.0e-8
        and abs(
            parent_o1_angle
            - 120.0
        ) < 1.0e-6
        and abs(
            parent_o2_angle
            - 120.0
        ) < 1.0e-6
        and abs(
            oco_angle
            - 120.0
        ) < 1.0e-6
        and abs(
            coh_angle
            - COH_ANGLE
        ) < 1.0e-6
        and abs(
            plane_angle
            - 90.0
        ) < 1.0e-6
        and ccooh_min[0] > 2.0
        and oxygen_min[0] > 2.5
        and acid_h_min[0] > 2.0
        and scaffold_z_span < 1.0e-10
        and group_abs_z_max > 0.50
    )


    return {
        "gate": gate,
        "formula": formula,
        "total_atoms": len(coords),
        "ordering_pass": ordering_pass,
        "scaffold_unchanged": scaffold_unchanged,
        "retained_h_unchanged": retained_h_unchanged,
        "parent_cc": parent_cc,
        "co_double": co_double,
        "co_single": co_single,
        "oh": oh,
        "parent_o1_angle": parent_o1_angle,
        "parent_o2_angle": parent_o2_angle,
        "oco_angle": oco_angle,
        "coh_angle": coh_angle,
        "plane_angle": plane_angle,
        "ccooh_min": ccooh_min,
        "oxygen_min": oxygen_min,
        "acid_h_min": acid_h_min,
        "scaffold_z_span": scaffold_z_span,
        "group_abs_z_max": group_abs_z_max,
    }


def write_xyz(
    path,
    candidate,
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

    elements = candidate[
        "elements"
    ]

    coords = candidate[
        "coords"
    ]

    with path.open("w") as handle:

        handle.write(
            "{}\n".format(
                len(coords)
            )
        )

        handle.write(
            "Deterministic monocarboxylated circumcoronene "
            "{}; source C54H18 SHA256={}; "
            "torsion=+{:.1f} deg; "
            "output COOH atoms=C72/O73/O74/H75\n".format(
                candidate[
                    "site_name"
                ],
                source_sha,
                COOH_TORSION,
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


def print_candidate_report(
    candidate,
    report,
):
    print(
        "===== {} =====".format(
            candidate[
                "site_name"
            ].upper()
        )
    )

    print(
        "representative = {}".format(
            candidate[
                "site_label"
            ]
        )
    )

    print(
        "source substitution = C{} / H{}".format(
            candidate[
                "parent_c"
            ] + 1,
            candidate[
                "replaced_h"
            ] + 1,
        )
    )

    print(
        "COOH starting torsion = +{:.1f} deg".format(
            COOH_TORSION
        )
    )

    print()
    print(
        "formula = {}".format(
            dict(
                report[
                    "formula"
                ]
            )
        )
    )

    print(
        "total atoms = {}".format(
            report[
                "total_atoms"
            ]
        )
    )

    print(
        "standard output ordering = {}".format(
            report[
                "ordering_pass"
            ]
        )
    )

    print(
        "C1-C54 scaffold unchanged = {}".format(
            report[
                "scaffold_unchanged"
            ]
        )
    )

    print(
        "retained parent H coordinates unchanged = {}".format(
            report[
                "retained_h_unchanged"
            ]
        )
    )

    print()
    print("standardized functional-group indices:")
    print("  C72 = carboxyl carbon")
    print("  O73 = carbonyl oxygen")
    print("  O74 = hydroxyl oxygen")
    print("  H75 = acidic hydrogen")

    print()
    print("retained parent-H mapping:")

    for output_h, source_h in candidate[
        "source_h_mapping"
    ]:

        print(
            "  output H{:>2} <- source H{:>2}".format(
                output_h,
                source_h,
            )
        )

    print()
    print("COOH starting geometry:")

    print(
        "  C_parent-C72 = {:.8f} A".format(
            report[
                "parent_cc"
            ]
        )
    )

    print(
        "  C72=O73 = {:.8f} A".format(
            report[
                "co_double"
            ]
        )
    )

    print(
        "  C72-O74 = {:.8f} A".format(
            report[
                "co_single"
            ]
        )
    )

    print(
        "  O74-H75 = {:.8f} A".format(
            report[
                "oh"
            ]
        )
    )

    print(
        "  Cparent-C72-O73 = {:.6f} deg".format(
            report[
                "parent_o1_angle"
            ]
        )
    )

    print(
        "  Cparent-C72-O74 = {:.6f} deg".format(
            report[
                "parent_o2_angle"
            ]
        )
    )

    print(
        "  O73-C72-O74 = {:.6f} deg".format(
            report[
                "oco_angle"
            ]
        )
    )

    print(
        "  C72-O74-H75 = {:.6f} deg".format(
            report[
                "coh_angle"
            ]
        )
    )

    print(
        "  COOH/scaffold plane angle = {:.6f} deg".format(
            report[
                "plane_angle"
            ]
        )
    )

    print()
    print("clearance diagnostics:")

    ccooh_d, ccooh_i, ccooh_el = (
        report[
            "ccooh_min"
        ]
    )

    print(
        "  C72 nearest non-parent atom = "
        "{}{} at {:.8f} A".format(
            ccooh_el,
            ccooh_i + 1,
            ccooh_d,
        )
    )

    (
        oxygen_d,
        oxygen_name,
        oxygen_i,
        oxygen_el,
    ) = report[
        "oxygen_min"
    ]

    print(
        "  nearest O/parent-edge contact = "
        "{} -> {}{} at {:.8f} A".format(
            oxygen_name,
            oxygen_el,
            oxygen_i + 1,
            oxygen_d,
        )
    )

    acid_h_d, acid_h_i, acid_h_el = (
        report[
            "acid_h_min"
        ]
    )

    print(
        "  H75 nearest retained atom = "
        "{}{} at {:.8f} A".format(
            acid_h_el,
            acid_h_i + 1,
            acid_h_d,
        )
    )

    print(
        "  scaffold z span = {:.8f} A".format(
            report[
                "scaffold_z_span"
            ]
        )
    )

    print(
        "  max |z| in COOH O/O/H = {:.8f} A".format(
            report[
                "group_abs_z_max"
            ]
        )
    )

    print()
    print(
        "{} COOH CONSTRUCTION GATE = {}".format(
            candidate[
                "site_name"
            ].upper(),
            (
                "PASS"
                if report[
                    "gate"
                ]
                else "FAIL"
            ),
        )
    )


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Construct deterministic Class-1 and Class-2 "
            "monocarboxylated circumcoronene candidates."
        )
    )

    parser.add_argument(
        "--input",
        default=DEFAULT_INPUT,
        help="Validated C54H18 parent XYZ.",
    )

    parser.add_argument(
        "--site",
        choices=[
            "class1",
            "class2",
            "both",
        ],
        default="both",
        help=(
            "Symmetry-class representative to construct. "
            "Default: both."
        ),
    )

    parser.add_argument(
        "--write",
        action="store_true",
        help=(
            "Write validated XYZ candidate(s). "
            "Without this flag, validation only is performed."
        ),
    )

    args = parser.parse_args()

    input_path = Path(
        args.input
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
        and source_sha
        != EXPECTED_INPUT_SHA256
    ):
        raise RuntimeError(
            "Default parent checksum mismatch.\n"
            "Expected: {}\n"
            "Observed: {}".format(
                EXPECTED_INPUT_SHA256,
                source_sha,
            )
        )

    elements, coords = read_xyz(
        input_path
    )

    parent_info = validate_parent(
        elements,
        coords,
    )

    if args.site == "both":
        requested_sites = [
            "class1",
            "class2",
        ]
    else:
        requested_sites = [
            args.site
        ]

    print(
        "===== DETERMINISTIC COOH FUNCTIONALIZATION ====="
    )

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

    print(
        "torsion convention = +{:.1f} deg".format(
            COOH_TORSION
        )
    )

    print()

    candidates = []

    for site_name in requested_sites:

        candidate = construct_candidate(
            site_name,
            elements,
            coords,
            parent_info,
        )

        report = validate_candidate(
            candidate,
            elements,
            coords,
        )

        print_candidate_report(
            candidate,
            report,
        )

        print()

        if not report[
            "gate"
        ]:
            raise SystemExit(
                "{} validation failed; "
                "no output will be written.".format(
                    site_name
                )
            )

        candidates.append(
            candidate
        )

    if args.write:

        for candidate in candidates:

            output_path = Path(
                DEFAULT_OUTPUTS[
                    candidate[
                        "site_name"
                    ]
                ]
            )

            write_xyz(
                output_path,
                candidate,
                source_sha,
            )

            print(
                "WROTE = {}".format(
                    output_path
                )
            )

    else:

        print(
            "VALIDATION ONLY: no COOH-GQD "
            "structure files written."
        )


if __name__ == "__main__":
    main()
