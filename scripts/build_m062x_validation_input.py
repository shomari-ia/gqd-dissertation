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
parser.add_argument("--source-run-id", required=True)
parser.add_argument("--chk", required=True)
parser.add_argument("--expected-atoms", type=int, required=True)
parser.add_argument("--charge", type=int, default=0)
parser.add_argument("--multiplicity", type=int, default=1)

args = parser.parse_args()

log = Path(args.log)
out = Path(args.output)

if not log.is_file():
    raise SystemExit(f"ERROR: source log missing: {log}")

if out.exists():
    raise SystemExit(f"ERROR: refusing to overwrite: {out}")

data = ccread(str(log))

if data is None:
    raise SystemExit(f"ERROR: cclib could not parse {log}")

coords = data.atomcoords[-1]
atomnos = [int(x) for x in data.atomnos]

if len(atomnos) != args.expected_atoms:
    raise SystemExit(
        f"ERROR: expected {args.expected_atoms} atoms; "
        f"parsed {len(atomnos)}"
    )

symbols = []

for z in atomnos:
    if z not in Z_TO_SYMBOL:
        raise SystemExit(f"ERROR: unsupported atomic number: {z}")
    symbols.append(Z_TO_SYMBOL[z])

lines = [
    f"%chk={args.chk}",
    "%mem=32GB",
    "%nprocshared=16",
    (
        "#p M062X/6-311+G(d,p) "
        "SCRF=(SMD,Solvent=Water) "
        "Int=UltraFine NoSymm"
    ),
    "",
    (
        f"{args.run_id} | M06-2X validation single point | "
        f"source={args.source_run_id}"
    ),
    "",
    f"{args.charge} {args.multiplicity}",
]

for symbol, xyz in zip(symbols, coords):
    lines.append(
        f"{symbol:<2s}"
        f"  {xyz[0]: .10f}"
        f"  {xyz[1]: .10f}"
        f"  {xyz[2]: .10f}"
    )

lines.append("")
lines.append("")

out.parent.mkdir(parents=True, exist_ok=True)
out.write_text("\n".join(lines))

print(f"PASS: wrote {out}")
print(f"Source: {args.source_run_id}")
print(f"Atoms: {len(symbols)}")
print(f"Charge/multiplicity: {args.charge} {args.multiplicity}")
