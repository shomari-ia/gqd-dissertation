#!/usr/bin/env python3
"""Validate and extract the targeted H75...N81 QTAIM BCP from Critic2 output."""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path

NUM = r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[Ee][+-]?\d+)?"


def normalize_endpoint(label: str) -> str:
    """Normalize labels such as H75, H_75, H(75) -> H75."""
    m = re.search(r"([A-Za-z]+)\D*(\d+)$", label.strip())
    if not m:
        return label.strip().upper()
    return f"{m.group(1).upper()}{int(m.group(2))}"


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
        return None if not m else float(m.group(1))

    rho = grab(rf"Field value \(f\):\s*({NUM})")
    lap = grab(rf"Laplacian \(del2 f\):\s*({NUM})")
    ell = grab(rf"Ellipticity .*?:\s*({NUM})")

    typem = re.search(r"Type\s*:\s*\((\d+)\s*,\s*([+-]?\d+)\)", block)
    cptype = None if not typem else f"({typem.group(1)},{typem.group(2)})"

    return rho, lap, ell, cptype


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("cro", type=Path)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--connectivity-out", type=Path)
    args = ap.parse_args()

    text = args.cro.read_text(errors="replace")

    if "CRITIC2 ended successfully" not in text:
        raise SystemExit("ERROR: Critic2 success marker absent")

    # Molecular AUTO bond-analysis rows:
    # ncp end1 end2 r1(ang) r2(ang) r1/r2 angle(deg)
    bond_row = re.compile(
        rf"^\s*(\d+)\s+(\S+)\s+(\S+)\s+"
        rf"({NUM})\s+({NUM})\s+({NUM})\s+({NUM})\s*$"
    )

    bonds = []
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
        ):
            break

        if not in_bonds:
            continue

        m = bond_row.match(line)
        if not m:
            continue

        raw1, raw2 = m.group(2), m.group(3)
        bonds.append({
            "cp_id": int(m.group(1)),
            "end1_raw": raw1,
            "end2_raw": raw2,
            "end1": normalize_endpoint(raw1),
            "end2": normalize_endpoint(raw2),
            "r1_ang": float(m.group(4)),
            "r2_ang": float(m.group(5)),
            "r1_r2_ratio": float(m.group(6)),
            "bond_path_angle_deg": float(m.group(7)),
        })

    if not saw_bond_header:
        raise SystemExit(
            "ERROR: Critic2 'Analysis of system bonds' section not found; "
            "cannot validate target-BPC absence."
        )

    if not bonds:
        raise SystemExit(
            "ERROR: bond-analysis section found but zero bond rows parsed; "
            "parser/table format must be reconciled before interpretation."
        )

    related = [
        b for b in bonds
        if "H75" in {b["end1"], b["end2"]}
        or "N81" in {b["end1"], b["end2"]}
    ]

    target = next(
        (b for b in bonds if {b["end1"], b["end2"]} == {"H75", "N81"}),
        None,
    )

    if args.connectivity_out:
        args.connectivity_out.parent.mkdir(parents=True, exist_ok=True)
        fields = [
            "cp_id", "end1_raw", "end2_raw", "end1", "end2",
            "r1_ang", "r2_ang", "r1_r2_ratio", "bond_path_angle_deg",
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
                f"(normalized {b['end1']}--{b['end2']}) "
                f"r1={b['r1_ang']:.6f} r2={b['r2_ang']:.6f} "
                f"angle={b['bond_path_angle_deg']:.4f}"
            )
    else:
        print("No BCP connectivity rows involve H75 or N81.")

    if target:
        print(
            f"TARGET_BCP=YES cp={target['cp_id']} "
            f"{target['end1']}--{target['end2']}"
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
