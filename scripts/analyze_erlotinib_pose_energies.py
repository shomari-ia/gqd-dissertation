#!/usr/bin/env python3

from pathlib import Path
from decimal import Decimal, getcontext
import csv

getcontext().prec = 28

HARTREE_TO_KCAL = Decimal("627.509474")

RUN_LOG = Path("run_log.tsv")
OUT = Path(
    "calculations/phase1_dft/b3lyp/results/"
    "erlotinib_pose_comparison.tsv"
)

IDS = {
    "gqd": "B3LYP-COOH-GQD-C1-004",
    "drug": "B3LYP-ERLOTINIB-001",
    "Flat": "B3LYP-COOH-GQD-ERLOTINIB-FLAT-001",
    "Slipped": "B3LYP-COOH-GQD-ERLOTINIB-SLIPPED-001",
    "Edge": "B3LYP-COOH-GQD-ERLOTINIB-EDGE-003",
}

rows = {}

with RUN_LOG.open() as f:
    reader = csv.DictReader(f, delimiter="\t")
    for row in reader:
        rows[row["run_id"]] = row

for key, run_id in IDS.items():
    if run_id not in rows:
        raise SystemExit(f"ERROR: missing required run: {run_id}")

for pose in ("Flat", "Slipped", "Edge"):
    row = rows[IDS[pose]]
    if row["status"] != "PASS":
        raise SystemExit(f"ERROR: {pose} is not execution PASS")
    if row["scientific_disposition"] != "ACCEPTED_ADSORPTION_MINIMUM":
        raise SystemExit(f"ERROR: {pose} is not scientifically accepted")

gqd_e = Decimal(rows[IDS["gqd"]]["scf_hartree"])
drug_e = Decimal(rows[IDS["drug"]]["scf_hartree"])

pose_data = {}

for pose in ("Flat", "Slipped", "Edge"):
    row = rows[IDS[pose]]
    e = Decimal(row["scf_hartree"])
    g = Decimal(row["gibbs_hartree"])

    raw_bind = e - gqd_e - drug_e

    pose_data[pose] = {
        "run_id": IDS[pose],
        "e": e,
        "g": g,
        "raw_bind": raw_bind,
    }

lowest_e = min(x["e"] for x in pose_data.values())
lowest_g = min(x["g"] for x in pose_data.values())

ranked = sorted(
    pose_data.items(),
    key=lambda item: item[1]["e"]
)

OUT.parent.mkdir(parents=True, exist_ok=True)

with OUT.open("w", newline="") as f:
    fieldnames = [
        "electronic_rank",
        "pose",
        "run_id",
        "scf_hartree",
        "gibbs_hartree",
        "delta_e_vs_lowest_kcal_mol",
        "delta_g_vs_lowest_kcal_mol",
        "raw_e_bind_hartree",
        "raw_e_bind_kcal_mol",
        "binding_status",
    ]

    writer = csv.DictWriter(
        f,
        fieldnames=fieldnames,
        delimiter="\t"
    )

    writer.writeheader()

    for rank, (pose, d) in enumerate(ranked, start=1):

        de = (d["e"] - lowest_e) * HARTREE_TO_KCAL
        dg = (d["g"] - lowest_g) * HARTREE_TO_KCAL
        bind_kcal = d["raw_bind"] * HARTREE_TO_KCAL

        writer.writerow({
            "electronic_rank": rank,
            "pose": pose,
            "run_id": d["run_id"],
            "scf_hartree": f"{d['e']:.8f}",
            "gibbs_hartree": f"{d['g']:.6f}",
            "delta_e_vs_lowest_kcal_mol": f"{de:.3f}",
            "delta_g_vs_lowest_kcal_mol": f"{dg:.3f}",
            "raw_e_bind_hartree": f"{d['raw_bind']:.8f}",
            "raw_e_bind_kcal_mol": f"{bind_kcal:.3f}",
            "binding_status": "PRE_BSSE",
        })

print("PASS: accepted pose set verified.")
print()
print("Pose ranking:")
for rank, (pose, d) in enumerate(ranked, start=1):
    de = (d["e"] - lowest_e) * HARTREE_TO_KCAL
    dg = (d["g"] - lowest_g) * HARTREE_TO_KCAL
    bind = d["raw_bind"] * HARTREE_TO_KCAL

    print(
        f"{rank}. {pose:8s} "
        f"dE={de:8.3f} kcal/mol  "
        f"dG={dg:8.3f} kcal/mol  "
        f"raw Ebind={bind:8.3f} kcal/mol"
    )

print()
print(f"Wrote: {OUT}")
