#!/usr/bin/env python3

from pathlib import Path
from decimal import Decimal, getcontext
import csv
import re

getcontext().prec = 28

HARTREE_TO_KCAL = Decimal("627.509474")

POSE_TABLE = Path(
    "calculations/phase1_dft/b3lyp/results/"
    "erlotinib_pose_comparison.tsv"
)

OUT = Path(
    "calculations/phase1_dft/b3lyp/results/"
    "erlotinib_bsse_comparison.tsv"
)

LOGS = {
    "Flat": (
        "B3LYP-COOH-GQD-ERLOTINIB-FLAT-BSSE-002",
        Path(
            "archive/logs/"
            "cooh_gqd_c1_erlotinib_flat_b3lyp_bsse_v02.log"
        ),
    ),
    "Slipped": (
        "B3LYP-COOH-GQD-ERLOTINIB-SLIPPED-BSSE-002",
        Path(
            "archive/logs/"
            "cooh_gqd_c1_erlotinib_slipped_b3lyp_bsse_v02.log"
        ),
    ),
    "Edge": (
        "B3LYP-COOH-GQD-ERLOTINIB-EDGE-BSSE-002",
        Path(
            "archive/logs/"
            "cooh_gqd_c1_erlotinib_edge_b3lyp_bsse_v02.log"
        ),
    ),
}

raw_smd = {}

with POSE_TABLE.open() as f:
    reader = csv.DictReader(f, delimiter="\t")

    for row in reader:
        raw_smd[row["pose"]] = Decimal(
            row["raw_e_bind_kcal_mol"]
        )

def grab(pattern, text, label):
    m = re.search(
        pattern,
        text,
        flags=re.MULTILINE | re.IGNORECASE
    )

    if not m:
        raise SystemExit(f"ERROR: could not extract {label}")

    return Decimal(m.group(1))

results = []

for pose in ("Flat", "Slipped", "Edge"):

    run_id, log = LOGS[pose]

    if not log.is_file():
        raise SystemExit(f"ERROR: missing {log}")

    text = log.read_text(errors="replace")

    cp_energy = grab(
        r"^\s*Counterpoise corrected energy\s*=\s*"
        r"([-+0-9.Ee]+)",
        text,
        f"{pose} corrected energy",
    )

    bsse_h = grab(
        r"^\s*BSSE energy\s*=\s*([-+0-9.Ee]+)",
        text,
        f"{pose} BSSE",
    )

    cp_raw = grab(
        r"^\s*complexation energy\s*=\s*"
        r"([-+0-9.]+)\s+kcal/mole\s+\(raw\)",
        text,
        f"{pose} raw CP interaction",
    )

    cp_corr = grab(
        r"^\s*complexation energy\s*=\s*"
        r"([-+0-9.]+)\s+kcal/mole\s+\(corrected\)",
        text,
        f"{pose} corrected CP interaction",
    )

    bsse_kcal = bsse_h * HARTREE_TO_KCAL

    smd_raw = raw_smd[pose]

    corrected = smd_raw + bsse_kcal

    results.append({
        "pose": pose,
        "run_id": run_id,
        "raw_smd_binding_kcal_mol": smd_raw,
        "bsse_gas_hartree": bsse_h,
        "bsse_gas_kcal_mol": bsse_kcal,
        "smd_plus_gas_bsse_kcal_mol": corrected,
        "gaussian_cp_corrected_energy_hartree": cp_energy,
        "gas_cp_raw_interaction_kcal_mol": cp_raw,
        "gas_cp_corrected_interaction_kcal_mol": cp_corr,
    })

lowest = min(
    r["smd_plus_gas_bsse_kcal_mol"]
    for r in results
)

results.sort(
    key=lambda r: r["smd_plus_gas_bsse_kcal_mol"]
)

OUT.parent.mkdir(parents=True, exist_ok=True)

with OUT.open("w", newline="") as f:

    fields = [
        "rank",
        "pose",
        "run_id",
        "raw_smd_binding_kcal_mol",
        "bsse_gas_hartree",
        "bsse_gas_kcal_mol",
        "smd_plus_gas_bsse_kcal_mol",
        "delta_corrected_vs_lowest_kcal_mol",
        "gaussian_cp_corrected_energy_hartree",
        "gas_cp_raw_interaction_kcal_mol",
        "gas_cp_corrected_interaction_kcal_mol",
    ]

    writer = csv.DictWriter(
        f,
        fieldnames=fields,
        delimiter="\t"
    )

    writer.writeheader()

    for rank, r in enumerate(results, start=1):

        delta = (
            r["smd_plus_gas_bsse_kcal_mol"]
            - lowest
        )

        writer.writerow({
            "rank": rank,
            "pose": r["pose"],
            "run_id": r["run_id"],
            "raw_smd_binding_kcal_mol":
                f'{r["raw_smd_binding_kcal_mol"]:.3f}',
            "bsse_gas_hartree":
                f'{r["bsse_gas_hartree"]:.12f}',
            "bsse_gas_kcal_mol":
                f'{r["bsse_gas_kcal_mol"]:.3f}',
            "smd_plus_gas_bsse_kcal_mol":
                f'{r["smd_plus_gas_bsse_kcal_mol"]:.3f}',
            "delta_corrected_vs_lowest_kcal_mol":
                f"{delta:.3f}",
            "gaussian_cp_corrected_energy_hartree":
                f'{r["gaussian_cp_corrected_energy_hartree"]:.12f}',
            "gas_cp_raw_interaction_kcal_mol":
                f'{r["gas_cp_raw_interaction_kcal_mol"]:.2f}',
            "gas_cp_corrected_interaction_kcal_mol":
                f'{r["gas_cp_corrected_interaction_kcal_mol"]:.2f}',
        })

print("PASS: BSSE comparison generated.")
print()

for rank, r in enumerate(results, start=1):

    delta = (
        r["smd_plus_gas_bsse_kcal_mol"]
        - lowest
    )

    print(
        f'{rank}. {r["pose"]:8s} '
        f'raw SMD={r["raw_smd_binding_kcal_mol"]:8.3f}  '
        f'BSSE={r["bsse_gas_kcal_mol"]:7.3f}  '
        f'corrected={r["smd_plus_gas_bsse_kcal_mol"]:8.3f}  '
        f'delta={delta:6.3f}'
    )

print()
print(f"Wrote: {OUT}")
