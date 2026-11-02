#!/usr/bin/env python3
"""Canonical COOH-GQD geometry/topology audit.

Audits the repository's 75-atom monocarboxylated circumcoronene GQD fragment
(C1-C54 scaffold; 21 remaining GQD atoms) from either an XYZ file or a
Gaussian output parsed with cclib. The script independently reconstructs
connectivity from Cartesian distances, measures best-fit-plane deformation,
checks circumcoronene graph invariants, verifies COOH connectivity, and can
produce a reproducible side-profile figure and machine-readable JSON report.

This tool intentionally does not use Open Babel, RDKit, or NetworkX.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Dict, List, Sequence, Set, Tuple

import numpy as np


EXPECTED_FORMULA = Counter({"C": 55, "H": 18, "O": 2})
EXPECTED_SCAFFOLD = {
    "atoms": 54,
    "edges": 72,
    "degree2": 18,
    "degree3": 36,
    "cycle_rank": 19,
    "six_cycles": 19,
}

# Broad enough to flag distorted historical contacts while remaining below
# the nearest nonbonded C...C separation in an intact circumcoronene scaffold.
DEFAULT_CC_MIN = 1.15
DEFAULT_CC_MAX = 1.85

# Project screening thresholds for severe scaffold deformation. These are
# configurable. They are deliberately much looser than the accepted C1
# baseline (RMS ~0.009 A; span ~0.047 A) while rejecting the historical
# warped scaffold (RMS ~1.69 A; span ~6.11 A).
DEFAULT_MAX_PLANE_RMS = 0.25
DEFAULT_MAX_PLANE_SPAN = 0.75

COVALENT_RADII = {
    "H": 0.31,
    "C": 0.76,
    "N": 0.71,
    "O": 0.66,
    "F": 0.57,
    "P": 1.07,
    "S": 1.05,
    "Cl": 1.02,
}
DEFAULT_BOND_SCALE = 1.25

ATOMIC_SYMBOLS = {
    1: "H",
    6: "C",
    7: "N",
    8: "O",
    9: "F",
    15: "P",
    16: "S",
    17: "Cl",
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def formula_string(elements: Sequence[str]) -> str:
    counts = Counter(elements)
    order = []
    if "C" in counts:
        order.append("C")
    if "H" in counts:
        order.append("H")
    order.extend(sorted(el for el in counts if el not in {"C", "H"}))
    return "".join(
        el + (str(counts[el]) if counts[el] != 1 else "")
        for el in order
    )


def read_xyz(path: Path) -> Tuple[List[str], np.ndarray, Dict[str, object]]:
    lines = path.read_text().splitlines()
    if len(lines) < 2:
        raise RuntimeError("XYZ file is incomplete")
    try:
        declared = int(lines[0].strip())
    except ValueError as exc:
        raise RuntimeError("XYZ first line is not an atom count") from exc

    elements: List[str] = []
    coords: List[List[float]] = []
    for line_no, line in enumerate(lines[2:], start=3):
        if not line.strip():
            continue
        fields = line.split()
        if len(fields) != 4:
            raise RuntimeError(
                f"Malformed XYZ coordinate line {line_no}: {line}"
            )
        elements.append(fields[0])
        coords.append(
            [float(fields[1]), float(fields[2]), float(fields[3])]
        )

    if declared != len(coords):
        raise RuntimeError(
            f"XYZ declares {declared} atoms but {len(coords)} were parsed"
        )

    metadata = {
        "format": "xyz",
        "geometry_selection": "single",
        "comment": lines[1].strip(),
    }
    return elements, np.asarray(coords, dtype=float), metadata


def read_gaussian(
    path: Path,
    geometry: str,
) -> Tuple[List[str], np.ndarray, Dict[str, object]]:
    try:
        from cclib.io import ccread
    except Exception as exc:
        raise RuntimeError(
            "cclib is required to parse Gaussian output files"
        ) from exc

    data = ccread(str(path))
    if (
        data is None
        or not hasattr(data, "atomcoords")
        or not hasattr(data, "atomnos")
    ):
        raise RuntimeError(
            "cclib could not parse atomic coordinates from the Gaussian output"
        )

    all_coords = np.asarray(data.atomcoords, dtype=float)
    if all_coords.ndim != 3 or all_coords.shape[0] < 1:
        raise RuntimeError("Gaussian output contains no coordinate frames")

    if geometry == "first":
        idx = 0
    elif geometry == "last":
        idx = all_coords.shape[0] - 1
    else:
        try:
            idx = int(geometry)
        except ValueError as exc:
            raise RuntimeError(
                "--geometry must be first, last, or an integer frame index"
            ) from exc
        if idx < 0:
            idx = all_coords.shape[0] + idx
        if not 0 <= idx < all_coords.shape[0]:
            raise RuntimeError(
                f"Requested frame {geometry} outside 0..{all_coords.shape[0]-1}"
            )

    elements = []
    for z in data.atomnos:
        symbol = ATOMIC_SYMBOLS.get(int(z))
        if symbol is None:
            raise RuntimeError(
                f"Unsupported atomic number in Gaussian file: {z}"
            )
        elements.append(symbol)

    metadata = {
        "format": "gaussian",
        "geometry_selection": geometry,
        "geometry_frame_index": idx,
        "geometry_frame_count": int(all_coords.shape[0]),
    }
    return elements, all_coords[idx], metadata


def read_structure(
    path: Path,
    geometry: str,
) -> Tuple[List[str], np.ndarray, Dict[str, object]]:
    suffix = path.suffix.lower()
    if suffix == ".xyz":
        return read_xyz(path)
    if suffix in {".log", ".out"}:
        return read_gaussian(path, geometry)
    raise RuntimeError("Supported inputs are .xyz, .log, and .out")


def distance(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.linalg.norm(a - b))


def infer_bonds(
    elements: Sequence[str],
    coords: np.ndarray,
    scale: float,
) -> List[Tuple[int, int, float]]:
    bonds: List[Tuple[int, int, float]] = []
    for i in range(len(elements)):
        ri = COVALENT_RADII.get(elements[i])
        if ri is None:
            continue
        for j in range(i + 1, len(elements)):
            rj = COVALENT_RADII.get(elements[j])
            if rj is None:
                continue
            d = distance(coords[i], coords[j])
            cutoff = scale * (ri + rj)
            if 0.40 < d <= cutoff:
                bonds.append((i, j, d))
    return bonds


def build_scaffold_graph(
    scaffold_coords: np.ndarray,
    cc_min: float,
    cc_max: float,
) -> Tuple[Set[Tuple[int, int]], Dict[int, Set[int]]]:
    n = len(scaffold_coords)
    adj = {i: set() for i in range(n)}
    edges: Set[Tuple[int, int]] = set()
    for i in range(n):
        for j in range(i + 1, n):
            d = distance(scaffold_coords[i], scaffold_coords[j])
            if cc_min <= d <= cc_max:
                edges.add((i, j))
                adj[i].add(j)
                adj[j].add(i)
    return edges, adj


def is_connected(adj: Dict[int, Set[int]]) -> bool:
    if not adj:
        return False
    seen = {next(iter(adj))}
    stack = list(seen)
    while stack:
        i = stack.pop()
        for j in adj[i]:
            if j not in seen:
                seen.add(j)
                stack.append(j)
    return len(seen) == len(adj)


def canonical_cycle(cycle: Sequence[int]) -> Tuple[int, ...]:
    seq = list(cycle)
    forms = []
    for candidate in (seq, list(reversed(seq))):
        for k in range(len(candidate)):
            forms.append(tuple(candidate[k:] + candidate[:k]))
    return min(forms)


def count_six_cycles(adj: Dict[int, Set[int]]) -> int:
    cycles: Set[Tuple[int, ...]] = set()

    def walk(start: int, current: int, path: List[int]) -> None:
        if len(path) == 6:
            if start in adj[current]:
                cycles.add(canonical_cycle(path))
            return
        for nb in adj[current]:
            if nb in path:
                continue
            walk(start, nb, path + [nb])

    for start in sorted(adj):
        walk(start, start, [start])
    return len(cycles)


def best_fit_plane(coords: np.ndarray) -> Dict[str, object]:
    center = coords.mean(axis=0)
    centered = coords - center
    _, _, vh = np.linalg.svd(centered, full_matrices=False)
    axis1 = vh[0]
    axis2 = vh[1]
    normal = vh[2]
    signed = centered @ normal
    return {
        "center": center,
        "axis1": axis1,
        "axis2": axis2,
        "normal": normal,
        "signed_distances": signed,
        "rms": float(np.sqrt(np.mean(signed ** 2))),
        "span": float(np.max(signed) - np.min(signed)),
        "max_abs": float(np.max(np.abs(signed))),
        "min": float(np.min(signed)),
        "max": float(np.max(signed)),
    }


def degree_distribution(
    adj: Dict[int, Set[int]],
) -> Dict[int, int]:
    counts = Counter(len(adj[i]) for i in adj)
    return dict(sorted(counts.items()))


def identify_cooh(
    elements: Sequence[str],
    coords: np.ndarray,
    bonds: Sequence[Tuple[int, int, float]],
    scaffold_atoms: int,
) -> Dict[str, object]:
    adjacency: Dict[int, List[Tuple[int, float]]] = {
        i: [] for i in range(len(elements))
    }
    for i, j, d in bonds:
        adjacency[i].append((j, d))
        adjacency[j].append((i, d))

    candidates = []
    for c in range(scaffold_atoms, len(elements)):
        if elements[c] != "C":
            continue
        scaffold_neighbors = [
            (j, d)
            for j, d in adjacency[c]
            if j < scaffold_atoms and elements[j] == "C"
        ]
        oxygen_neighbors = [
            (j, d)
            for j, d in adjacency[c]
            if elements[j] == "O"
        ]
        if len(scaffold_neighbors) == 1 and len(oxygen_neighbors) == 2:
            hydroxyl = []
            for o, cod in oxygen_neighbors:
                h_neighbors = [
                    (h, d)
                    for h, d in adjacency[o]
                    if elements[h] == "H"
                ]
                if h_neighbors:
                    hydroxyl.append((o, cod, h_neighbors))
            candidates.append(
                {
                    "carboxyl_carbon": c,
                    "scaffold_neighbor": scaffold_neighbors[0],
                    "oxygen_neighbors": oxygen_neighbors,
                    "hydroxyl_oxygen_candidates": hydroxyl,
                }
            )

    gate = (
        len(candidates) == 1
        and len(candidates[0]["hydroxyl_oxygen_candidates"]) == 1
    )
    detail = candidates[0] if len(candidates) == 1 else None

    report: Dict[str, object] = {
        "gate": gate,
        "candidate_count": len(candidates),
        "candidate": None,
    }
    if detail is not None:
        c = detail["carboxyl_carbon"]
        scaffold_neighbor, cc_d = detail["scaffold_neighbor"]
        oxygen_neighbors = detail["oxygen_neighbors"]
        hydroxyl = detail["hydroxyl_oxygen_candidates"]
        report["candidate"] = {
            "carboxyl_carbon_atom": c + 1,
            "scaffold_attachment_atom": scaffold_neighbor + 1,
            "scaffold_C_COOH_A": cc_d,
            "oxygen_atoms": [o + 1 for o, _ in oxygen_neighbors],
            "C_O_distances_A": [d for _, d in oxygen_neighbors],
            "hydroxyl_oxygen_atom": (
                hydroxyl[0][0] + 1 if len(hydroxyl) == 1 else None
            ),
            "hydroxyl_hydrogen_atom": (
                hydroxyl[0][2][0][0] + 1
                if len(hydroxyl) == 1
                else None
            ),
            "O_H_A": (
                hydroxyl[0][2][0][1]
                if len(hydroxyl) == 1
                else None
            ),
        }
    return report


def make_figure(
    path: Path,
    coords: np.ndarray,
    scaffold_atoms: int,
    plane: Dict[str, object],
    title: str,
) -> None:
    try:
        import matplotlib.pyplot as plt
    except Exception as exc:
        raise RuntimeError(
            "matplotlib is required for --figure"
        ) from exc

    center = np.asarray(plane["center"])
    axis1 = np.asarray(plane["axis1"])
    normal = np.asarray(plane["normal"])
    centered = coords - center
    x = centered @ axis1
    y = centered @ normal

    fig, ax = plt.subplots(figsize=(8.2, 4.2))
    ax.scatter(
        x[:scaffold_atoms],
        y[:scaffold_atoms],
        s=25,
        label="C1-C54 scaffold",
    )
    if len(coords) > scaffold_atoms:
        ax.scatter(
            x[scaffold_atoms:],
            y[scaffold_atoms:],
            s=32,
            marker="x",
            label="Remaining GQD atoms",
        )
    ax.axhline(0.0, linewidth=0.8)
    ax.set_xlabel("Principal in-plane coordinate (A)")
    ax.set_ylabel("Best-fit-plane normal coordinate (A)")
    ax.set_title(title)
    ax.grid(True, alpha=0.20)
    ax.legend(loc="best")
    ax.text(
        0.02,
        0.97,
        (
            f"C1-C54 RMS={plane['rms']:.6f} A; "
            f"span={plane['span']:.6f} A"
        ),
        transform=ax.transAxes,
        va="top",
    )
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=220, bbox_inches="tight")
    plt.close(fig)


def write_bonds_tsv(
    path: Path,
    elements: Sequence[str],
    bonds: Sequence[Tuple[int, int, float]],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as handle:
        handle.write(
            "atom_i\telement_i\tatom_j\telement_j\tdistance_A\n"
        )
        for i, j, d in bonds:
            handle.write(
                f"{i+1}\t{elements[i]}\t{j+1}\t"
                f"{elements[j]}\t{d:.8f}\n"
            )


def audit(
    args: argparse.Namespace,
) -> Tuple[Dict[str, object], bool]:
    path = Path(args.input)
    if not path.exists():
        raise RuntimeError(f"Input does not exist: {path}")

    elements, coords, metadata = read_structure(
        path,
        args.geometry,
    )
    if len(elements) < args.gqd_atoms:
        raise RuntimeError(
            f"Input has {len(elements)} atoms; at least "
            f"{args.gqd_atoms} are required"
        )

    gqd_elements = list(elements[: args.gqd_atoms])
    gqd_coords = np.asarray(
        coords[: args.gqd_atoms],
        dtype=float,
    )
    scaffold_elements = gqd_elements[: args.scaffold_atoms]
    scaffold_coords = gqd_coords[: args.scaffold_atoms]

    full_bonds = infer_bonds(
        gqd_elements,
        gqd_coords,
        args.bond_scale,
    )
    scaffold_edges, scaffold_adj = build_scaffold_graph(
        scaffold_coords,
        args.cc_min,
        args.cc_max,
    )
    connected = is_connected(scaffold_adj)
    deg = degree_distribution(scaffold_adj)
    cycle_rank = (
        len(scaffold_edges) - args.scaffold_atoms + 1
        if connected
        else None
    )
    six_cycles = count_six_cycles(scaffold_adj)
    plane = best_fit_plane(scaffold_coords)
    cooh = identify_cooh(
        gqd_elements,
        gqd_coords,
        full_bonds,
        args.scaffold_atoms,
    )

    formula = Counter(gqd_elements)
    formula_gate = formula == EXPECTED_FORMULA
    scaffold_identity_gate = (
        scaffold_elements == ["C"] * args.scaffold_atoms
    )
    topology_gate = (
        len(scaffold_edges) == EXPECTED_SCAFFOLD["edges"]
        and deg.get(2, 0) == EXPECTED_SCAFFOLD["degree2"]
        and deg.get(3, 0) == EXPECTED_SCAFFOLD["degree3"]
        and set(deg).issubset({2, 3})
        and connected
        and cycle_rank == EXPECTED_SCAFFOLD["cycle_rank"]
        and six_cycles == EXPECTED_SCAFFOLD["six_cycles"]
    )
    geometry_gate = (
        plane["rms"] <= args.max_plane_rms
        and plane["span"] <= args.max_plane_span
    )
    molecular_bond_gate = len(full_bonds) == 93

    failures = []
    if not formula_gate:
        failures.append("formula")
    if not scaffold_identity_gate:
        failures.append("scaffold_atom_identity")
    if not topology_gate:
        failures.append("scaffold_topology")
    if not geometry_gate:
        failures.append("scaffold_planarity")
    if not cooh["gate"]:
        failures.append("cooh_connectivity")
    if not molecular_bond_gate:
        failures.append("molecular_bond_count")

    overall = not failures

    report: Dict[str, object] = {
        "tool": "scripts/audit_gqd_geometry_topology.py",
        "input": str(path),
        "input_sha256": sha256_file(path),
        "source": metadata,
        "full_input_atom_count": len(elements),
        "full_input_formula": formula_string(elements),
        "audited_gqd_atom_count": len(gqd_elements),
        "audited_gqd_formula": formula_string(gqd_elements),
        "formula_gate": formula_gate,
        "inferred_gqd_bonds": len(full_bonds),
        "molecular_bond_count_gate": molecular_bond_gate,
        "scaffold": {
            "atom_count": args.scaffold_atoms,
            "atom_identity_gate": scaffold_identity_gate,
            "C_C_edges": len(scaffold_edges),
            "degree_distribution": {
                str(k): v for k, v in deg.items()
            },
            "connected": connected,
            "cycle_rank": cycle_rank,
            "six_membered_cycles": six_cycles,
            "cc_distance_window_A": [
                args.cc_min,
                args.cc_max,
            ],
            "topology_gate": topology_gate,
            "plane_rms_A": plane["rms"],
            "plane_span_A": plane["span"],
            "plane_max_abs_A": plane["max_abs"],
            "plane_min_A": plane["min"],
            "plane_max_A": plane["max"],
            "max_plane_rms_A": args.max_plane_rms,
            "max_plane_span_A": args.max_plane_span,
            "geometry_gate": geometry_gate,
        },
        "cooh": cooh,
        "overall_gate": overall,
        "failures": failures,
    }

    if args.figure:
        title = (
            args.figure_title
            or path.stem.replace("_", " ")
        )
        make_figure(
            Path(args.figure),
            gqd_coords,
            args.scaffold_atoms,
            plane,
            title,
        )
        report["figure"] = str(args.figure)

    if args.bonds_tsv:
        write_bonds_tsv(
            Path(args.bonds_tsv),
            gqd_elements,
            full_bonds,
        )
        report["bonds_tsv"] = str(args.bonds_tsv)

    if args.json:
        out = Path(args.json)
        out.parent.mkdir(
            parents=True,
            exist_ok=True,
        )
        out.write_text(
            json.dumps(
                report,
                indent=2,
                sort_keys=True,
            )
            + "\n"
        )

    return report, overall


def print_report(
    report: Dict[str, object],
) -> None:
    sc = report["scaffold"]
    cooh = report["cooh"]
    print("===== GQD GEOMETRY / TOPOLOGY AUDIT =====")
    print(f"tool = {report['tool']}")
    print(f"input = {report['input']}")
    print(f"input_sha256 = {report['input_sha256']}")
    print(f"source_format = {report['source']['format']}")
    print(
        "geometry_selection = "
        f"{report['source']['geometry_selection']}"
    )
    print()
    print(
        "full input atoms = "
        f"{report['full_input_atom_count']}"
    )
    print(
        "full input formula = "
        f"{report['full_input_formula']}"
    )
    print(
        "audited GQD atoms = "
        f"{report['audited_gqd_atom_count']}"
    )
    print(
        "audited GQD formula = "
        f"{report['audited_gqd_formula']}"
    )
    print(
        "formula gate = "
        f"{'PASS' if report['formula_gate'] else 'FAIL'}"
    )
    print(
        "inferred GQD bonds = "
        f"{report['inferred_gqd_bonds']}"
    )
    print(
        "93-bond molecular gate = "
        f"{'PASS' if report['molecular_bond_count_gate'] else 'FAIL'}"
    )
    print()
    print("scaffold C1-C54:")
    print(f"  C-C edges = {sc['C_C_edges']}")
    print(
        "  degree distribution = "
        f"{sc['degree_distribution']}"
    )
    print(f"  connected = {sc['connected']}")
    print(f"  cycle rank = {sc['cycle_rank']}")
    print(
        "  six-membered cycles = "
        f"{sc['six_membered_cycles']}"
    )
    print(
        "  topology gate = "
        f"{'PASS' if sc['topology_gate'] else 'FAIL'}"
    )
    print(
        f"  plane RMS = {sc['plane_rms_A']:.6f} A"
    )
    print(
        f"  plane span = {sc['plane_span_A']:.6f} A"
    )
    print(
        "  max |plane deviation| = "
        f"{sc['plane_max_abs_A']:.6f} A"
    )
    print(
        "  geometry gate = "
        f"{'PASS' if sc['geometry_gate'] else 'FAIL'}"
    )
    print()
    print(
        "COOH connectivity gate = "
        f"{'PASS' if cooh['gate'] else 'FAIL'}"
    )
    if cooh.get("candidate"):
        c = cooh["candidate"]
        print(
            "  carboxyl carbon = atom "
            f"{c['carboxyl_carbon_atom']}"
        )
        print(
            "  scaffold attachment = atom "
            f"{c['scaffold_attachment_atom']} at "
            f"{c['scaffold_C_COOH_A']:.6f} A"
        )
        print(f"  oxygen atoms = {c['oxygen_atoms']}")
        if c["hydroxyl_oxygen_atom"] is not None:
            print(
                "  hydroxyl O-H = atoms "
                f"{c['hydroxyl_oxygen_atom']}-"
                f"{c['hydroxyl_hydrogen_atom']} at "
                f"{c['O_H_A']:.6f} A"
            )
    print()
    if report["overall_gate"]:
        print("GQD MODEL AUDIT = PASS")
    else:
        print("GQD MODEL AUDIT = FAIL")
        print(
            "failed domains = "
            + ", ".join(report["failures"])
        )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Independently audit a monocarboxylated "
            "circumcoronene GQD from XYZ or Gaussian output. "
            "The first 75 atoms are the GQD fragment and "
            "C1-C54 the graphene scaffold by default."
        )
    )
    parser.add_argument(
        "input",
        help="XYZ or Gaussian .log/.out file",
    )
    parser.add_argument(
        "--geometry",
        default="last",
        help=(
            "For Gaussian output: first, last, or integer "
            "cclib coordinate-frame index (default: last)"
        ),
    )
    parser.add_argument(
        "--gqd-atoms",
        type=int,
        default=75,
        help="Number of leading atoms forming the GQD fragment",
    )
    parser.add_argument(
        "--scaffold-atoms",
        type=int,
        default=54,
        help="Number of leading GQD atoms forming C1-C54 scaffold",
    )
    parser.add_argument(
        "--cc-min",
        type=float,
        default=DEFAULT_CC_MIN,
        help="Minimum inferred scaffold C-C distance (A)",
    )
    parser.add_argument(
        "--cc-max",
        type=float,
        default=DEFAULT_CC_MAX,
        help="Maximum inferred scaffold C-C distance (A)",
    )
    parser.add_argument(
        "--bond-scale",
        type=float,
        default=DEFAULT_BOND_SCALE,
        help="Covalent-radius scale for whole-GQD bond inference",
    )
    parser.add_argument(
        "--max-plane-rms",
        type=float,
        default=DEFAULT_MAX_PLANE_RMS,
        help="Maximum scaffold best-fit-plane RMS (A)",
    )
    parser.add_argument(
        "--max-plane-span",
        type=float,
        default=DEFAULT_MAX_PLANE_SPAN,
        help="Maximum scaffold best-fit-plane span (A)",
    )
    parser.add_argument(
        "--json",
        help="Write machine-readable JSON report",
    )
    parser.add_argument(
        "--bonds-tsv",
        help="Write inferred GQD bond list as TSV",
    )
    parser.add_argument(
        "--figure",
        help="Write reproducible side-profile figure",
    )
    parser.add_argument(
        "--figure-title",
        help="Optional figure title",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        report, passed = audit(args)
        print_report(report)
        return 0 if passed else 2
    except Exception as exc:
        print(f"AUDIT ERROR: {exc}", file=sys.stderr)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
