#!/usr/bin/env python3

from pathlib import Path
from decimal import Decimal, getcontext

getcontext().prec = 28

HARTREE_TO_KCAL = Decimal("627.509474")

SUMDIR = Path("calculations/phase1_dft/m062x/summaries")
OUT = Path(
    "calculations/phase1_dft/m062x/results/"
    "erlotinib_m062x_validation.tsv"
)

FILES = {
    "C1": SUMDIR / "cooh_gqd_c1_m062x_smd_sp_v01.summary.txt",
    "Erlotinib": SUMDIR / "erlotinib_m062x_smd_sp_v01.summary.txt",
    "Flat": SUMDIR / "cooh_gqd_c1_erlotinib_flat_m062x_smd_sp_v01.summary.txt",
    "Slipped": SUMDIR / "cooh_gqd_c1_erlotinib_slipped_m062x_smd_sp_v01.summary.txt",
    "Edge": SUMDIR / "cooh_gqd_c1_erlotinib_edge_m062x_smd_sp_v01.summary.txt",
}

def read_summary(path):
    if not path.is_file():
        raise SystemExit(f"ERROR: missing summary: {path}")

    data = {}

    for line in path.read_text().splitlines():
        if not line.strip():
            continue

        parts = line.split(None, 1)

        if len(parts) == 2:
            data[parts[0]] = parts[1].strip()

    if data.get("qc_status") != "PASS":
        raise SystemExit(
            f"ERROR: {path} is not QC PASS"
        )

    if data.get("termination") != "NORMAL":
        raise SystemExit(
            f"ERROR: {path} did not terminate normally"
        )

    return data

data = {
    name: read_summary(path)
    for name, path in FILES.items()
}

e_c1 = Decimal(data["C1"]["scf_hartree"])
e_drug = Decimal(data["Erlotinib"]["scf_hartree"])

reference = e_c1 + e_drug

results = []

for pose in ("Flat", "Slipped", "Edge"):

    e_complex = Decimal(
        data[pose]["scf_hartree"]
    )

    bind_h = e_complex - reference
    bind_kcal = bind_h * HARTREE_TO_KCAL

    results.append({
        "pose": pose,
        "run_id": data[pose]["run_id"],
        "complex_hartree": e_complex,
        "binding_hartree": bind_h,
        "binding_kcal": bind_kcal,
    })

results.sort(
    key=lambda x: x["binding_kcal"]
)

lowest = results[0]["binding_kcal"]

OUT.parent.mkdir(parents=True, exist_ok=True)

with OUT.open("w") as f:

    f.write(
        "rank\tpose\trun_id\t"
        "c1_hartree\terlotinib_hartree\t"
        "complex_hartree\t"
        "binding_hartree\t"
        "binding_kcal_mol\t"
        "delta_vs_lowest_kcal_mol\n"
    )

    for rank, r in enumerate(results, 1):

        delta = r["binding_kcal"] - lowest

        f.write(
            f"{rank}\t"
            f'{r["pose"]}\t'
            f'{r["run_id"]}\t'
            f"{e_c1:.8f}\t"
            f"{e_drug:.8f}\t"
            f'{r["complex_hartree"]:.8f}\t'
            f'{r["binding_hartree"]:.8f}\t'
            f'{r["binding_kcal"]:.3f}\t'
            f"{delta:.3f}\n"
        )

print("PASS: M06-2X validation table generated.")
print()

for rank, r in enumerate(results, 1):

    delta = r["binding_kcal"] - lowest

    print(
        f'{rank}. {r["pose"]:8s} '
        f'Ebind={r["binding_kcal"]:8.3f} kcal/mol  '
        f'delta={delta:7.3f}'
    )

print()
print(f"Wrote: {OUT}")
