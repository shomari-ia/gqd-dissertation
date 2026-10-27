#!/bin/bash
#SBATCH --job-name=g16_magnolia
#SBATCH --partition=defq
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=16
#SBATCH --mem=64G
#SBATCH --time=48:00:00
#SBATCH --output=slurm-%x-%j.out
#
# run_gaussian_magnolia.slurm — unified Gaussian 16 submission script for Magnolia.
#
# Submit from the repository root with a unique RUN_ID and current input path:
#
# sbatch -J <job_name> \
#   --export=ALL,RUN_ID=<unique_run_id>,INPUT=<path/to/current_input.com> \
#   scripts/run_gaussian_magnolia.slurm
#
# If resources are overridden at submission, keep the Slurm allocation
# consistent with the Gaussian %nprocshared and %mem directives.

set -euo pipefail

cd "${SLURM_SUBMIT_DIR:?Submit the job with sbatch from the repository root.}"
REPO_DIR="$PWD"
RUNTIME_GIT_COMMIT="$(git rev-parse HEAD 2>/dev/null || echo NA)"
if [[ -n "$(git status --porcelain 2>/dev/null)" ]]; then RUNTIME_GIT_DIRTY=true; else RUNTIME_GIT_DIRTY=false; fi

: "${INPUT:?Export INPUT=path/to/input.com with sbatch}"
: "${RUN_ID:?Export RUN_ID=STAGE-SYSTEM-NNN with sbatch}"

if [[ ! -f "$INPUT" ]]; then
    echo "ERROR: Gaussian input file not found: $INPUT" >&2
    exit 2
fi

STAGE_DIR="$(dirname "$(dirname "$INPUT")")"
BASE="$(basename "$INPUT")"
BASE="${BASE%.com}"
BASE="${BASE%.gjf}"

OUTPUT="archive/logs/${BASE}.log"
PROV="${STAGE_DIR}/prov/${RUN_ID}.prov"
CHK="$(grep -i -m1 '^%chk=' "$INPUT" | cut -d= -f2- || true)"
OLDCHK="$(grep -i -m1 '^%oldchk=' "$INPUT" | cut -d= -f2- || true)"
INPUT_NPROC="$(grep -i -m1 '^%nprocshared=' "$INPUT" | cut -d= -f2- | tr -d '[:space:]' || true)"
INPUT_MEM="$(grep -i -m1 '^%mem=' "$INPUT" | cut -d= -f2- | tr -d '[:space:]' || true)"
SUMMARY="${STAGE_DIR}/summaries/${BASE}.summary.txt"

mkdir -p \
    archive/logs \
    archive/chk \
    "${STAGE_DIR}/prov" \
    "${STAGE_DIR}/summaries"

# --------------------------------------------------------- immutable-evidence gate

if [[ -e "$OUTPUT" ]]; then
    echo "ERROR: Refusing to overwrite existing output: $OUTPUT" >&2
    exit 5
fi

if [[ -e "$PROV" ]]; then
    echo "ERROR: Refusing to overwrite existing provenance: $PROV" >&2
    exit 6
fi

if [[ -e "$SUMMARY" ]]; then
    echo "ERROR: Refusing to overwrite existing summary: $SUMMARY" >&2
    exit 8
fi

if [[ -n "$OLDCHK" && ! -f "$OLDCHK" ]]; then
    echo "ERROR: Required Gaussian %oldchk file not found: $OLDCHK" >&2
    exit 11
fi

if [[ -n "$CHK" && -e "$CHK" ]]; then
    echo "ERROR: Refusing to overwrite existing checkpoint: $CHK" >&2
    exit 7
fi

if [[ -n "$INPUT_NPROC" && ! "$INPUT_NPROC" =~ ^[0-9]+$ ]]; then
    echo "ERROR: Invalid Gaussian %nprocshared value: $INPUT_NPROC" >&2
    exit 9
fi

if [[ -n "$INPUT_NPROC" && -n "${SLURM_CPUS_PER_TASK:-}" && "$INPUT_NPROC" -gt "$SLURM_CPUS_PER_TASK" ]]; then
    echo "ERROR: Gaussian requests $INPUT_NPROC CPUs but Slurm allocated only $SLURM_CPUS_PER_TASK." >&2
    exit 10
fi

# --------------------------------------------------------- Gaussian scratch

SCRDIR="/tmp/${USER}.${SLURM_JOB_ID}"
mkdir -p "$SCRDIR"
export GAUSS_SCRDIR="$SCRDIR"
export OMP_NUM_THREADS=1

cleanup() {
    rm -rf "$SCRDIR"
}
trap cleanup EXIT

ulimit -s unlimited

# --------------------------------------------------------- Magnolia Gaussian build

EXEC_HOST="$(hostname)"
echo "Execution host: $EXEC_HOST"

export g16root="/usr/local/apps/gaussian/g16-c02-avx2"
GAUSSIAN_BUILD="g16-c02-avx2"

# Gaussian's legacy profile references optional variables and may return a
# nonzero status during normal environment setup. Temporarily disable both
# nounset and errexit while sourcing it, then restore strict Bash mode.
set +e
set +u
# shellcheck disable=SC1091
. "$g16root/g16/bsd/g16.profile"
GAUSSIAN_PROFILE_RC=$?
set -u
set -e

echo "Gaussian profile return code: $GAUSSIAN_PROFILE_RC"

if ! command -v g16 >/dev/null 2>&1; then
    echo "ERROR: g16 was not found after loading $GAUSSIAN_BUILD." >&2
    exit 4
fi

# ------------------------------------------------------------- provenance

{
    echo "run_id=${RUN_ID}"
    echo "date=$(date --iso-8601=seconds)"
    echo "cluster=magnolia"
    echo "scheduler=slurm"
    echo "input_file=${INPUT}"
    echo "output_file=${OUTPUT}"
    echo "checkpoint_file=${CHK:-NA}"
    echo "old_checkpoint_file=${OLDCHK:-NA}"
    if [[ -n "$OLDCHK" && -f "$OLDCHK" ]]; then
        echo "old_checkpoint_sha256=$(sha256sum "$OLDCHK" | awk '{print $1}')"
    else
        echo "old_checkpoint_sha256=NA"
    fi
    echo "gaussian_nprocshared=${INPUT_NPROC:-NA}"
    echo "gaussian_mem=${INPUT_MEM:-NA}"
    echo "job_script=scripts/run_gaussian_magnolia.slurm"
    echo "job_script_sha256=$(sha256sum scripts/run_gaussian_magnolia.slurm | awk '{print $1}')"
    echo "job_id=${SLURM_JOB_ID:-NA}"
    echo "job_name=${SLURM_JOB_NAME:-g16_magnolia}"
    echo "partition=${SLURM_JOB_PARTITION:-defq}"
    echo "execution_host=${EXEC_HOST}"
    echo "node_list=${SLURM_JOB_NODELIST:-NA}"
    echo "nodes=${SLURM_JOB_NUM_NODES:-NA}"
    echo "ntasks=${SLURM_NTASKS:-NA}"
    echo "cpus_per_task=${SLURM_CPUS_PER_TASK:-NA}"
    echo "job_cpus_per_node=${SLURM_JOB_CPUS_PER_NODE:-NA}"
    echo "mem_per_node=${SLURM_MEM_PER_NODE:-NA}"
    echo "gaussian_build=${GAUSSIAN_BUILD}"
    echo "g16root=${g16root}"
    echo "gaussian_path=$(command -v g16)"
    echo "scratch_directory=${GAUSS_SCRDIR}"
    echo "omp_num_threads=${OMP_NUM_THREADS}"
    echo "hostname=$(hostname)"
    echo "repository_directory=${REPO_DIR}"
    echo "runtime_directory=$(pwd)"
    echo "git_commit=${GIT_COMMIT:-NA}"
    echo "git_dirty=${GIT_DIRTY:-UNKNOWN}"
    echo "runtime_git_commit=${RUNTIME_GIT_COMMIT}"
    echo "runtime_git_dirty=${RUNTIME_GIT_DIRTY}"
    echo "input_sha256=$(sha256sum "$INPUT" | awk '{print $1}')"
    echo "start_time=$(date --iso-8601=seconds)"
    } > "$PROV"

# ------------------------------------------------------------------- run

set +e
g16 < "$INPUT" > "$OUTPUT"
GAUSSIAN_EXIT=$?
set -e

echo "gaussian_exit=${GAUSSIAN_EXIT}" >> "$PROV"
echo "end_time=$(date --iso-8601=seconds)" >> "$PROV"

if [[ -f "$OUTPUT" ]]; then
    echo "output_sha256=$(sha256sum "$OUTPUT" | awk '{print $1}')" >> "$PROV"
else
    echo "output_sha256=NA" >> "$PROV"
fi

if [[ -n "$CHK" && -f "$CHK" ]]; then
    echo "checkpoint_sha256=$(sha256sum "$CHK" | awk '{print $1}')" >> "$PROV"
else
    echo "checkpoint_sha256=NA" >> "$PROV"
fi

# --------------------------------------------------------------- QC gate

set +e
scripts/verify_gaussian.sh "$OUTPUT" "${STAGE_DIR}/summaries" "$RUN_ID" "$INPUT"
QC_EXIT=$?
set -e

echo "qc_exit=${QC_EXIT}" >> "$PROV"
if [[ -f "$SUMMARY" ]]; then
    echo "summary_sha256=$(sha256sum "$SUMMARY" | awk '{print $1}')" >> "$PROV"
else
    echo "summary_sha256=NA" >> "$PROV"
fi

# The provenance and QC files are retained even if Gaussian fails.
# Return failure to Slurm when either Gaussian or the QC gate fails.

if (( GAUSSIAN_EXIT != 0 )); then
    exit "$GAUSSIAN_EXIT"
fi

exit "$QC_EXIT"
