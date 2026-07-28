#!/bin/bash
# verify_gaussian.sh — quality-control gate for a single Gaussian 16 log.
#
# Usage:  scripts/verify_gaussian.sh <path/to/job.log> [summary_dir]
#
# Writes a small text summary (committable) and prints one TSV line:
#   run_id  status  imag_freq  final_scf_hartree  gibbs_hartree  log_sha256
#
# Exit codes: 0 = PASS, 1 = usage/file error, 2 = abnormal termination,
#             3 = optimization not completed, 4 = imaginary frequency present.
#
# The exit code is the gate. A result does not advance to the next stage
# unless this script exits 0.

set -euo pipefail

if [[ $# -lt 1 ]]; then
    echo "Usage: $0 <gaussian.log> [summary_dir]" >&2
    exit 1
fi

LOG="$1"
SUMDIR="${2:-}"

[[ -f "$LOG" ]] || { echo "ERROR: not found: $LOG" >&2; exit 1; }

RUN_ID=$(basename "$LOG" .log)
STATUS="PASS"
CODE=0

# --- termination -------------------------------------------------------
if grep -q "Normal termination" "$LOG"; then
    TERM="NORMAL"
else
    TERM="ABNORMAL"
    STATUS="FAILED"
    CODE=2
fi

ERRLINE=$(grep -m1 -E "Error termination|Convergence failure|galloc|Erroneous write" "$LOG" || true)

# --- optimization ------------------------------------------------------
ROUTE=$(grep -m1 "^ #" "$LOG" | sed 's/^ *//' || true)
if grep -qi "opt" <<<"$ROUTE"; then
    if grep -q "Optimization completed" "$LOG"; then
        OPT="COMPLETED"
    else
        OPT="NOT_COMPLETED"
        STATUS="FAILED"
        [[ $CODE -eq 0 ]] && CODE=3
    fi
else
    OPT="NA"
fi

# --- imaginary frequencies --------------------------------------------
# Gaussian prints harmonic frequencies on "Frequencies --" lines (3 per line).
# Any negative value is an imaginary mode.
if grep -q "Frequencies --" "$LOG"; then
    IMAG=$(grep "Frequencies --" "$LOG" \
           | awk '{for(i=3;i<=NF;i++) if($i+0 < 0) n++} END{print n+0}')
    if [[ "$IMAG" -gt 0 ]]; then
        STATUS="FAILED"
        [[ $CODE -eq 0 ]] && CODE=4
    fi
else
    IMAG="NA"
fi

# --- energies ----------------------------------------------------------
SCF=$(grep "SCF Done" "$LOG" | tail -n 1 | awk '{print $5}')
SCF="${SCF:-NA}"

GIBBS=$(grep "Sum of electronic and thermal Free Energies" "$LOG" \
        | tail -n 1 | awk '{print $NF}')
GIBBS="${GIBBS:-NA}"

ZPE=$(grep "Zero-point correction" "$LOG" | tail -n 1 | awk '{print $3}')
ZPE="${ZPE:-NA}"

# BSSE counterpoise, if this was a Counterpoise=2 job
CP=$(grep -m1 "counterpoise corrected energy" "$LOG" | awk '{print $NF}' || true)
CP="${CP:-NA}"

CHARGE_MULT=$(grep -m1 "Charge =" "$LOG" | sed 's/^ *//' || echo "NA")
NATOMS=$(grep -m1 "NAtoms=" "$LOG" | awk '{print $2}' || echo "NA")
CPUTIME=$(grep "Job cpu time" "$LOG" | tail -n 1 | sed 's/^ *//' || echo "NA")
ELAPSED=$(grep "Elapsed time" "$LOG" | tail -n 1 | sed 's/^ *//' || echo "NA")
SHA=$(sha256sum "$LOG" | awk '{print $1}')

# --- summary file ------------------------------------------------------
if [[ -n "$SUMDIR" ]]; then
    mkdir -p "$SUMDIR"
    {
        echo "run_id          $RUN_ID"
        echo "log_file        $LOG"
        echo "log_sha256      $SHA"
        echo "verified_at     $(date --iso-8601=seconds)"
        echo "route           $ROUTE"
        echo "charge_mult     $CHARGE_MULT"
        echo "n_atoms         $NATOMS"
        echo "termination     $TERM"
        echo "optimization    $OPT"
        echo "imag_freq       $IMAG"
        echo "scf_hartree     $SCF"
        echo "zpe_hartree     $ZPE"
        echo "gibbs_hartree   $GIBBS"
        echo "cp_corrected    $CP"
        echo "cpu_time        $CPUTIME"
        echo "elapsed_time    $ELAPSED"
        echo "qc_status       $STATUS"
        [[ -n "$ERRLINE" ]] && echo "error_line      $ERRLINE"
    } > "$SUMDIR/${RUN_ID}.summary.txt"
fi

printf "%s\t%s\t%s\t%s\t%s\t%s\n" \
    "$RUN_ID" "$STATUS" "$IMAG" "$SCF" "$GIBBS" "$SHA"

exit $CODE
