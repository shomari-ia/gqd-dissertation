#!/usr/bin/env python3
"""Parse Critic2 molecular Hirshfeld/Hirshfeld-I output into fragment charges."""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path

Z = {"H": 1, "C": 6, "N": 7, "O": 8}
EXPECTED_ATOMS = 127
EXPECTED_ELECTRONS = 572.0
GQD_LAST_ATOM = 75

NUMBER = r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[Ee][+-]?\d+)?"

# Standard Hirshfeld table:
# nneq mult name N_hirsh V_hirsh
STANDARD_ROW = re.compile(
    rf"^\s*(\d+)\s+\d+\s+([A-Za-z]+)_\s+({NUMBER})\s+({NUMBER})"
)

# Hirshfeld-I table:
# nneq mult name Z nmin nmax N_HI q_HI
ITERATIVE_ROW = re.compile(
    rf"^\s*(\d+)\s+\d+\s+([A-Za-z]+)_\s+"
    rf"(\d+)\s+\d+\s+\d+\s+({NUMBER})\s+({NUMBER})"
)


def extract_standard_table(
    lines: list[str],
) -> list[tuple[int, str, float]]:
    marker = "# N_hirsh = atomic electron populations"
    try:
        start = next(i for i, line in enumerate(lines) if marker in line)
    except StopIteration as exc:
        raise SystemExit(f"ERROR: marker not found: {marker}") from exc

    rows: list[tuple[int, str, float]] = []
    seen: set[int] = set()

    for line in lines[start + 1 :]:
        m = STANDARD_ROW.match(line)
        if not m:
            if len(rows) >= EXPECTED_ATOMS:
                break
            continue

        atom = int(m.group(1))
        symbol = m.group(2).upper()
        pop = float(m.group(3))

        if atom in seen:
            continue
        if symbol not in Z:
            raise SystemExit(f"ERROR: unsupported element in standard table: {symbol}")

        rows.append((atom, symbol, pop))
        seen.add(atom)

        if len(rows) == EXPECTED_ATOMS:
            break

    validate_rows(rows, "standard Hirshfeld")
    return rows


def extract_iterative_table(
    lines: list[str],
) -> list[tuple[int, str, float]]:
    marker = "# N_HI = Hirshfeld-I population; q_HI = Z - N_HI"
    try:
        start = next(i for i, line in enumerate(lines) if marker in line)
    except StopIteration as exc:
        raise SystemExit(f"ERROR: marker not found: {marker}") from exc

    rows: list[tuple[int, str, float]] = []
    seen: set[int] = set()

    for line in lines[start + 1 :]:
        m = ITERATIVE_ROW.match(line)
        if not m:
            if len(rows) >= EXPECTED_ATOMS:
                break
            continue

        atom = int(m.group(1))
        symbol = m.group(2).upper()
        z_reported = int(m.group(3))
        pop = float(m.group(4))
        q_reported = float(m.group(5))

        if atom in seen:
            continue
        if symbol not in Z:
            raise SystemExit(f"ERROR: unsupported element in Hirshfeld-I table: {symbol}")
        if z_reported != Z[symbol]:
            raise SystemExit(
                f"ERROR: atom {atom} {symbol} has Critic2 Z={z_reported}, "
                f"expected {Z[symbol]}"
            )

        q_recomputed = Z[symbol] - pop
        if abs(q_recomputed - q_reported) > 1e-8:
            raise SystemExit(
                f"ERROR: atom {atom} Hirshfeld-I charge mismatch: "
                f"reported={q_reported:.10f}, recomputed={q_recomputed:.10f}"
            )

        rows.append((atom, symbol, pop))
        seen.add(atom)

        if len(rows) == EXPECTED_ATOMS:
            break

    validate_rows(rows, "Hirshfeld-I")
    return rows


def validate_rows(
    rows: list[tuple[int, str, float]],
    label: str,
) -> None:
    if len(rows) != EXPECTED_ATOMS:
        raise SystemExit(
            f"ERROR: expected {EXPECTED_ATOMS} rows in {label}; found {len(rows)}"
        )

    if [x[0] for x in rows] != list(range(1, EXPECTED_ATOMS + 1)):
        raise SystemExit(f"ERROR: {label} atom numbering is not exactly 1..127")


def summarize(rows: list[tuple[int, str, float]]) -> dict[str, float]:
    q_gqd = 0.0
    q_drug = 0.0
    electrons = 0.0

    for atom, symbol, pop in rows:
        electrons += pop
        q = Z[symbol] - pop

        if atom <= GQD_LAST_ATOM:
            q_gqd += q
        else:
            q_drug += q

    return {
        "electrons": electrons,
        "q_gqd": q_gqd,
        "q_drug": q_drug,
        "q_total": q_gqd + q_drug,
        "drug_to_gqd_e": -q_gqd,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("cro", type=Path)
    ap.add_argument("--pose", required=True)
    ap.add_argument("--analysis-id", required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()

    if not args.cro.is_file():
        raise SystemExit(f"ERROR: missing Critic2 output: {args.cro}")

    text = args.cro.read_text(errors="replace")
    lines = text.splitlines()

    if "CRITIC2 ended successfully" not in text:
        raise SystemExit("ERROR: Critic2 success marker absent")

    warning_match = re.search(
        r"CRITIC2 ended successfully \((\d+) WARNINGS?,\s*(\d+) COMMENTS?\)",
        text,
    )
    if not warning_match:
        raise SystemExit("ERROR: completion warning/comment summary not found")

    warnings = int(warning_match.group(1))
    comments = int(warning_match.group(2))

    if warnings != 0:
        raise SystemExit(f"ERROR: Critic2 completed with {warnings} warning(s)")

    conv = re.search(r"Hirshfeld-I converged in\s+(\d+)\s+iterations", text)
    if not conv:
        raise SystemExit("ERROR: Hirshfeld-I convergence marker absent")

    if re.search(r"\bpinned\b", text, flags=re.IGNORECASE):
        raise SystemExit("ERROR: pinned Hirshfeld-I atom detected")

    standard = extract_standard_table(lines)
    iterative = extract_iterative_table(lines)

    hs = summarize(standard)
    hi = summarize(iterative)

    for label, result in (("Hirshfeld", hs), ("Hirshfeld-I", hi)):
        if abs(result["electrons"] - EXPECTED_ELECTRONS) > 1e-3:
            raise SystemExit(
                f"ERROR: {label} electron total {result['electrons']:.8f} "
                f"is inconsistent with {EXPECTED_ELECTRONS:.1f}"
            )
        if abs(result["q_total"]) > 1e-3:
            raise SystemExit(
                f"ERROR: {label} fragment charges do not sum to neutrality: "
                f"{result['q_total']:.8f}"
            )

    args.out.parent.mkdir(parents=True, exist_ok=True)

    fields = [
        "pose",
        "analysis_id",
        "critic2_warnings",
        "critic2_comments",
        "hirshfeld_i_iterations",
        "hirshfeld_total_e",
        "hirshfeld_gqd_charge_e",
        "hirshfeld_drug_charge_e",
        "hirshfeld_drug_to_gqd_e",
        "hirshfeld_i_total_e",
        "hirshfeld_i_gqd_charge_e",
        "hirshfeld_i_drug_charge_e",
        "hirshfeld_i_drug_to_gqd_e",
        "qc_status",
    ]

    row = {
        "pose": args.pose,
        "analysis_id": args.analysis_id,
        "critic2_warnings": warnings,
        "critic2_comments": comments,
        "hirshfeld_i_iterations": int(conv.group(1)),
        "hirshfeld_total_e": f"{hs['electrons']:.8f}",
        "hirshfeld_gqd_charge_e": f"{hs['q_gqd']:.8f}",
        "hirshfeld_drug_charge_e": f"{hs['q_drug']:.8f}",
        "hirshfeld_drug_to_gqd_e": f"{hs['drug_to_gqd_e']:.8f}",
        "hirshfeld_i_total_e": f"{hi['electrons']:.8f}",
        "hirshfeld_i_gqd_charge_e": f"{hi['q_gqd']:.8f}",
        "hirshfeld_i_drug_charge_e": f"{hi['q_drug']:.8f}",
        "hirshfeld_i_drug_to_gqd_e": f"{hi['drug_to_gqd_e']:.8f}",
        "qc_status": "PASS",
    }

    with args.out.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, delimiter="\t")
        w.writeheader()
        w.writerow(row)

    print("PASS: Critic2 fragment-charge parsing complete.")
    print(f"Pose: {args.pose}")
    print(f"Hirshfeld:   GQD={hs['q_gqd']:+.6f} e  drug={hs['q_drug']:+.6f} e")
    print(f"Hirshfeld-I: GQD={hi['q_gqd']:+.6f} e  drug={hi['q_drug']:+.6f} e")
    print(f"Hirshfeld-I iterations: {int(conv.group(1))}")
    print(f"Wrote: {args.out}")


if __name__ == "__main__":
    main()
