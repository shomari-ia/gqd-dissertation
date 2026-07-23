# Build Order

Seven components, in dependency order. Each one is small, each one is finished
before the next begins, and each has a stated "done when" so you are never
guessing whether to move on.

Total setup time if you sit down and do it: about three hours. Components 1–3
are the only ones that block job submission.

---

## Component 1 — Local repository and line endings

**Why first:** everything else lands inside this folder, and the line-ending
rule has to exist *before* the first script is committed. If you commit CRLF
files and fix it later, you fix it twice.

1. Unzip this skeleton to a working folder on your laptop, e.g.
   `C:\research\gqd-dissertation`.
2. Open Notepad++ → Settings → Preferences → New Document → Format: **Unix (LF)**.
   Then Edit → EOL Conversion → Unix (LF) on any file you already have.
3. In Git Bash (or GitHub Desktop's terminal), from inside the folder:

   ```bash
   git init
   git add .
   git commit -m "Initialize repository backbone: structure, QC scripts, run-log system"
   ```

4. Create an **empty, private** repository named `gqd-dissertation` on
   github.com — no README, no .gitignore, no license (you already have them).
5. Connect and push:

   ```bash
   git remote add origin https://github.com/<your-username>/gqd-dissertation.git
   git branch -M main
   git push -u origin main
   ```

Keep it private until the defense; make it public at deposit time (Component 7).

**Done when:** `git status` says clean, and the file tree is visible on github.com.

**Skip:** branches. This is a one-person repository. Committing to `main` with
good messages and tagging milestones gives you the entire benefit of branching
with none of the merge overhead.

---

## Component 2 — The repository on Maple

**Why:** the cluster copy and the laptop copy must be the *same* repository, or
provenance breaks. Git is the transfer mechanism for text; FileZilla is only
for pulling large binaries back.

1. SSH in through the two-hop gateway (hpcwoods → Maple) inside `tmux`.
2. Clone into your work directory:

   ```bash
   git clone https://github.com/<your-username>/gqd-dissertation.git
   cd gqd-dissertation
   chmod +x scripts/*.sh
   ```

3. Set the three site-specific values in `scripts/run_gaussian.pbs` — the
   queue name, the Gaussian module name, and the `g16` launch line. **Get these
   from the MCSR example job, not from memory.** Then:

   ```bash
   git commit -am "Set Maple queue, Gaussian module, and launch command"
   git push
   ```

4. Verify the QC script runs on any old PM6 log you already have:

   ```bash
   scripts/verify_gaussian.sh path/to/some_pm6.log
   ```

**Done when:** `verify_gaussian.sh` prints a TSV line and exits 0 on a job you
know succeeded.

**Working rule from here on:** edit text on the cluster (nano/vim) or on the
laptop, never both at once. `git pull` before you start, `git push` when you
stop. This is what actually kills the CRLF problem — not the setting, the habit.

---

## Component 3 — First tracked job, end to end

**Why:** prove the loop works on one cheap job before you have twenty
expensive ones to reconcile.

1. Copy your real coordinates into
   `calculations/phase1_dft/pm6/inputs/cooh_gqd_pm6_opt_v01.com`
   (the template is there; note that `%chk` points into `archive/chk/`).
2. Commit the input **before** submitting — the run log records the commit
   hash, so the input must exist in history at submission time:

   ```bash
   git add calculations/phase1_dft/pm6/inputs/cooh_gqd_pm6_opt_v01.com
   git commit -m "Add PM6 pre-optimization input for COOH-GQD"
   ```

3. Submit:

   ```bash
   qsub -N cooh_gqd_pm6 \
        -l select=1:ncpus=8:mem=8gb -l walltime=04:00:00 \
        -v RUN_ID=PM6-COOH-GQD-001,INPUT=calculations/phase1_dft/pm6/inputs/cooh_gqd_pm6_opt_v01.com \
        scripts/run_gaussian.pbs
   ```

4. When it finishes, rebuild and commit the log:

   ```bash
   scripts/build_run_log.sh --write
   git add run_log.tsv calculations/phase1_dft/pm6/prov calculations/phase1_dft/pm6/summaries
   git commit -m "Record PM6 optimization of COOH-GQD (PM6-COOH-GQD-001)"
   git push
   ```

**Done when:** `run_log.tsv` has one row you did not type, containing a real
job ID, node name, SCF energy, commit hash, and output checksum.

That row is the unit of the whole system. Every job after this is the same four
commands.

---

## Component 4 — Google Drive archive

**Why:** the `.chk` files are load-bearing in this project (B3LYP reads its
geometry from the PM6 checkpoint), and they are too large for GitHub.

Create this, exactly:

```
GQD-Dissertation/
├── 01_manuscript/        chapters as Google Docs
├── 02_archive/
│   └── phase1_dft/
│       └── <run_id>/     one folder per run: .log, .chk, .fchk, .wfx
├── 03_reports/           the biweekly committee reports
└── 04_figures_source/    editable figure sources
```

Two rules that make Drive safe to rely on:

- **Folder name = `run_id`.** That is the join key back to `run_log.tsv`. No
  other naming scheme, no dates in folder names.
- **Write once.** Never edit or replace a file inside `02_archive/`. A corrected
  calculation is a new `run_id`, therefore a new folder. Drive has no version
  history you would want to defend in a committee meeting.

Transfer with FileZilla (SFTP, port 22, via the gateway host). **Set Transfer →
Transfer type → Binary.** FileZilla's default is Auto, which applies text
conversion by extension and will silently corrupt `.chk` files and reintroduce
CRLF into scripts.

**Done when:** `02_archive/PM6-COOH-GQD-001/` exists and holds the log and
checkpoint from Component 3.

---

## Component 5 — Zotero → `docs/references.bib`

**Why:** the Chapter 2 methods draft cites eleven method references that need
verified volumes and pages. A `.bib` file inside the repository means the
bibliography is version-controlled alongside the methods that cite it.

1. Install the **Better BibTeX** plugin.
2. Collections: `Ch1-Introduction`, `Ch2-PhaseI-DFT`, `Ch3-PhaseII-pH`,
   `Ch4-PhaseIII-Docking-MD`, `Methods-Software`. Put all eleven method
   references (Becke; Lee/Yang/Parr; Grimme ×2; Marenich; Zhao/Truhlar; Boys/
   Bernardi; Lu/Chen; Contreras-García; O'Boyle; Frisch) in `Methods-Software`.
3. Pin citation keys (right-click → Better BibTeX → Pin key) so they never
   change under you.
4. Right-click the library root → Export → Better BibLaTeX → **Keep updated**,
   saving to `docs/references.bib`. It now re-exports automatically on change.
5. Commit `docs/references.bib` whenever it changes.

**Done when:** `docs/references.bib` is in the repo and the count matches your
37/37 target.

---

## Component 6 — Analysis environment (Anaconda + notebooks)

**Why:** only once there are energies to process. Do not build this before
Component 3 produces numbers.

```bash
conda env create -f environments/environment.yml
conda activate gqd
```

`cclib` parses Gaussian logs into Python objects, which is far more reliable
than grep for anything beyond a single energy — orbital energies, frequency
lists, per-atom charges.

Two rules for `notebooks/`:

- Notebooks are for exploration. The moment a notebook produces a number or a
  figure that will appear in the dissertation, that code moves to
  `scripts/analysis/` and the figure is regenerated from the script.
- Clear all outputs before committing (Kernel → Restart & Clear Output).
  Committed notebook outputs create enormous, unreadable diffs.

RStudio is worth keeping only if you would rather build tables and figures in
`ggplot2`; if so, keep it to `scripts/analysis/*.R` and skip the Python
plotting stack. Running both languages for one figure set is a maintenance cost
with no scientific return.

**Done when:** `conda activate gqd` works and `python -c "import cclib"` is silent.

---

## Component 7 — Milestones and deposit (later, but decide now)

Tag the repository at each phase boundary:

```bash
git tag -a v0.1-phase1-structures -m "Structure prep and PM6 pre-optimization complete"
git tag -a v0.2-phase1-individual -m "B3LYP optimization and frequency verification of all five species"
git tag -a v0.3-phase1-complete   -m "Binding energies and electronic-structure analysis complete"
git push origin --tags
```

At submission, connect the GitHub repository to **Zenodo** and publish a
release. Zenodo mints a DOI for that exact commit, and `CITATION.cff` becomes
the citation metadata automatically. The archive folders on Drive move to a
Zenodo dataset deposit or the institutional repository, with `run_log.tsv` as
the index that ties them to the results tables.

**Done when:** each phase boundary carries a tag, and the DOI exists before the
defense.
