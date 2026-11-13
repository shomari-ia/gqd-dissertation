#!/usr/bin/env python3

from pathlib import Path
import argparse
from cclib.io import ccread

Z_TO_SYMBOL = {
    1: "H",
    6: "C",
    7: "N",
    8: "O",
}

parser = argparse.ArgumentParser()

parser.add_argument("--log", required=True)
parser.add_argument("--output", required=True)
parser.add_argument("--run-id", required=True)
parser.add_argument("--chk", required=True)
parser.add_argument("--fragment-split", type=int, required=True)

args = parser.parse_args()

log = Path(args.log)
out = Path(args.output)

if not log.is_file():
    raise SystemExit(f"ERROR: missing source log: {log}")

if out.exists():
    raise SystemExit(f"ERROR: refusing to overwrite: {out}")

data = ccread(str(log))

if data is None:
    raise SystemExit("ERROR: cclib could not parse source log")

coords = data.atomcoords[-1]
atomnos = data.atomnos

symbols = []

for z in atomnos:
    z = int(z)
    if z not in Z_TO_SYMBOL:
        raise SystemExit(f"ERROR: unsupported atomic number {z}")
    symbols.append(Z_TO_SYMBOL[z])

n = len(symbols)

if not (0 < args.fragment_split < n):
    raise SystemExit("ERROR: invalid fragment split")

# Current GQD/Erlotinib scientific model:
# fragment 1 = neutral singlet C55H18O2 GQD
# fragment 2 = neutral singlet Erlotinib
# total complex = neutral singlet

lines = [
    f"%chk={args.chk}",
    "%mem=32GB",
    "%nprocshared=16",
    (
        "#p B3LYP/6-31G(d,p) EmpiricalDispersion=GD3BJ "
        "Counterpoise=2 SCRF=(SMD,Solvent=Water) "
        "Int=UltraFine NoSymm"
    ),
    "",
    f"{args.run_id} | accepted B3LYP geometry | Counterpoise=2 | v01",
    "",
    "0 1 0 1 0 1",
]

for i, (symbol, xyz) in enumerate(zip(symbols, coords)):
    fragment = 1 if i < args.fragment_split else 2

    lines.append(
        f"{symbol}(Fragment={fragment})"
        f"  {xyz[0]: .10f}"
        f"  {xyz[1]: .10f}"
        f"  {xyz[2]: .10f}"
    )

# Gaussian molecular specification terminator.
lines.append("")
lines.append("")

out.parent.mkdir(parents=True, exist_ok=True)
out.write_text("\n".join(lines))

print(f"PASS: wrote {out}")
print(f"Atoms: {n}")
print(f"Fragment 1: {args.fragment_split}")
print(f"Fragment 2: {n - args.fragment_split}")
