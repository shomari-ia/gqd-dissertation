#!/usr/bin/env python3

from pathlib import Path
from collections import Counter
import hashlib


ROOT = Path(".")
INPUT_DIR = ROOT / "calculations/phase1_dft/b3lyp/inputs"

SYSTEMS = [
    {
        "run_id": "B3LYP-COOH-GQD-C1-004",
        "label": "corrected Class 1 / C1",
        "seed": ROOT / (
            "structures/prepared/"
            "cooh_gqd_class1_c1_b3lyp_v02_imag_plus_010A.xyz"
        ),
        "seed_sha256":
            "63c79218e8f76d23ba99280d2030512abfd6db6407eb408d5163cf4063885e41",
        "input": INPUT_DIR / (
            "cooh_gqd_class1_c1_b3lyp_optfreq_v03.com"
        ),
        "chk":
            "archive/chk/cooh_gqd_class1_c1_b3lyp_optfreq_v03.chk",
    },
    {
        "run_id": "B3LYP-COOH-GQD-C2-005",
        "label": "corrected Class 2 / C3",
        "seed": ROOT / (
            "structures/prepared/"
            "cooh_gqd_class2_c3_b3lyp_v02_imag_plus_010A.xyz"
        ),
        "seed_sha256":
            "1527707060436d1f1cbd173eb03fcb0dd15ef89b5c28d8d1fcda7c79a5ad8bc5",
        "input": INPUT_DIR / (
            "cooh_gqd_class2_c3_b3lyp_optfreq_v03.com"
        ),
        "chk":
            "archive/chk/cooh_gqd_class2_c3_b3lyp_optfreq_v03.chk",
    },
]

ROUTE = (
    "#p opt=(calcfc,tight,maxcycles=200) freq "
    "B3LYP/6-31G(d,p) "
    "EmpiricalDispersion=GD3BJ "
    "SCRF=(SMD,Solvent=Water) "
    "Int=UltraFine NoSymm"
)


def sha256(path):
    h = hashlib.sha256()

    with path.open("rb") as handle:
        for block in iter(
            lambda: handle.read(1024 * 1024),
            b"",
        ):
            h.update(block)

    return h.hexdigest()


def read_xyz(path):
    lines = path.read_text().splitlines()

    if len(lines) < 2:
        raise SystemExit(
            "ERROR: malformed XYZ {}".format(path)
        )

    n_atoms = int(lines[0])

    atom_lines = lines[2:2 + n_atoms]

    if len(atom_lines) != n_atoms:
        raise SystemExit(
            "ERROR: expected {} atom lines in {}".format(
                n_atoms,
                path,
            )
        )

    symbols = []

    for line in atom_lines:
        fields = line.split()

        if len(fields) != 4:
            raise SystemExit(
                "ERROR: malformed atom line in {}: {}".format(
                    path,
                    line,
                )
            )

        symbol = fields[0]

        if symbol not in ("C", "H", "O"):
            raise SystemExit(
                "ERROR: unexpected element {} in {}".format(
                    symbol,
                    path,
                )
            )

        # Validate Cartesian fields.
        float(fields[1])
        float(fields[2])
        float(fields[3])

        symbols.append(symbol)

    return n_atoms, symbols, atom_lines


INPUT_DIR.mkdir(parents=True, exist_ok=True)

print("===== COOH-GQD B3LYP V03 RETRY INPUT BUILD =====")
print("ROUTE={}".format(ROUTE))

for system in SYSTEMS:
    print()
    print("=" * 72)
    print(system["run_id"])
    print("=" * 72)

    if not system["seed"].is_file():
        raise SystemExit(
            "ERROR: missing seed {}".format(
                system["seed"]
            )
        )

    actual_seed_sha = sha256(system["seed"])

    print(
        "SEED_SHA256={}".format(
            actual_seed_sha
        )
    )

    if actual_seed_sha != system["seed_sha256"]:
        raise SystemExit(
            "ERROR: seed hash mismatch for {}".format(
                system["run_id"]
            )
        )

    if system["input"].exists():
        raise SystemExit(
            "ERROR: refusing to overwrite existing input {}".format(
                system["input"]
            )
        )

    if (ROOT / system["chk"]).exists():
        raise SystemExit(
            "ERROR: checkpoint collision {}".format(
                system["chk"]
            )
        )

    n_atoms, symbols, atom_lines = read_xyz(
        system["seed"]
    )

    formula = Counter(symbols)

    if n_atoms != 75:
        raise SystemExit(
            "ERROR: expected 75 atoms; found {}".format(
                n_atoms
            )
        )

    if formula != Counter(
        {
            "C": 55,
            "H": 18,
            "O": 2,
        }
    ):
        raise SystemExit(
            "ERROR: unexpected formula {}".format(
                dict(formula)
            )
        )

    # Preserve authoritative standardized atom order.
    expected_order = (
        ["C"] * 54
        + ["H"] * 17
        + ["C", "O", "O", "H"]
    )

    if symbols != expected_order:
        raise SystemExit(
            "ERROR: standardized atom order failed for {}".format(
                system["run_id"]
            )
        )

    title = (
        "{} | {} | v02 imaginary-mode PLUS 0.10 A retry"
    ).format(
        system["run_id"],
        system["label"],
    )

    parts = [
        "%chk={}".format(system["chk"]),
        "%mem=32GB",
        "%nprocshared=16",
        ROUTE,
        "",
        title,
        "",
        "0 1",
    ]

    parts.extend(atom_lines)

    # Explicit Gaussian terminal blank record.
    rendered = "\n".join(parts) + "\n\n"

    system["input"].write_text(rendered)

    raw = system["input"].read_bytes()

    trailing_newlines = (
        len(raw)
        - len(raw.rstrip(b"\n"))
    )

    print(
        "SEED={}".format(
            system["seed"]
        )
    )
    print("N_ATOMS={}".format(n_atoms))
    print("FORMULA=C55H18O2")
    print("ATOM_ORDER=PASS")
    print(
        "INPUT={}".format(
            system["input"]
        )
    )
    print(
        "CHK={}".format(
            system["chk"]
        )
    )
    print("CHARGE_MULT=0 1")
    print("MEM=32GB")
    print("NPROC=16")
    print("NOSYMM=YES")
    print("ULTRAFINE_GRID=YES")
    print("CALCFC=YES")
    print("TIGHT_OPT=YES")
    print("MAXCYCLES=200")
    print(
        "TRAILING_NEWLINES={}".format(
            trailing_newlines
        )
    )

    if trailing_newlines != 2:
        raise SystemExit(
            "ERROR: terminal Gaussian blank record failed"
        )

    if "%oldchk=" in rendered.lower():
        raise SystemExit(
            "ERROR: unexpected oldchk in Cartesian retry"
        )

    if "geom=check" in rendered.lower():
        raise SystemExit(
            "ERROR: unexpected geom=check in Cartesian retry"
        )

    print(
        "INPUT_SHA256={}".format(
            sha256(system["input"])
        )
    )
    print("INPUT_BUILD=PASS")

print()
print("ALL_B3LYP_V03_RETRY_INPUTS=PASS")
