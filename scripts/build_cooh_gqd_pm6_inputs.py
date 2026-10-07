#!/usr/bin/env python3

import argparse
import hashlib
from collections import Counter
from pathlib import Path


SYSTEMS = (
    {
        "label": "Class 1",
        "representative": "C1",
        "run_id": "PM6-COOH-GQD-C1-008",
        "source": Path(
            "structures/prepared/cooh_gqd_class1_c1_v01.xyz"
        ),
        "source_sha256": (
            "33cda2addb0a7962dacab5fe3816a193"
            "5a520dbf8f183a57058c145c8ac01571"
        ),
        "output": Path(
            "calculations/phase1_dft/pm6/inputs/"
            "cooh_gqd_class1_c1_pm6_opt_v03.com"
        ),
        "chk": (
            "archive/chk/"
            "cooh_gqd_class1_c1_pm6_opt_v03.chk"
        ),
    },
    {
        "label": "Class 2",
        "representative": "C3",
        "run_id": "PM6-COOH-GQD-C2-009",
        "source": Path(
            "structures/prepared/cooh_gqd_class2_c3_v01.xyz"
        ),
        "source_sha256": (
            "c1c4856b9f7dc618ec4757dc131c844"
            "a82bbee473ddd114a3457ef8fe7815b73"
        ),
        "output": Path(
            "calculations/phase1_dft/pm6/inputs/"
            "cooh_gqd_class2_c3_pm6_opt_v03.com"
        ),
        "chk": (
            "archive/chk/"
            "cooh_gqd_class2_c3_pm6_opt_v03.chk"
        ),
    },
)


def sha256_file(path):
    digest = hashlib.sha256()

    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)

    return digest.hexdigest()


def validate_xyz(system):
    path = system["source"]

    if not path.is_file():
        raise RuntimeError(
            "Missing source XYZ: {}".format(path)
        )

    observed_sha = sha256_file(path)

    if observed_sha != system["source_sha256"]:
        raise RuntimeError(
            "Source SHA256 mismatch for {}: expected {}, observed {}".format(
                path,
                system["source_sha256"],
                observed_sha,
            )
        )

    lines = path.read_text().splitlines()

    if len(lines) != 77:
        raise RuntimeError(
            "{}: expected 77 XYZ lines, observed {}".format(
                path,
                len(lines),
            )
        )

    try:
        atom_count = int(lines[0].strip())
    except ValueError as exc:
        raise RuntimeError(
            "{}: invalid XYZ atom-count line".format(path)
        ) from exc

    if atom_count != 75:
        raise RuntimeError(
            "{}: expected 75 atoms, observed {}".format(
                path,
                atom_count,
            )
        )

    atom_lines = lines[2:]

    if len(atom_lines) != 75:
        raise RuntimeError(
            "{}: expected 75 coordinate lines, observed {}".format(
                path,
                len(atom_lines),
            )
        )

    elements = []

    for atom_number, line in enumerate(atom_lines, start=1):
        fields = line.split()

        if len(fields) != 4:
            raise RuntimeError(
                "{} atom {}: expected element + 3 coordinates".format(
                    path,
                    atom_number,
                )
            )

        element = fields[0]

        try:
            float(fields[1])
            float(fields[2])
            float(fields[3])
        except ValueError as exc:
            raise RuntimeError(
                "{} atom {}: invalid Cartesian coordinate".format(
                    path,
                    atom_number,
                )
            ) from exc

        elements.append(element)

    counts = Counter(elements)

    expected_formula = {
        "C": 55,
        "H": 18,
        "O": 2,
    }

    if dict(counts) != expected_formula:
        raise RuntimeError(
            "{}: formula mismatch: observed {}".format(
                path,
                dict(counts),
            )
        )

    if elements[:54] != ["C"] * 54:
        raise RuntimeError(
            "{}: atoms 1-54 are not all scaffold carbon".format(path)
        )

    if elements[54:71] != ["H"] * 17:
        raise RuntimeError(
            "{}: atoms 55-71 are not all retained edge hydrogen".format(
                path
            )
        )

    expected_tail = ["C", "O", "O", "H"]

    if elements[71:75] != expected_tail:
        raise RuntimeError(
            "{}: atoms 72-75 are not C/O/O/H".format(path)
        )

    return atom_lines, observed_sha


def render_input(system, atom_lines):
    title = (
        "COOH-GQD {} ({}) PM6 pre-optimization | "
        "corrected v03 | charge=0 mult=1"
    ).format(
        system["label"],
        system["representative"],
    )

    parts = [
        "%chk={}".format(system["chk"]),
        "%mem=8GB",
        "%nprocshared=8",
        "#p PM6 opt SCF=XQC",
        "",
        title,
        "",
        "0 1",
    ]

    parts.extend(atom_lines)

    text = "\n".join(parts) + "\n\n"

    if not text.endswith("\n\n"):
        raise RuntimeError(
            "{} rendered input is missing the terminal blank line".format(
                system["label"]
            )
        )

    if text.endswith("\n\n\n"):
        raise RuntimeError(
            "{} rendered input has more than one terminal blank record".format(
                system["label"]
            )
        )

    return text


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Validate corrected COOH-GQD Class-1/Class-2 XYZ sources "
            "and deterministically generate PM6 v03 Gaussian retry inputs."
        )
    )

    parser.add_argument(
        "--write",
        action="store_true",
        help="Write validated Gaussian input files.",
    )

    args = parser.parse_args()

    rendered = []

    for system in SYSTEMS:
        atom_lines, source_sha = validate_xyz(system)
        text = render_input(system, atom_lines)

        rendered.append(
            (
                system,
                source_sha,
                text,
            )
        )

    print("COOH-GQD corrected PM6 v03 input validation = PASS")

    for system, source_sha, text in rendered:
        print("")
        print("LABEL={}".format(system["label"]))
        print("REPRESENTATIVE={}".format(system["representative"]))
        print("RUN_ID={}".format(system["run_id"]))
        print("SOURCE={}".format(system["source"]))
        print("SOURCE_SHA256={}".format(source_sha))
        print("OUTPUT={}".format(system["output"]))
        print("CHECKPOINT={}".format(system["chk"]))
        print("ATOMS=75")
        print("FORMULA=C55H18O2")
        print("CHARGE=0")
        print("MULTIPLICITY=1")
        print("ROUTE=#p PM6 opt SCF=XQC")
        print("MEMORY=8GB")
        print("NPROC=8")
        print("TERMINAL_BLANK_LINE=PASS")

        if args.write:
            output = system["output"]

            if output.exists():
                raise RuntimeError(
                    "Refusing to overwrite existing input: {}".format(
                        output
                    )
                )

            output.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            output.write_text(text)

            print(
                "WROTE={}".format(output)
            )
            print(
                "INPUT_SHA256={}".format(
                    sha256_file(output)
                )
            )

    if not args.write:
        print("")
        print("DRY RUN ONLY: no Gaussian input files were written.")


if __name__ == "__main__":
    main()
