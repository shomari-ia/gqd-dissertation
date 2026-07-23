# Naming Conventions

One pattern, used everywhere. If a name does not fit the pattern, the file does
not belong where you are about to put it.

## Files

    <system>_<method>_<task>_v<NN>.<ext>

    cooh_gqd_pm6_opt_v01.com
    cooh_gqd_b3lyp_optfreq_v01.com
    cooh_gqd_b3lyp_optfreq_v01.log
    erlotinib_b3lyp_optfreq_v01.com
    cooh_gqd_erlotinib_flat_b3lyp_optfreq_v01.com
    cooh_gqd_venetoclax_slipped_cp_v01.com

Lowercase, underscores, no spaces, no dates in filenames (the run log has the
date). `v01` increments only when the *input* changes — a restart of an
unchanged input keeps the version and gets a new `run_id`.

## Systems (`system_id`)

Must match a key in `config/systems.yml`:

    cooh_gqd
    erlotinib | gefitinib | venetoclax | abt737
    cooh_gqd_erlotinib          (complex)
    cooh_gqd_erlotinib_flat     (complex, specific pose)

## Runs (`run_id`)

    <STAGE>-<SYSTEM>-<NNN>

    PM6-COOH-GQD-001
    DFT-COOH-GQD-001
    DFT-ERLOTINIB-001
    DFT-COOH-GQD-ERLOTINIB-FLAT-001
    CP-COOH-GQD-ERLOTINIB-001
    SP-COOH-GQD-ERLOTINIB-001

Stages: `PM6`, `DFT`, `CP` (counterpoise), `SP` (M06-2X single point),
`TD` (TDDFT), `WFX` (wavefunction generation).

The number increments per system+stage and **never repeats, never gets
reused**. A failed job keeps its number forever; the retry gets the next one.

## Checkpoints

`%chk` always points into `archive/chk/` and always carries the full file
stem, so PM6 and DFT checkpoints for the same molecule can never collide:

    %oldchk=archive/chk/cooh_gqd_pm6_opt_v01.chk
    %chk=archive/chk/cooh_gqd_b3lyp_optfreq_v01.chk

Reusing one `.chk` name across stages overwrites the PM6 record and destroys
the geometry hand-off you depend on. This is the single most common way this
kind of pipeline loses its provenance.
