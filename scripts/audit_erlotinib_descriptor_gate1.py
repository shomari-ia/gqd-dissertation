#!/usr/bin/env python3

from pathlib import Path
from cclib.io import ccread
import csv

MANIFEST = Path("archive_manifest.tsv")

CASES = [
    (
        "C1",
        "M062X-COOH-GQD-C1-001",
        Path("archive/logs/cooh_gqd_c1_m062x_smd_sp_v01.log"),
        Path("archive/chk/cooh_gqd_c1_m062x_smd_sp_v01.chk"),
        None,
    ),
    (
        "Erlotinib",
        "M062X-ERLOTINIB-001",
        Path("archive/logs/erlotinib_m062x_smd_sp_v01.log"),
        Path("archive/chk/erlotinib_m062x_smd_sp_v01.chk"),
        None,
    ),
    (
        "Flat",
        "M062X-COOH-GQD-ERLOTINIB-FLAT-001",
        Path("archive/logs/cooh_gqd_c1_erlotinib_flat_m062x_smd_sp_v01.log"),
        Path("archive/chk/cooh_gqd_c1_erlotinib_flat_m062x_smd_sp_v01.chk"),
        75,
    ),
    (
        "Slipped",
        "M062X-COOH-GQD-ERLOTINIB-SLIPPED-001",
        Path("archive/logs/cooh_gqd_c1_erlotinib_slipped_m062x_smd_sp_v01.log"),
        Path("archive/chk/cooh_gqd_c1_erlotinib_slipped_m062x_smd_sp_v01.chk"),
        75,
    ),
    (
        "Edge",
        "M062X-COOH-GQD-ERLOTINIB-EDGE-001",
        Path("archive/logs/cooh_gqd_c1_erlotinib_edge_m062x_smd_sp_v01.log"),
        Path("archive/chk/cooh_gqd_c1_erlotinib_edge_m062x_smd_sp_v01.chk"),
        75,
    ),
]

manifest = {}

with MANIFEST.open() as f:
    reader = csv.DictReader(f, delimiter="\t")
    for row in reader:
        manifest[row["file_path"]] = row

out = Path(
    "calculations/phase1_dft/descriptors/results/"
    "erlotinib_descriptor_gate1.tsv"
)

rows = []

for system, run_id, log, chk, split in CASES:

    if not log.is_file():
        raise SystemExit(f"ERROR: missing log: {log}")

    if not chk.is_file():
        raise SystemExit(f"ERROR: missing checkpoint: {chk}")

    log_rec = manifest.get(str(log))
    chk_rec = manifest.get(str(chk))

    if not log_rec or not chk_rec:
        raise SystemExit(
            f"ERROR: {system} log/checkpoint absent from archive manifest"
        )

    if log_rec["run_id"] != run_id or chk_rec["run_id"] != run_id:
        raise SystemExit(
            f"ERROR: manifest run-ID mismatch for {system}"
        )

    data = ccread(str(log))

    if data is None:
        raise SystemExit(f"ERROR: cclib failed: {log}")

    natoms = len(data.atomnos)

    has_coords = hasattr(data, "atomcoords")
    has_mo = hasattr(data, "moenergies") and hasattr(data, "homos")

    homo = lumo = gap = "NA"

    if has_mo:
        spin = 0
        h = int(data.homos[spin])
        energies = data.moenergies[spin]

        homo = float(energies[h])
        lumo = float(energies[h + 1])
        gap = lumo - homo

    charges = getattr(data, "atomcharges", {})
    charge_keys = ",".join(sorted(charges.keys())) if charges else "NONE"

    mull_gqd = "NA"
    mull_drug = "NA"

    if split is not None and "mulliken" in charges:
        q = charges["mulliken"]
        mull_gqd = float(sum(q[:split]))
        mull_drug = float(sum(q[split:]))

    status = (
        "PASS_EXISTING_EVIDENCE"
        if has_coords and has_mo
        else "REVIEW"
    )

    rows.append({
        "system": system,
        "run_id": run_id,
        "atoms": natoms,
        "coordinates": "YES" if has_coords else "NO",
        "mo_energies": "YES" if has_mo else "NO",
        "homo_ev": homo,
        "lumo_ev": lumo,
        "gap_ev": gap,
        "atomcharge_keys": charge_keys,
        "mulliken_gqd_charge": mull_gqd,
        "mulliken_drug_charge": mull_drug,
        "log_manifest": "PASS",
        "chk_manifest": "PASS",
        "gate1_status": status,
    })

with out.open("w", newline="") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=rows[0].keys(),
        delimiter="\t",
    )
    writer.writeheader()
    writer.writerows(rows)

print("PASS: descriptor Gate-1 audit complete.")
print(f"Wrote: {out}")

for r in rows:
    print(
        f'{r["system"]:10s} '
        f'atoms={r["atoms"]:3d} '
        f'MO={r["mo_energies"]} '
        f'gap={r["gap_ev"]} '
        f'charges={r["atomcharge_keys"]} '
        f'{r["gate1_status"]}'
    )
