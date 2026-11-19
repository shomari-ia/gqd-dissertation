#!/usr/bin/env python3
"""Extract the targeted H75...N81 QTAIM bond critical point from Critic2 output."""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("cro", type=Path)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()

    text = args.cro.read_text(errors="replace")

    if "CRITIC2 ended successfully" not in text:
        raise SystemExit("ERROR: Critic2 success marker absent")

    # Critic2 bond-analysis rows:
    # ncp end1 end2 r1 r2 r1/r2 angle
    bond_row = re.compile(
        r"^\s*(\d+)\s+(\S+)\s+(\S+)\s+"
        r"([+-]?[0-9.Ee]+)\s+([+-]?[0-9.Ee]+)\s+"
        r"([+-]?[0-9.Ee]+)\s+([+-]?[0-9.Ee]+)\s*$"
    )

    target = None
    in_bonds = False

    for line in text.splitlines():
        if "* Analysis of system bonds" in line:
            in_bonds = True
            continue
        if in_bonds and line.lstrip().startswith("* Analysis of system rings"):
            break
        if not in_bonds:
            continue

        m = bond_row.match(line)
        if not m:
            continue

        cp = int(m.group(1))
        e1, e2 = m.group(2), m.group(3)
        if {e1.upper(), e2.upper()} == {"H75", "N81"}:
            target = {
                "cp_id": cp,
                "end1": e1,
                "end2": e2,
                "r1_ang": float(m.group(4)),
                "r2_ang": float(m.group(5)),
                "r1_r2_ratio": float(m.group(6)),
                "bond_path_angle_deg": float(m.group(7)),
            }
            break

    args.out.parent.mkdir(parents=True, exist_ok=True)

    fields = [
        "target",
        "bcp_found",
        "cp_id",
        "end1",
        "end2",
        "r1_ang",
        "r2_ang",
        "r1_r2_ratio",
        "bond_path_angle_deg",
        "rho_bcp",
        "laplacian_bcp",
        "ellipticity",
        "qc_status",
    ]

    row = {
        "target": "H75...N81",
        "bcp_found": "NO",
        "cp_id": "",
        "end1": "",
        "end2": "",
        "r1_ang": "",
        "r2_ang": "",
        "r1_r2_ratio": "",
        "bond_path_angle_deg": "",
        "rho_bcp": "",
        "laplacian_bcp": "",
        "ellipticity": "",
        "qc_status": "PASS_NO_TARGET_BCP",
    }

    if target is not None:
        cp = target["cp_id"]
        block_re = re.compile(
            rf"\+ Critical point no\.\s*{cp}\s*\n(.*?)(?=\n\+ Critical point no\.|\Z)",
            re.S,
        )
        bm = block_re.search(text)
        rho = lap = ell = None
        if bm:
            block = bm.group(1)
            m = re.search(r"Field value \(f\):\s*([+-]?[0-9.Ee]+)", block)
            if m:
                rho = float(m.group(1))
            m = re.search(r"Laplacian \(del2 f\):\s*([+-]?[0-9.Ee]+)", block)
            if m:
                lap = float(m.group(1))
            m = re.search(r"Ellipticity .*?:\s*([+-]?[0-9.Ee]+)", block)
            if m:
                ell = float(m.group(1))

        row.update({
            "bcp_found": "YES",
            "cp_id": cp,
            "end1": target["end1"],
            "end2": target["end2"],
            "r1_ang": f"{target['r1_ang']:.8f}",
            "r2_ang": f"{target['r2_ang']:.8f}",
            "r1_r2_ratio": f"{target['r1_r2_ratio']:.8f}",
            "bond_path_angle_deg": f"{target['bond_path_angle_deg']:.8f}",
            "rho_bcp": "" if rho is None else f"{rho:.10e}",
            "laplacian_bcp": "" if lap is None else f"{lap:.10e}",
            "ellipticity": "" if ell is None else f"{ell:.10e}",
            "qc_status": "PASS_TARGET_BCP_FOUND",
        })

    with args.out.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, delimiter="\t")
        w.writeheader()
        w.writerow(row)

    print(f"PASS: targeted QTAIM parser complete; bcp_found={row['bcp_found']}")
    if target:
        print(
            f"Target BCP cp={target['cp_id']} endpoints="
            f"{target['end1']}/{target['end2']}"
        )
        print(f"rho={row['rho_bcp']} laplacian={row['laplacian_bcp']}")
    else:
        print("No H75...N81 bond critical point was found under this targeted search.")
        print("This is a valid topological result and is not interpreted as absence of interaction.")


if __name__ == "__main__":
    main()
