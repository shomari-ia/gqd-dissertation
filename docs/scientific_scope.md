# GQD Dissertation — Scientific Scope

## Purpose

This document defines the canonical scientific scope of the GQD dissertation
computational project.

It answers the question:

> What molecular systems, computational models, scientific endpoints, and
> validation criteria belong to the dissertation?

This file is distinct from:

- `docs/computational_workflow.md`, which defines how the calculations progress;
- `run_log.tsv`, which records individual computational jobs;
- `LAB_JOURNAL.md`, which records scientific decisions, observations, problems,
  interpretations, and work-session history;
- the Reproducibility Build Journal, which records infrastructure development
  and corrections.

Changes to the scientific scope must be intentional, scientifically justified,
documented in `LAB_JOURNAL.md`, and committed to Git.

---

## 1. Scientific Objective

The dissertation investigates functionalized graphene quantum dots as
computationally characterized nanocarriers for anticancer drug delivery.

The project integrates:

1. quantum-chemical characterization of drug loading,
2. pH-dependent drug-release behavior, and
3. biological target validation using molecular docking and molecular dynamics.

The central objective is to determine whether a carboxyl-functionalized
graphene quantum dot can bind selected anticancer drugs favorably, alter
drug-carrier interaction strength under different protonation conditions,
and allow the released drug to retain biologically relevant target binding.

---

## 2. GQD Model

### Base structure

Circumcoronene graphene quantum dot:

    C54H18

The structure is used as the finite graphene-like carbon framework.

### Functionalized structure

Primary dissertation model:

    monocarboxylated circumcoronene
    COOH-GQD
    molecular composition: C55H18O2

A single edge hydrogen of circumcoronene is replaced by a carboxyl
functional group (-COOH).

### Current accepted structure

Accepted tracked pre-optimization:

    RUN_ID: PM6-COOH-GQD-005

The optimized structure contains:

    75 total atoms
    55 carbon atoms
    18 hydrogen atoms
    2 oxygen atoms

Direct Cartesian validation of the accepted PM6 geometry identified:

    carboxyl carbon: Gaussian atom 58
    oxygen atoms: Gaussian atoms 73 and 74

Distances:

    C58-O73 = 1.2096 Å
    C58-O74 = 1.3796 Å
    C58-C40 = 1.4618 Å

The geometry therefore passes the current COOH-GQD connectivity gate.

---

## 3. Functionalization Strategy

The primary model contains one carboxyl group attached to an edge carbon
of circumcoronene.

Scientific roles of the carboxyl functionality include:

- modifying drug-GQD interactions,
- providing a chemically responsive functional site,
- enabling comparison of protonated (-COOH) and deprotonated (-COO-)
  states during Phase II,
- providing the principal functionalization model for the dissertation.

Additional functionalization densities or alternative functional groups are
outside the canonical scope unless explicitly approved and documented as
an extension study.

---

## 4. Drug Set

### Current documented Phase I drug set

The existing Computational Guide and Dissertation Execution Plan specify:

| Drug | Primary target context |
|---|---|
| Erlotinib | EGFR |
| Gefitinib | EGFR |
| Venetoclax (ABT-199) | Bcl-2 |
| ABT-737 | Bcl-2 |

### Scope status

DRUG SET STATUS: PENDING FINAL SCOPE LOCK

These four drugs constitute the currently documented computational plan.

Before tracked PM6 calculations for all drug systems are launched, the drug
set will be formally confirmed in the Work Journal and this section will be
changed from `PENDING FINAL SCOPE LOCK` to `LOCKED`.

Once locked, substitution or removal of a drug requires a documented
scientific rationale and Git-tracked scope amendment.

---

## 5. Protein Targets

### EGFR

Primary receptor target for EGFR-directed compounds.

Candidate structures documented in the execution plan:

    PDB 1M17
    PDB 4HJO
    PDB 4WKQ

Principal site:

    ATP-binding pocket / kinase domain

### Bcl-2

Primary receptor target for Bcl-2-directed compounds.

Candidate structures documented in the execution plan:

    PDB 6O0K
    PDB 4LVT
    PDB 4LXD

Principal site:

    BH3-binding groove

Final receptor structure selection must be validated and documented before
production docking.

---

## 6. Computational Levels of Theory

### PM6 pre-optimization

Purpose:

    inexpensive geometry cleanup before higher-level DFT

Software:

    Gaussian 16

PM6 structures are not used as substitutes for final DFT energetic results.
Their primary role is geometry preparation and workflow validation.

### Primary DFT optimization and frequency level

    B3LYP-D3(BJ)/6-31G(d,p)

Gaussian dispersion keyword:

    EmpiricalDispersion=GD3BJ

Solvation:

    SMD water

Primary task:

    geometry optimization + frequency analysis

Frequency calculations are required to characterize optimized stationary
points and determine whether structures represent minima.

### Validation single-point level

    M06-2X/6-311+G(d,p)

Solvation:

    SMD water

Purpose:

    higher-level energetic validation of selected optimized structures

GD3BJ is not added to the M06-2X validation calculation under the current
protocol.

---

## 7. Solvent Model

Primary implicit solvent environment:

    water

Gaussian model:

    SCRF=(SMD,Solvent=Water)

Comparative energies must be generated using compatible methods, basis
sets, and solvent definitions.

Gas-phase and solvated energies must not be mixed within a binding-energy
comparison.

---

## 8. Phase I — GQD Drug Loading

### Scientific question

How favorably do the selected anticancer drugs interact with the
carboxyl-functionalized GQD, and what electronic interactions contribute
to loading?

### Core workflow

Individual species optimization
→ drug-GQD complex generation
→ complex optimization
→ frequency verification
→ binding-energy analysis
→ electronic-structure characterization

### Primary endpoints

- optimized isolated species,
- optimized drug-GQD complexes,
- frequency verification,
- electronic energies,
- Gibbs free-energy quantities where applicable,
- binding energies,
- BSSE-corrected interaction energies,
- M06-2X validation energies,
- HOMO-LUMO gaps,
- charge-transfer descriptors,
- non-covalent interaction characterization,
- QTAIM/NCI/ELF/DOS analyses as supported by the finalized analysis plan.

### Primary loading criterion

A negative binding energy indicates energetically favorable association
under the defined computational model.

---

## 9. Phase II — pH-Responsive Release

### Scientific question

Does changing the protonation state of the functionalized GQD and relevant
drug sites alter drug-carrier binding sufficiently to support a
pH-responsive release mechanism?

### Principal GQD states

Protonated:

    -COOH

Deprotonated:

    -COO-

Charge assignments must be explicitly tracked for every protonation state.

### Core workflow

protonation-state construction
→ DFT optimization
→ frequency calculations
→ state-specific binding/free-energy comparison
→ potential-energy-surface analysis
→ release-mechanism interpretation

### Primary endpoints

- protonation-state energetics,
- state-specific binding energetics,
- Gibbs free-energy comparisons,
- ΔΔG between relevant pH-state models,
- relaxed dissociation scans,
- release barriers where supported,
- pH-dependent energetic interpretation.

### Working release criterion

Current execution-plan target:

    ΔΔG > 5 kcal/mol

This value is treated as a study criterion and must be interpreted within
the assumptions of the computational protonation-state model.

---

## 10. Phase III — Biological Target Validation

### Scientific question

After release from the GQD model, does the drug retain target-binding
behavior consistent with biological activity?

### Methods

Molecular docking:

    AutoDock Vina

Molecular dynamics:

    GROMACS

Binding free-energy analysis:

    MM/PBSA and/or MM/GBSA as defined by the final validated workflow

### Docking endpoints

- validated receptor preparation,
- native-ligand re-docking,
- docking score,
- binding pose,
- residue interactions,
- comparison of free vs released drug structures.

### Docking validation criterion

Working criterion:

    native-ligand re-docking RMSD < 2.0 Å

### Molecular dynamics endpoints

- RMSD,
- RMSF,
- hydrogen-bond persistence,
- contact behavior,
- structural stability,
- binding free-energy estimates,
- replica agreement and uncertainty where applicable.

### Working retained-efficacy comparison

Current execution-plan criterion:

    |ΔΔG_bind| < 2 kcal/mol

for comparison of free-drug and released-drug target binding.

This threshold is a working interpretation criterion rather than proof of
clinical efficacy.

---

## 11. Phase Integration

The dissertation integrates evidence across three scales:

    GQD-drug interaction
            ↓
    pH-responsive release
            ↓
    drug-protein target interaction

The final interpretation must distinguish clearly between:

- computational evidence,
- mechanistic hypotheses,
- predictions,
- experimentally validated conclusions from the literature.

The computational model does not independently establish therapeutic
efficacy, clinical safety, or in vivo delivery performance.

---

## 12. Scope-Control Rule

This document is the scientific source of truth for the computational
dissertation.

A change involving any of the following is a scope change:

- GQD model,
- functionalization,
- drug set,
- protein targets,
- level of theory,
- solvent model,
- primary scientific endpoint,
- validation criterion,
- major computational phase.

For a scope change:

1. record the rationale in `LAB_JOURNAL.md`;
2. modify this document;
3. review the Git diff;
4. commit with a descriptive scientific commit message;
5. preserve prior computational runs rather than rewriting their history.

---

## Current Scope Status

GQD model:                 DEFINED
COOH connectivity:         VALIDATED
PM6 COOH-GQD structure:    ACCEPTED
Primary DFT protocol:      DEFINED
Solvent model:             DEFINED
Phase I endpoints:         DEFINED
Phase II endpoints:        DEFINED
Phase III endpoints:       DEFINED
Protein targets:           DEFINED
Final drug set:            PENDING SCOPE LOCK


