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
