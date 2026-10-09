## PubChem 3D unavailable for large/flexible drug — Venetoclax

**Observed system:** Venetoclax, PubChem CID 49846579

**Problem:**  
A PubChem PUG-REST request using `record_type=3d` returned a 404 response
instead of a valid SDF. Open Babel consequently reported that the MDL file
contained no atom/bond count.

**Resolution:**  
Use the authoritative PubChem 2D SDF as the locked molecular-graph source,
then perform a separately documented and validated 2D-to-3D conformer
generation step before force-field and quantum-chemical optimization.

**Reproducibility note:**  
Repeated PubChem 2D downloads may differ at the byte level because the
generated SDF header contains time-dependent metadata. Preserve one exact
accepted raw instance and record its checksum rather than assuming a future
download will reproduce the same SHA256.

**Accepted Venetoclax raw-source SHA256:**

    9dff3ed26809ef2ebe54b2260e188e7fd2383f74fdbfd99137a91eecfe68bf04





## Gaussian `End of file in ZSymb` after Cartesian coordinates

### Symptom

Gaussian terminates in Link 101 immediately after echoing the complete
Cartesian molecular specification:

    End of file in ZSymb.
    Error termination via Lnk1e .../l101.exe

The calculation may terminate within seconds, before any SCF energy or
optimization step is produced.

### Confirmed cause in corrected COOH-GQD PM6 v02 inputs

The Gaussian input contained the complete route section, charge/multiplicity,
and all 75 Cartesian coordinates, but the file ended immediately after the
last atom with only one newline byte.

Gaussian requires the molecular specification to be terminated by a blank
record. For these Cartesian inputs, the file therefore must end with two
newline bytes after the final atom:

    <last atom>\n\n

The failed v02 files ended with:

    <last atom>\n

Known successful project Gaussian inputs ended with the required terminal
blank line.

### Diagnostic

Use a byte-level check rather than relying only on a text editor:

    python - <<'PY'
    from pathlib import Path
    p = Path("input.com")
    data = p.read_bytes()
    print("trailing_newlines =", len(data) - len(data.rstrip(b"\n")))
    print("ends_with_blank_line =", data.endswith(b"\n\n"))
    PY

Expected for this project:

    trailing_newlines = 2
    ends_with_blank_line = True

### Correction

Fix the input-generation code so rendered Gaussian Cartesian inputs end with
an explicit terminal blank record.

Do not overwrite or reuse an input/run identifier that has already been
executed. Preserve the failed input, log, checkpoint, QC summary, and
provenance as immutable failure evidence. Generate a new input version and
new run identifier for the corrected retry.

### Advancement rule

A generated Gaussian Cartesian input must pass an EOF-format gate before
submission:

- complete route section;
- charge and multiplicity present;
- expected atom count present;
- exact intended Cartesian coordinates present;
- file ends with `\n\n`.

A Gaussian `End of file in ZSymb` failure at this stage is an input-format
failure, not evidence of a molecular-geometry or electronic-convergence
problem.

## B3LYP optimization completes but QC fails because of a COOH-localized imaginary frequency

### Symptom

A Gaussian `opt freq` calculation may terminate normally and report:

    Optimization completed.
    -- Stationary point found.
    Normal termination of Gaussian 16

but `scripts/verify_gaussian.sh` returns exit code 4 and the QC summary reports:

    imag_freq       1
    qc_status       FAILED

This is not a Gaussian execution failure. The geometry optimization completed,
but the frequency calculation shows that the stationary structure does not pass
the project's true-minimum gate.

### Confirmed COOH-GQD example

Corrected B3LYP Class-1/C1 and Class-2/C3 calculations each produced all 219
expected vibrational modes for a nonlinear 75-atom system, but each had one
negative frequency.

Class 1:

    imaginary frequency = -6.2326 cm^-1
    COOH displacement share = 96.788%

Class 2:

    imaginary frequency = -54.3969 cm^-1
    COOH displacement share = 93.843%

The graphene scaffold was not the dominant unstable coordinate.

Class 1 had relaxed to an almost coplanar COOH arrangement and the negative
mode was a very shallow out-of-plane COOH motion.

Class 2 retained an exactly perpendicular COOH orientation and Cs symmetry.
Its negative mode displaced the COOH away from that symmetry-associated
stationary geometry.

### Diagnostic procedure

1. Confirm normal Gaussian termination and completed optimization.
2. Count every `Frequencies --` value and verify the expected number of modes.
3. Count all negative frequencies rather than inspecting only the end of the
   frequency list.
4. Parse the imaginary-mode displacement vectors and identify which atoms
   dominate the mode.
5. Check molecular connectivity before and after any proposed mode
   displacement.
6. Test the positive and negative eigenvector directions for symmetry
   equivalence before scheduling duplicate calculations.

### Correction strategy

Do not overwrite the completed calculation and do not simply ignore a small
negative mode when the project acceptance rule requires zero imaginary
frequencies.

Preserve the original input, log, checkpoint, provenance, and QC summary as an
immutable failed-minimum lineage.

Construct a new retry seed by displacing the completed geometry a small,
documented distance along the imaginary normal-mode eigenvector. For the
corrected COOH-GQD candidates, a maximum atomic displacement of 0.10 A
preserved the full 93-bond molecular graph.

Generate both eigenvector signs initially when needed for diagnosis. If the
two directions are demonstrated to be mirror- or symmetry-equivalent, retain
that evidence and schedule only one deterministic branch to avoid duplicate
computation.

For a symmetry-associated saddle, disable symmetry in the retry optimization.
Use tighter optimization/numerical controls only as a documented recovery
measure; do not change the underlying scientific level of theory merely to
force a pass.

### Advancement rule

Normal termination plus `Optimization completed` is not sufficient for an
accepted optimized B3LYP structure.

For isolated COOH-GQD acceptance, the retry must achieve:

- normal Gaussian termination;
- completed optimization / stationary point;
- complete frequency calculation;
- zero imaginary frequencies;
- preserved C55H18O2 composition and atom order;
- preserved intended molecular connectivity and graphene topology;
- acceptable post-DFT structural deformation.

Only after both site-class candidates satisfy these gates may their matched
DFT energies and thermochemistry be used for authoritative site-class
selection.
