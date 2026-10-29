# GQD Computational Research Journal — Publication / Defense Edition

**Status:** Living publication template  
**Controlled date:** 2026-10-29  
**Relationship to audit record:** Derived from `LAB_JOURNAL.md`; never replaces it.

## Purpose

Create a concise, visually organized, printable scientific record for dissertation defense display, long-term project records, committee review, and future publication/portfolio use.

The publication edition is curated around scientific milestones rather than raw execution chronology.

## Design language

- Primary typeface: Georgia.
- Palette: black, charcoal, light gray, white, with restrained muted-gold accents in the print edition.
- Layout: generous white space; strong section dividers; one dominant scientific question per spread.
- Figures: only evidence-bearing figures; captions must identify the scientific claim.
- Tables: compact, bordered, minimal.
- Tone: precise, scientific, readable, not conversational.
- Density rule: no page should reproduce raw terminal output unless the output itself is the evidence.

## Defining principles

1. **Computational convergence is not equivalent to scientific validity.**
2. **Never delete a failed calculation; classify it.**
3. **A retry receives a new RUN_ID.**
4. **Execution/QC status and scientific disposition are separate facts.**
5. **A number without a traceable RUN_ID does not enter the dissertation.**
6. **Supersession preserves history while changing scientific eligibility.**
7. **Independent validation must test the molecular model, not only the software's success markers.**
8. **Infrastructure failure is not chemical failure.**
9. **Accepted monomers are immutable inputs to deterministic complex construction.**
10. **Committee-facing claims should be shorter than the evidence chain that supports them.**

## Front matter

### Cover

**GQD Computational Research Journal**  
*Scientific Development, Evidence, Decisions & Reproducibility Record*

Shomari A. Johnson  
Jackson State University  
Computational Data Enabled Science and Engineering  
Interdisciplinary Center for Nanotoxicity

### Inside cover / publication note

This journal is a curated scientific record derived from the canonical GQD dissertation repository, Lab Journal, run ledger, archive manifest, Scientific Evidence Register, and Supersession Register.

The audit record remains authoritative for exact chronology.

### How to read this journal

Each milestone answers five questions:

1. What scientific question was being addressed?
2. What evidence was generated?
3. What passed or failed?
4. What decision changed the project state?
5. What became authorized next?

### Notation / status key

- **PASS** — execution/QC pass.
- **ACCEPTED** — passed all applicable scientific gates.
- **HOLD** — insufficient evidence to advance.
- **SUPERSEDED** — preserved history, no longer current scientific baseline.
- **QUARANTINED** — preserved but barred from scientific reuse.
- **RETAINED FAILURE** — failed run kept as diagnostic or infrastructure evidence.
- **RELEASED** — authorized for downstream scientific use.

## Suggested book sections

### I. Research Architecture
- dissertation question;
- three-phase model;
- drug set and targets;
- computational method stack;
- evidence-control architecture.

### II. Reproducibility Foundation
- Git/HPC/Drive architecture;
- run ID concept;
- provenance;
- archive/checksum control;
- failure classification.

### III. The Carrier Model
- original COOH-GQD concept;
- discovery of the structural problem;
- deterministic circumcoronene rebuild;
- C1/C2 site-class comparison;
- authoritative C1 selection.

### IV. Isolated Drug Baselines
- Erlotinib;
- Gefitinib;
- Venetoclax;
- ABT-737.

Each drug receives a compact identity / method / accepted run / geometry / energy card.

### V. Phase I — Drug Loading
- Erlotinib adsorption;
- Gefitinib adsorption;
- Venetoclax adsorption;
- ABT-737 adsorption;
- BSSE / validation / electronic descriptors;
- comparative Phase I synthesis.

### VI. Phase II — pH-Responsive Release
- state construction;
- energetics;
- release scans;
- comparative release interpretation.

### VII. Phase III — Target Validation
- docking validation;
- free vs released drug;
- MD production;
- trajectory analysis;
- MM/PBSA or MM/GBSA.

### VIII. Problems, Corrections & Scientific Lessons
A curated set of the most important failure/correction events:
- malformed historical GQD;
- Gaussian input-format failures;
- imaginary-frequency recovery;
- archive/provenance repair;
- Maple edge infrastructure failure;
- Maple → Magnolia validation.

### IX. Integrated Findings
- cross-phase evidence;
- limitations;
- what the calculations support;
- what they do not establish;
- future experimental work.

### X. Final Evidence Index
- accepted run index;
- supersession map;
- software/platform versions;
- final repository checkpoint;
- selected QR links to evidence packages.

## Milestone spread template

### Milestone [###] — [Title]

**Scientific question**  
One to three sentences.

**Why it mattered**  
Short statement of the decision at stake.

**Starting state**  
Only the facts needed to understand the milestone.

**Evidence generated**
- RUN_ID(s)
- method / platform
- key geometry or validation figures
- energies / frequencies / topology facts
- archive/checksum reference

**Decision**
One clear sentence.

**Scientific disposition**
Controlled code.

**Defining principle**
One principle or lesson.

**What changed next**
One concise advancement statement.

**Evidence links**
- Scientific Evidence ID
- SEP ID
- repository path
- archive RUN_ID folder
- optional QR code in print edition

## Failure / correction spread template

### Correction Record — [Issue]

**Observed problem**  
What failed.

**Failure class**  
Structural / frequency / input-format / infrastructure / provenance / platform.

**What the evidence ruled out**  
Prevent overinterpretation.

**Root cause**

**Correction**

**Validation after correction**

**Scientific effect**
What was superseded, retained, or released.

**Lesson**
One sentence.

## Calculation evidence card template

| Field | Value |
|---|---|
| RUN_ID | |
| Scientific system | |
| Formula / atom count | |
| Method | |
| Solvent | |
| Platform / software | |
| Scheduler / job | |
| QC status | |
| Imaginary frequencies | |
| SCF | |
| Gibbs | |
| Scientific disposition | |
| Archive status | |
| Evidence ID | |

## Figure rules

Every figure must answer a question.

Preferred figure classes:
- corrected vs historical geometry;
- pose comparison;
- NCI / QTAIM evidence;
- energy comparison;
- pH-response curve;
- docking pose;
- MD stability plot;
- workflow/evidence architecture.

Each caption should include:
- what is shown;
- why it matters;
- run/evidence identifier when relevant.

## Seed milestone list from the current project

1. Reproducibility architecture established.
2. Historical COOH-GQD lineage accepted computationally.
3. Structural/topology defect discovered.
4. Historical carrier superseded.
5. Deterministic circumcoronene rebuild.
6. C1/C2 corrected site classes validated.
7. C1 authoritative baseline selected.
8. Isolated drug baselines completed.
9. Corrected Erlotinib flat/slipped/edge lineages constructed.
10. Flat and slipped adsorption minima accepted.
11. Edge Maple execution retained as infrastructure failure.
12. Magnolia platform validated and released.
13. Scientific Evidence / Acceptance Gate control layer established.

Future milestones are added only when the canonical scientific state changes.

## Update rule

The publication journal is updated after a **scientific milestone**, not after every HPC command.

A milestone qualifies when one or more of the following changes:
- authoritative baseline;
- accepted scientific result;
- failure classification;
- supersession;
- platform release;
- advancement gate;
- phase completion;
- committee-level scientific interpretation.

Raw chronology remains in `LAB_JOURNAL.md`.

## Print plan

Working print format:
- US Letter portrait;
- optional landscape foldout/inserts for wide scientific tables;
- high-quality matte paper;
- grayscale-safe design with restrained gold accent;
- section tabs/dividers;
- final bound copy for defense table and archival record.

The final edition should be exported to print-ready PDF only after the dissertation scientific state is frozen.
