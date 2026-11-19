#!/usr/bin/env python3
"""Validate and extract the targeted H75...N81 QTAIM BCP from Critic2 output."""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path

NUM = r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[EeDd][+-]?\d+)?"


def as_float(token: str) -> float:
    return float(token.strip().rstrip(",;").replace("D", "E").replace("d", "e"))


def endpoint_atom_id(label: str) -> int | None:
    """Extract atom id from labels such as H75, H_75, H(75), n(75)."""
    s = label.strip()
    m = re.search(r"\((\d+)\)$", s)
    if m:
        return int(m.group(1))
    m = re.search(r"(\d+)$", s)
    if m:
        return int(m.group(1))
    return None


def normalize_endpoint(label: str) -> str:
    """Normalize endpoint labels while preserving atom identity when available."""
    s = label.strip()
    aid = endpoint_atom_id(s)
    if aid is None:
        return s.upper()

    # Prefer an explicit elemental prefix, if present.
    m = re.match(r"\s*([A-Za-z]+)", s)
    if m and m.group(1).lower() != "n":
        return f"{m.group(1).upper()}{aid}"
    return f"ATOM{aid}"


def extract_cp_properties(text: str, cp: int):
    block_re = re.compile(
        rf"\+ Critical point no\.\s*{cp}\s*\n(.*?)(?=\n\+ Critical point no\.|\nEnd AUTO|\Z)",
        re.S,
    )
    bm = block_re.search(text)
    if not bm:
        return None, None, None, None

    block = bm.group(1)

    def grab(pattern):
        m = re.search(pattern, block)
        return None if not m else as_float(m.group(1))

    rho = grab(rf"Field value \(f\):\s*({NUM})")
    lap = grab(rf"Laplacian \(del2 f\):\s*({NUM})")
    ell = grab(rf"Ellipticity .*?:\s*({NUM})")

    typem = re.search(r"Type\s*:\s*\((\d+)\s*,\s*([+-]?\d+)\)", block)
    cptype = None if not typem else f"({typem.group(1)},{typem.group(2)})"

    return rho, lap, ell, cptype


def parse_bond_row(line: str):
    """Parse one Critic2 bond-analysis row without assuming rigid whitespace."""
    s = line.strip()
    if not s or s.startswith(("#", "*", "+", "%")):
        return None

    parts = s.split()
    if len(parts) < 7:
        return None

    try:
        cp = int(parts[0])
    except ValueError:
        return None

    end1_raw = parts[1]
    end2_raw = parts[2]

    nums = []
    for token in parts[3:]:
        try:
            nums.append(as_float(token))
        except ValueError:
            continue
        if len(nums) == 4:
            break

    if len(nums) < 4:
        return None

    return {
        "cp_id": cp,
        "end1_raw": end1_raw,
        "end2_raw": end2_raw,
        "end1": normalize_endpoint(end1_raw),
        "end2": normalize_endpoint(end2_raw),
        "end1_atom_id": endpoint_atom_id(end1_raw),
        "end2_atom_id": endpoint_atom_id(end2_raw),
        "r1_ang": nums[0],
        "r2_ang": nums[1],
        "r1_r2_ratio": nums[2],
        "bond_path_angle_deg": nums[3],
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("cro", type=Path)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--connectivity-out", type=Path)
    args = ap.parse_args()

    text = args.cro.read_text(errors="replace")

    if "CRITIC2 ended successfully" not in text:
        raise SystemExit("ERROR: Critic2 success marker absent")

    bonds = []
    candidate_unparsed = []
    in_bonds = False
    saw_bond_header = False

    for line in text.splitlines():
        if "* Analysis of system bonds" in line:
            in_bonds = True
            saw_bond_header = True
            continue

        if in_bonds and (
            line.lstrip().startswith("* Analysis of system rings")
            or line.lstrip().startswith("* Attractor connectivity matrix")
            or line.lstrip().startswith("* Complete CP list")
            or line.lstrip().startswith("* Additional properties")
        ):
            break

        if not in_bonds:
            continue

        row = parse_bond_row(line)
        if row is not None:
            bonds.append(row)
            continue

        stripped = line.strip()
        if stripped and stripped[0].isdigit():
            candidate_unparsed.append(stripped)

    if not saw_bond_header:
        raise SystemExit(
            "ERROR: Critic2 'Analysis of system bonds' section not found; "
            "cannot validate target-BCP absence."
        )

    if not bonds:
        sample = "\n".join(candidate_unparsed[:8]) or "<no data-like rows captured>"
        raise SystemExit(
            "ERROR: bond-analysis section found but zero bond rows parsed.\n"
            "First data-like lines from that section:\n"
            f"{sample}"
        )

    related = [
        b for b in bonds
        if b["end1_atom_id"] in {75, 81}
        or b["end2_atom_id"] in {75, 81}
    ]

    target = next(
        (
            b for b in bonds
            if {b["end1_atom_id"], b["end2_atom_id"]} == {75, 81}
        ),
        None,
    )

    if args.connectivity_out:
        args.connectivity_out.parent.mkdir(parents=True, exist_ok=True)
        fields = [
            "cp_id",
            "end1_raw",
            "end2_raw",
            "end1",
            "end2",
            "end1_atom_id",
            "end2_atom_id",
            "r1_ang",
            "r2_ang",
            "r1_r2_ratio",
            "bond_path_angle_deg",
        ]
        with args.connectivity_out.open("w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fields, delimiter="\t")
            w.writeheader()
            for b in related:
                w.writerow(b)

    args.out.parent.mkdir(parents=True, exist_ok=True)

    fields = [
        "target",
        "bond_section_found",
        "bond_rows_parsed",
        "h75_or_n81_related_rows",
        "bcp_found",
        "cp_id",
        "end1",
        "end2",
        "end1_atom_id",
        "end2_atom_id",
        "r1_ang",
        "r2_ang",
        "r1_r2_ratio",
        "bond_path_angle_deg",
        "cp_type",
        "rho_bcp",
        "laplacian_bcp",
        "ellipticity",
        "qc_status",
    ]

    row = {
        "target": "H75...N81",
        "bond_section_found": "YES",
        "bond_rows_parsed": len(bonds),
        "h75_or_n81_related_rows": len(related),
        "bcp_found": "NO",
        "cp_id": "",
        "end1": "",
        "end2": "",
        "end1_atom_id": "",
        "end2_atom_id": "",
        "r1_ang": "",
        "r2_ang": "",
        "r1_r2_ratio": "",
        "bond_path_angle_deg": "",
        "cp_type": "",
        "rho_bcp": "",
        "laplacian_bcp": "",
        "ellipticity": "",
        "qc_status": "PASS_NO_TARGET_BCP",
    }

    if target is not None:
        cp = target["cp_id"]
        rho, lap, ell, cptype = extract_cp_properties(text, cp)

        if cptype is not None and cptype != "(3,-1)":
            raise SystemExit(
                f"ERROR: target connectivity row points to CP {cp} "
                f"with unexpected type {cptype}"
            )

        row.update({
            "bcp_found": "YES",
            "cp_id": cp,
            "end1": target["end1"],
            "end2": target["end2"],
            "end1_atom_id": target["end1_atom_id"],
            "end2_atom_id": target["end2_atom_id"],
            "r1_ang": f"{target['r1_ang']:.8f}",
            "r2_ang": f"{target['r2_ang']:.8f}",
            "r1_r2_ratio": f"{target['r1_r2_ratio']:.8f}",
            "bond_path_angle_deg": f"{target['bond_path_angle_deg']:.8f}",
            "cp_type": "" if cptype is None else cptype,
            "rho_bcp": "" if rho is None else f"{rho:.10e}",
            "laplacian_bcp": "" if lap is None else f"{lap:.10e}",
            "ellipticity": "" if ell is None else f"{ell:.10e}",
            "qc_status": "PASS_TARGET_BCP_FOUND",
        })

    with args.out.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, delimiter="\t")
        w.writeheader()
        w.writerow(row)

    print("PASS: targeted QTAIM connectivity validation complete.")
    print(f"Bond rows parsed: {len(bonds)}")
    print(f"H75/N81-related bond rows: {len(related)}")

    if related:
        print("Related BCP connectivity:")
        for b in related:
            print(
                f"  cp={b['cp_id']} "
                f"{b['end1_raw']}--{b['end2_raw']} "
                f"(ids {b['end1_atom_id']}--{b['end2_atom_id']}) "
                f"r1={b['r1_ang']:.6f} r2={b['r2_ang']:.6f} "
                f"angle={b['bond_path_angle_deg']:.4f}"
            )
    else:
        print("No BCP connectivity rows involve atom IDs 75 or 81.")

    if target:
        print(
            f"TARGET_BCP=YES cp={target['cp_id']} "
            f"atom_ids={target['end1_atom_id']}--{target['end2_atom_id']}"
        )
        print(
            f"rho={row['rho_bcp']} "
            f"laplacian={row['laplacian_bcp']} "
            f"ellipticity={row['ellipticity']}"
        )
    else:
        print("TARGET_BCP=NO")
        print(
            "A NO result is accepted only because the Critic2 bond-connectivity "
            "table was successfully parsed."
        )


if __name__ == "__main__":
    main()
