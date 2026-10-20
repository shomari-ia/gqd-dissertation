#!/usr/bin/env python3

from collections import Counter
from hashlib import sha256
from pathlib import Path

import numpy as np


GQD_PATH = Path(
    "structures/optimized/cooh_gqd_class1_c1_b3lyp_optfreq_v03.xyz"
)
DRUG_PATH = Path(
    "structures/accepted/erlotinib_b3lyp_accepted.xyz"
)
OUT_DIR = Path("structures/complexes_corrected")

EXPECTED_GQD_SHA256 = (
    "67e3c0968faec4b251d0801315273a6a5ed2d34c2536abda7460982e29c0f3c9"
)
EXPECTED_DRUG_SHA256 = (
    "d203adfb4d245f8ef5e9a33248612e348e64ad49f5b1673711fec87cc68c939a"
)

GQD_ATOMS = 75
DRUG_ATOMS = 52
COMPLEX_ATOMS = 127

GQD_FORMULA = Counter({"C": 55, "H": 18, "O": 2})
DRUG_FORMULA = Counter({"C": 22, "H": 23, "N": 3, "O": 4})

CORE_IDX = [6, 7, 8, 9, 10, 11, 12, 13, 14, 18]

FLAT_CORE_SEPARATION = 3.90
FLAT_AZIMUTH_DEG = 209.00

SLIPPED_CORE_SEPARATION = 3.40
SLIPPED_AZIMUTH_DEG = 324.00
SLIP_DISTANCE = 2.50

HEAVY_CLASH_GATE = 2.00
BASAL_ALL_ATOM_GATE = 2.00

EDGE_HN_DISTANCE = 1.90
EDGE_TWIST_DEG = 260.00


def file_sha256(path):
    h = sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def read_xyz(path):
    lines = path.read_text().splitlines()

    if len(lines) < 2:
        raise ValueError(f"Malformed XYZ: {path}")

    natoms = int(lines[0].strip())
    coord_lines = [line for line in lines[2:] if line.strip()]

    if len(coord_lines) != natoms:
        raise ValueError(
            f"{path}: header says {natoms} atoms but "
            f"{len(coord_lines)} coordinate lines were found"
        )

    atoms = []

    for line in coord_lines:
        fields = line.split()

        if len(fields) < 4:
            raise ValueError(f"Malformed coordinate line: {line}")

        element = fields[0]
        xyz = np.array(
            [float(fields[1]), float(fields[2]), float(fields[3])],
            dtype=float,
        )

        atoms.append((element, xyz))

    return natoms, atoms, coord_lines


def fit_plane(coords):
    centroid = coords.mean(axis=0)
    centered = coords - centroid

    _, _, vh = np.linalg.svd(centered, full_matrices=False)

    normal = vh[-1]
    normal /= np.linalg.norm(normal)

    return centroid, normal


def rotation_from_to(a, b):
    a = a / np.linalg.norm(a)
    b = b / np.linalg.norm(b)

    cross = np.cross(a, b)
    dot = np.clip(np.dot(a, b), -1.0, 1.0)

    if np.isclose(dot, 1.0):
        return np.eye(3)

    if np.isclose(dot, -1.0):
        trial = np.array([1.0, 0.0, 0.0])

        if abs(np.dot(a, trial)) > 0.9:
            trial = np.array([0.0, 1.0, 0.0])

        axis = np.cross(a, trial)
        axis /= np.linalg.norm(axis)

        K = np.array(
            [
                [0.0, -axis[2], axis[1]],
                [axis[2], 0.0, -axis[0]],
                [-axis[1], axis[0], 0.0],
            ]
        )

        return np.eye(3) + 2.0 * (K @ K)

    s = np.linalg.norm(cross)

    K = np.array(
        [
            [0.0, -cross[2], cross[1]],
            [cross[2], 0.0, -cross[0]],
            [-cross[1], cross[0], 0.0],
        ]
    )

    return np.eye(3) + K + K @ K * ((1.0 - dot) / (s * s))


def axis_rotation(axis, angle_deg):
    axis = axis / np.linalg.norm(axis)
    angle = np.radians(angle_deg)

    K = np.array(
        [
            [0.0, -axis[2], axis[1]],
            [axis[2], 0.0, -axis[0]],
            [-axis[1], axis[0], 0.0],
        ]
    )

    return (
        np.eye(3)
        + np.sin(angle) * K
        + (1.0 - np.cos(angle)) * (K @ K)
    )


def heavy_minimum(gqd_atoms, drug_elements, drug_xyz):
    best = None

    for gi, (gel, gxyz) in enumerate(gqd_atoms, start=1):
        if gel == "H":
            continue

        for di, (del_, dxyz) in enumerate(
            zip(drug_elements, drug_xyz),
            start=1,
        ):
            if del_ == "H":
                continue

            distance = np.linalg.norm(gxyz - dxyz)

            if best is None or distance < best[0]:
                best = (distance, gi, gel, di, del_)

    return best


def all_atom_minimum(gqd_atoms, drug_elements, drug_xyz):
    best = None

    for gi, (gel, gxyz) in enumerate(gqd_atoms, start=1):
        for di, (del_, dxyz) in enumerate(
            zip(drug_elements, drug_xyz),
            start=1,
        ):
            distance = np.linalg.norm(gxyz - dxyz)

            if best is None or distance < best[0]:
                best = (distance, gi, gel, di, del_)

    return best


def max_pairwise_distance_error(original, transformed):
    max_error = 0.0

    for i in range(len(original)):
        for j in range(i + 1, len(original)):
            d0 = np.linalg.norm(original[i] - original[j])
            d1 = np.linalg.norm(transformed[i] - transformed[j])
            max_error = max(max_error, abs(d1 - d0))

    return max_error


def write_complex(
    path,
    comment,
    gqd_raw_lines,
    drug_elements,
    drug_xyz,
):
    with path.open("w") as handle:
        handle.write(f"{COMPLEX_ATOMS}\n")
        handle.write(comment + "\n")

        # Preserve authoritative GQD coordinate records exactly.
        for line in gqd_raw_lines:
            handle.write(line.rstrip() + "\n")

        # Erlotinib is rigidly rotated/translated from accepted geometry.
        for element, xyz in zip(drug_elements, drug_xyz):
            handle.write(
                f"{element:<2} "
                f"{xyz[0]: .10f} "
                f"{xyz[1]: .10f} "
                f"{xyz[2]: .10f}\n"
            )


def formula(atoms):
    return Counter(element for element, _ in atoms)


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    gqd_sha = file_sha256(GQD_PATH)
    drug_sha = file_sha256(DRUG_PATH)

    if gqd_sha != EXPECTED_GQD_SHA256:
        raise RuntimeError(
            "Authoritative GQD SHA256 mismatch:\n"
            f"expected {EXPECTED_GQD_SHA256}\n"
            f"observed {gqd_sha}"
        )

    if drug_sha != EXPECTED_DRUG_SHA256:
        raise RuntimeError(
            "Accepted Erlotinib SHA256 mismatch:\n"
            f"expected {EXPECTED_DRUG_SHA256}\n"
            f"observed {drug_sha}"
        )

    gqd_natoms, gqd, gqd_raw = read_xyz(GQD_PATH)
    drug_natoms, drug, _ = read_xyz(DRUG_PATH)

    if gqd_natoms != GQD_ATOMS:
        raise RuntimeError(
            f"Expected {GQD_ATOMS} GQD atoms; found {gqd_natoms}"
        )

    if drug_natoms != DRUG_ATOMS:
        raise RuntimeError(
            f"Expected {DRUG_ATOMS} Erlotinib atoms; found {drug_natoms}"
        )

    if formula(gqd) != GQD_FORMULA:
        raise RuntimeError(
            f"Unexpected GQD formula counts: {formula(gqd)}"
        )

    if formula(drug) != DRUG_FORMULA:
        raise RuntimeError(
            f"Unexpected Erlotinib formula counts: {formula(drug)}"
        )

    gqd_xyz = np.array([xyz for _, xyz in gqd])
    drug_elements = [element for element, _ in drug]
    drug_xyz = np.array([xyz for _, xyz in drug])

    # Corrected GQD basal plane, C1-C54.
    scaffold = gqd_xyz[:54]
    gqd_centroid, gqd_normal = fit_plane(scaffold)

    # Canonical normal orientation for reproducibility.
    if gqd_normal[2] < 0:
        gqd_normal = -gqd_normal

    # Deterministic C1 outward vector projected into the basal plane.
    c1 = gqd_xyz[0]

    outward = c1 - gqd_centroid
    outward -= np.dot(outward, gqd_normal) * gqd_normal
    outward /= np.linalg.norm(outward)

    # Accepted Erlotinib quinazoline plane.
    core_xyz = np.array([drug_xyz[i - 1] for i in CORE_IDX])
    core_centroid, drug_normal = fit_plane(core_xyz)

    if drug_normal[2] < 0:
        drug_normal = -drug_normal

    # ------------------------------------------------------------------
    # FLAT: Face A, quinazoline plane parallel to GQD.
    # The 3.90 A separation and 209 deg in-plane azimuth are the
    # smallest tested deterministic starting geometry that satisfies
    # both the heavy-atom and 2.0 A basal all-atom clash gates.
    # ------------------------------------------------------------------
    R_flat_face = rotation_from_to(drug_normal, gqd_normal)
    R_flat_spin = axis_rotation(gqd_normal, FLAT_AZIMUTH_DEG)

    flat_target_centroid = (
        gqd_centroid + FLAT_CORE_SEPARATION * gqd_normal
    )

    flat_xyz = (
        (drug_xyz - core_centroid)
        @ R_flat_face.T
        @ R_flat_spin.T
        + flat_target_centroid
    )

    flat_heavy = heavy_minimum(
        gqd,
        drug_elements,
        flat_xyz,
    )

    flat_core = np.array([flat_xyz[i - 1] for i in CORE_IDX])
    flat_core_centroid, flat_normal = fit_plane(flat_core)

    flat_sep = np.dot(
        flat_core_centroid - gqd_centroid,
        gqd_normal,
    )

    flat_angle = np.degrees(
        np.arccos(
            np.clip(
                abs(np.dot(flat_normal, gqd_normal)),
                -1.0,
                1.0,
            )
        )
    )

    # ------------------------------------------------------------------
    # SLIPPED: Face A, 3.40 A core-plane separation, shifted
    # 2.50 A AWAY from the C1/COOH edge.  A separate 324 deg azimuth
    # maximizes nonbonded clearance while preserving the slipped basin.
    # ------------------------------------------------------------------
    R_slipped_face = rotation_from_to(drug_normal, gqd_normal)
    R_slipped_spin = axis_rotation(
        gqd_normal,
        SLIPPED_AZIMUTH_DEG,
    )

    slipped_target_centroid = (
        gqd_centroid
        + SLIPPED_CORE_SEPARATION * gqd_normal
        - SLIP_DISTANCE * outward
    )

    slipped_xyz = (
        (drug_xyz - core_centroid)
        @ R_slipped_face.T
        @ R_slipped_spin.T
        + slipped_target_centroid
    )

    slipped_heavy = heavy_minimum(
        gqd,
        drug_elements,
        slipped_xyz,
    )

    slipped_core = np.array(
        [slipped_xyz[i - 1] for i in CORE_IDX]
    )
    slipped_core_centroid, slipped_normal = fit_plane(slipped_core)

    slipped_sep = np.dot(
        slipped_core_centroid - gqd_centroid,
        gqd_normal,
    )

    slipped_angle = np.degrees(
        np.arccos(
            np.clip(
                abs(np.dot(slipped_normal, gqd_normal)),
                -1.0,
                1.0,
            )
        )
    )

    # ------------------------------------------------------------------
    # EDGE: corrected COOH O74-H75 donor directed toward Erlotinib N6.
    # Target H75...N6 = 1.90 A.
    # Quinazoline plane approximately 80 degrees to GQD basal plane.
    # Deterministic twist = 260 degrees.
    # ------------------------------------------------------------------
    n6 = drug_xyz[5]
    c9 = drug_xyz[8]
    c18 = drug_xyz[17]

    u1 = (c9 - n6) / np.linalg.norm(c9 - n6)
    u2 = (c18 - n6) / np.linalg.norm(c18 - n6)

    lone_bisector = -(u1 + u2)
    lone_bisector /= np.linalg.norm(lone_bisector)

    o74 = gqd_xyz[73]
    h75 = gqd_xyz[74]

    donor = h75 - o74
    donor /= np.linalg.norm(donor)

    target_n6 = h75 + EDGE_HN_DISTANCE * donor
    target_lone = -donor

    R_align = rotation_from_to(
        lone_bisector,
        target_lone,
    )

    rel = drug_xyz - n6
    rel_aligned = rel @ R_align.T

    R_twist = axis_rotation(
        target_lone,
        EDGE_TWIST_DEG,
    )

    edge_xyz = rel_aligned @ R_twist.T + target_n6

    edge_heavy = heavy_minimum(
        gqd,
        drug_elements,
        edge_xyz,
    )

    if edge_heavy[0] < HEAVY_CLASH_GATE:
        raise RuntimeError(
            "Edge pose violates heavy-atom clash gate: "
            f"{edge_heavy[0]:.6f} A"
        )

    edge_core = np.array([edge_xyz[i - 1] for i in CORE_IDX])
    _, edge_normal = fit_plane(edge_core)

    edge_angle = np.degrees(
        np.arccos(
            np.clip(
                abs(np.dot(edge_normal, gqd_normal)),
                -1.0,
                1.0,
            )
        )
    )

    hn_distance = np.linalg.norm(
        h75 - edge_xyz[5]
    )
    on_distance = np.linalg.norm(
        o74 - edge_xyz[5]
    )

    # ------------------------------------------------------------------
    # Rigid-body preservation validation.
    # ------------------------------------------------------------------
    flat_rigid_error = max_pairwise_distance_error(
        drug_xyz,
        flat_xyz,
    )
    slipped_rigid_error = max_pairwise_distance_error(
        drug_xyz,
        slipped_xyz,
    )
    edge_rigid_error = max_pairwise_distance_error(
        drug_xyz,
        edge_xyz,
    )

    for label, error in [
        ("flat", flat_rigid_error),
        ("slipped", slipped_rigid_error),
        ("edge", edge_rigid_error),
    ]:
        if error > 1.0e-8:
            raise RuntimeError(
                f"{label} pose failed rigid-body invariant: "
                f"{error:.3e} A"
            )

    flat_all = all_atom_minimum(
        gqd,
        drug_elements,
        flat_xyz,
    )
    slipped_all = all_atom_minimum(
        gqd,
        drug_elements,
        slipped_xyz,
    )
    edge_all = all_atom_minimum(
        gqd,
        drug_elements,
        edge_xyz,
    )

    if flat_heavy[0] < HEAVY_CLASH_GATE:
        raise RuntimeError(
            "Flat pose violates heavy-atom clash gate: "
            f"{flat_heavy[0]:.6f} A"
        )

    if slipped_heavy[0] < HEAVY_CLASH_GATE:
        raise RuntimeError(
            "Slipped pose violates heavy-atom clash gate: "
            f"{slipped_heavy[0]:.6f} A"
        )

    if flat_all[0] < BASAL_ALL_ATOM_GATE:
        raise RuntimeError(
            "Flat pose violates basal all-atom clash gate: "
            f"{flat_all[0]:.6f} A"
        )

    if slipped_all[0] < BASAL_ALL_ATOM_GATE:
        raise RuntimeError(
            "Slipped pose violates basal all-atom clash gate: "
            f"{slipped_all[0]:.6f} A"
        )

    # ------------------------------------------------------------------
    # Write corrected-lineage XYZ files.
    # ------------------------------------------------------------------
    flat_path = OUT_DIR / (
        "cooh_gqd_c1_erlotinib_flat_start_v01.xyz"
    )
    slipped_path = OUT_DIR / (
        "cooh_gqd_c1_erlotinib_slipped_start_v01.xyz"
    )
    edge_path = OUT_DIR / (
        "cooh_gqd_c1_erlotinib_edge_start_v01.xyz"
    )

    common = (
        f"corrected lineage; GQD={GQD_PATH}; "
        f"GQD_sha256={gqd_sha}; "
        f"Erlotinib={DRUG_PATH}; "
        f"Erlotinib_sha256={drug_sha}; "
        "GQD_atoms=1-75; Erlotinib_atoms=76-127"
    )

    write_complex(
        flat_path,
        (
            common
            + f"; pose=flat; face=A; "
            f"core_plane_sep={FLAT_CORE_SEPARATION:.2f}A; "
            f"azimuth={FLAT_AZIMUTH_DEG:.2f}deg"
        ),
        gqd_raw,
        drug_elements,
        flat_xyz,
    )

    write_complex(
        slipped_path,
        (
            common
            + f"; pose=slipped; face=A; "
            f"core_plane_sep={SLIPPED_CORE_SEPARATION:.2f}A; "
            f"azimuth={SLIPPED_AZIMUTH_DEG:.2f}deg; "
            f"slip={SLIP_DISTANCE:.2f}A_away_from_C1"
        ),
        gqd_raw,
        drug_elements,
        slipped_xyz,
    )

    write_complex(
        edge_path,
        (
            common
            + f"; pose=edge; target=O74-H75...N6; "
            f"H75_N6={EDGE_HN_DISTANCE:.2f}A; "
            f"twist={EDGE_TWIST_DEG:.2f}deg"
        ),
        gqd_raw,
        drug_elements,
        edge_xyz,
    )

    print("SOURCE_VALIDATION=PASS")
    print(f"GQD_SHA256={gqd_sha}")
    print(f"ERLOTINIB_SHA256={drug_sha}")
    print(f"GQD_ATOMS={gqd_natoms}")
    print(f"ERLOTINIB_ATOMS={drug_natoms}")
    print(f"COMPLEX_ATOMS={COMPLEX_ATOMS}")
    print("COMPLEX_FORMULA=C77H41N3O6")
    print()

    print("FLAT")
    print(f"  core_plane_sep={flat_sep:.6f} A")
    print(f"  plane_angle={flat_angle:.6f} deg")
    print(f"  azimuth={FLAT_AZIMUTH_DEG:.6f} deg")
    print(f"  heavy_min={flat_heavy[0]:.6f} A")
    print(
        "  closest_heavy="
        f"GQD {flat_heavy[2]}{flat_heavy[1]} / "
        f"Erlotinib {flat_heavy[4]}{flat_heavy[3]}"
    )
    print(f"  all_atom_min={flat_all[0]:.6f} A")
    print(f"  rigid_error={flat_rigid_error:.3e} A")
    print(f"  output={flat_path}")
    print()

    print("SLIPPED")
    print(f"  core_plane_sep={slipped_sep:.6f} A")
    print(f"  plane_angle={slipped_angle:.6f} deg")
    print(f"  azimuth={SLIPPED_AZIMUTH_DEG:.6f} deg")
    print(f"  slip_distance={SLIP_DISTANCE:.6f} A")
    print("  slip_direction=away_from_C1")
    print(f"  heavy_min={slipped_heavy[0]:.6f} A")
    print(
        "  closest_heavy="
        f"GQD {slipped_heavy[2]}{slipped_heavy[1]} / "
        f"Erlotinib {slipped_heavy[4]}{slipped_heavy[3]}"
    )
    print(f"  all_atom_min={slipped_all[0]:.6f} A")
    print(f"  rigid_error={slipped_rigid_error:.3e} A")
    print(f"  output={slipped_path}")
    print()

    print("EDGE")
    print(f"  plane_angle={edge_angle:.6f} deg")
    print(f"  twist={EDGE_TWIST_DEG:.6f} deg")
    print(f"  H75_N6={hn_distance:.6f} A")
    print(f"  O74_N6={on_distance:.6f} A")
    print(f"  heavy_min={edge_heavy[0]:.6f} A")
    print(
        "  closest_heavy="
        f"GQD {edge_heavy[2]}{edge_heavy[1]} / "
        f"Erlotinib {edge_heavy[4]}{edge_heavy[3]}"
    )
    print(f"  all_atom_min={edge_all[0]:.6f} A")
    print(f"  rigid_error={edge_rigid_error:.3e} A")
    print(f"  output={edge_path}")
    print()

    print("BUILD_COMPLEX_CORRECTED=PASS")


if __name__ == "__main__":
    main()
