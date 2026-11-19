# Milestone 03 — Scientific Graphics Library

**Workspace:** GQD Creative + Presentation Studio  
**Edition:** Scientific Graphics Set 01 · Draft for visual review  
**Visual identity:** Shomari IA · Gray Scientific Futurism  
**Boundaries:** Design assets only. Canonical research records are not modified.

## Objective

Create a repeatable, recognizable visual language for computational science that connects GitHub, the dissertation presentation, research journal, posters, AXIOM, and QR-linked exhibits — without diluting scientific rigor.

## Architecture

| Collection | Deliverables | First release |
|---|---|---|
| 01. Method icons | Quantum modeling, adsorption, pH, docking, MD | **5 SVGs created** |
| 02. Evidence icons | Scientific acceptance, provenance, archive integrity | **3 SVGs created** |
| 03. Research diagrams | Multiscale phase architecture, acceptance pipeline | **2 SVGs created** |
| 04. Molecular figures | Carrier, drug, and complexes from accepted coordinates | **Not created; requires scientific source validation** |
| 05. Presentation motifs | Title divider, chapter ribbon, figure labels | **Queued** |
| 06. Publication components | Poster modules, print-safe variants, evidence plates | **Queued** |
| 07. QR-linked display panels | Branded QR frames with tested URLs and alt text | **Queued** |
| 08. AXIOM overlays | Headshot, explanatory pose, functional chest display | **Queued; separate mascot design work** |

## Set 01 — scientific process icons

1. DFT modeling — `assets/graphics/icons/dft-orbitals.svg`
2. Drug adsorption — `assets/graphics/icons/adsorption.svg`
3. pH-responsive modeling — `assets/graphics/icons/ph-protonation.svg`
4. Molecular docking — `assets/graphics/icons/molecular-docking.svg`
5. Molecular dynamics — `assets/graphics/icons/molecular-dynamics.svg`
6. Scientific acceptance gate — `assets/graphics/icons/scientific-acceptance.svg`
7. Provenance / traceability — `assets/graphics/icons/provenance.svg`
8. Archive integrity — `assets/graphics/icons/archive-integrity.svg`

## Set 01 — diagrams

- `assets/graphics/diagrams/multiscale-methods.svg`: three-phase conceptual research map. Phase II / III are planned, not claimed complete.
- `assets/graphics/diagrams/evidence-gates.svg`: grouped sequence G0–G3, G4–G5, G6–G9 and disposition; see the actual Acceptance Gates v2.0 for the governing definitions.

## Visual grammar

**Palette:** dark neutral graphite, brushed gray/silver, white text and a restrained warm gold accent. No default cyan/blue.  
**Forms:** smooth lines, restrained scientific curves, signal traces, negative space, precise spacing and typographic hierarchy. The revised molecular-docking icon shows a connected ligand nested in a stylized receptor pocket rather than an ambiguous free-floating shape.

**Typography:** Georgia for authored titles and narrative/body text in presentation decks, posters, journal and digital exhibits; mathematical notation, code, and dense numeric labels may use appropriate specialist fonts. GitHub-rendered Markdown typography is controlled by GitHub and cannot be globally changed through README content.  
**Sizing:** icons are 128×128 vector; diagrams use widescreen or banner format and should be legible when scaled.  
**Accessibility:** SVG title/description, high contrast, textual labels for dispositions, never color-only PASS/FAIL semantics.  
**Naming:** descriptive `kebab-case` paths; filenames identify concepts, not unsupported findings.

## Scientific control policy

- **Project logo/identity does not represent a validated molecular structure.**
- True GQD geometry figures, complex adsorption poses, molecular orbitals, energy results, and trajectories must derive from accepted source files and reproducible analysis.
- Scientific acceptance and supersession are maintained only in the canonical evidence/status system. A decorative checkmark is not a substitute for the applicable gate evidence.
- The `GQD` repo is the authoritative scientific record. Shomari IA profile and AXIOM remain visual/presentation identities.
- Existing calculations, scripts, run ledgers, scientific status, and acceptance gates are outside this creative change.

## Quality and promotion gate for graphic assets

- [x] Contains only conceptual diagrams/icons
- [x] Shared grayscale design language
- [x] Descriptive SVG title and alt-text guidance
- [x] No validation claims embedded in graphics
- [ ] Visual approval across GitHub light/dark themes
- [ ] PowerPoint import test
- [ ] Print contrast test
- [ ] Final branding review

## Production order after Set 01

1. Reusable title / section / methodology slide templates.
2. Scientific-status chips with text and evidence identifier (never color alone).
3. Source-backed molecular illustrations from approved Gaussian structures.
4. Poster format components (16:9; A0/A1 options).
5. QR panels, with functional destination verification and offline fallbacks.
