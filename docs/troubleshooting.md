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



