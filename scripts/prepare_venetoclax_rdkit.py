#!/usr/bin/env python3

import csv
import os
import rdkit
from rdkit import Chem
from rdkit.Chem import AllChem, rdMolDescriptors

SRC = "structures/raw/venetoclax_pubchem_cid49846579_2d.sdf"
OUT_SDF = "structures/prepared/venetoclax_rdkit_mmff94_prep_v01.sdf"
OUT_TSV = "structures/prepared/venetoclax_rdkit_mmff94_prep_v01.energies.tsv"

NCONFS = 100
SEED = 20260922
PRUNE_RMS = 0.75
MAX_ITERS = 2000

print("RDKit version =", rdkit.__version__)
print("source =", SRC)
print("conformers_requested =", NCONFS)
print("random_seed =", SEED)
print("prune_rms_A =", PRUNE_RMS)
print("MMFF_variant = MMFF94")
print("num_threads = 1")

os.makedirs(os.path.dirname(OUT_SDF), exist_ok=True)

suppl = Chem.SDMolSupplier(SRC, removeHs=True)
mol = next((m for m in suppl if m is not None), None)

if mol is None:
    raise RuntimeError("Failed to read Venetoclax raw SDF")

raw_formula = rdMolDescriptors.CalcMolFormula(mol)
raw_smiles = Chem.MolToSmiles(mol, canonical=True)
raw_charge = Chem.GetFormalCharge(mol)

if raw_formula != "C45H50ClN7O7S":
    raise RuntimeError("Unexpected formula: {}".format(raw_formula))

if raw_charge != 0:
    raise RuntimeError("Unexpected formal charge: {}".format(raw_charge))

molH = Chem.AddHs(mol)

if not AllChem.MMFFHasAllMoleculeParams(molH):
    raise RuntimeError("MMFF94 does not parameterize all atoms")

params = AllChem.ETKDGv3()
params.randomSeed = SEED
params.pruneRmsThresh = PRUNE_RMS
params.useSmallRingTorsions = True
params.useMacrocycleTorsions = True
params.enforceChirality = True
params.numThreads = 1

cids = list(
    AllChem.EmbedMultipleConfs(
        molH,
        numConfs=NCONFS,
        params=params
    )
)

if not cids:
    raise RuntimeError("ETKDGv3 embedding produced no conformers")

results = AllChem.MMFFOptimizeMoleculeConfs(
    molH,
    numThreads=1,
    maxIters=MAX_ITERS,
    mmffVariant="MMFF94"
)

rows = []

for cid, result in zip(cids, results):
    status, energy = result
    rows.append({
        "conf_id": int(cid),
        "converged": 1 if status == 0 else 0,
        "status_code": int(status),
        "energy_kcal_mol": float(energy),
    })

converged = [r for r in rows if r["converged"] == 1]

if not converged:
    raise RuntimeError("No MMFF94 conformer converged")

converged.sort(
    key=lambda r: (r["energy_kcal_mol"], r["conf_id"])
)

best = converged[0]
best_cid = best["conf_id"]

molH.SetProp("source_file", SRC)
molH.SetProp("prep_method", "RDKit ETKDGv3 + MMFF94")
molH.SetProp("rdkit_version", rdkit.__version__)
molH.SetProp("random_seed", str(SEED))
molH.SetProp("conformers_requested", str(NCONFS))
molH.SetProp("num_conformers_generated", str(len(cids)))
molH.SetProp("num_conformers_converged", str(len(converged)))
molH.SetProp("selected_conf_id", str(best_cid))
molH.SetProp(
    "selected_energy_kcal_mol",
    "{:.6f}".format(best["energy_kcal_mol"])
)
molH.SetProp("formula", rdMolDescriptors.CalcMolFormula(molH))
molH.SetProp("canonical_smiles_noH", raw_smiles)

writer = Chem.SDWriter(OUT_SDF)
writer.write(molH, confId=best_cid)
writer.close()

rows.sort(
    key=lambda r: (
        -r["converged"],
        r["energy_kcal_mol"],
        r["conf_id"]
    )
)

with open(OUT_TSV, "w", newline="") as f:
    writer = csv.writer(f, delimiter="\t")
    writer.writerow([
        "rank",
        "conf_id",
        "converged",
        "status_code",
        "energy_kcal_mol"
    ])

    for rank, row in enumerate(rows, start=1):
        writer.writerow([
            rank,
            row["conf_id"],
            row["converged"],
            row["status_code"],
            "{:.6f}".format(row["energy_kcal_mol"])
        ])

print("embedded_conformers =", len(cids))
print("converged_conformers =", len(converged))
print("selected_conf_id =", best_cid)
print(
    "selected_energy_kcal_mol =",
    "{:.6f}".format(best["energy_kcal_mol"])
)
print("wrote =", OUT_SDF)
print("wrote =", OUT_TSV)
