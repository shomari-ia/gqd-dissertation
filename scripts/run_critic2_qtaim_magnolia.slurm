#!/bin/bash
#SBATCH --partition=defq
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=02:00:00
#SBATCH --output=slurm-%x-%j.out

set -euo pipefail

cd "${SLURM_SUBMIT_DIR:?Submit from repository root}"

: "${ANALYSIS_ID:?Export ANALYSIS_ID}"
: "${CRITIC2_INPUT:?Export CRITIC2_INPUT}"

CRITIC2_PREFIX="$HOME/.local/opt/critic2/critic2-linux-x86_64"
CRITIC2_BIN="$CRITIC2_PREFIX/usr/bin/critic2"
CRITIC2_SHARE="$CRITIC2_PREFIX/usr/share/critic2"

if [[ ! -x "$CRITIC2_BIN" ]]; then
    echo "ERROR: Critic2 executable unavailable: $CRITIC2_BIN" >&2
    exit 2
fi

if [[ ! -f "$CRITIC2_INPUT" ]]; then
    echo "ERROR: missing Critic2 input: $CRITIC2_INPUT" >&2
    exit 3
fi

export CRITIC_HOME="$CRITIC2_SHARE"
export OMP_NUM_THREADS="${SLURM_CPUS_PER_TASK:-8}"

OUTDIR="calculations/phase1_dft/descriptors/critic2/qtaim/outputs"
PROVDIR="calculations/phase1_dft/descriptors/critic2/qtaim/prov"

mkdir -p "$OUTDIR" "$PROVDIR"

OUT="$OUTDIR/${ANALYSIS_ID}.cro"
ERR="$OUTDIR/${ANALYSIS_ID}.stderr.txt"
PROV="$PROVDIR/${ANALYSIS_ID}.prov"

if [[ -e "$OUT" || -e "$ERR" || -e "$PROV" ]]; then
    echo "ERROR: refusing to overwrite immutable QTAIM artifact" >&2
    exit 4
fi

if ! git diff --quiet || ! git diff --cached --quiet; then
    GIT_DIRTY=true
else
    GIT_DIRTY=false
fi

GIT_COMMIT="$(git rev-parse HEAD)"
INPUT_SHA="$(sha256sum "$CRITIC2_INPUT" | awk '{print $1}')"
BINARY_SHA="$(sha256sum "$CRITIC2_BIN" | awk '{print $1}')"

set +e
"$CRITIC2_BIN" < "$CRITIC2_INPUT" > "$OUT" 2> "$ERR"
RC=$?
set -e

if [[ "$RC" -eq 0 ]] && ! grep -qi 'ended successfully' "$OUT"; then
    RC=7
fi

OUT_SHA="NA"
ERR_SHA="NA"
[[ -f "$OUT" ]] && OUT_SHA="$(sha256sum "$OUT" | awk '{print $1}')"
[[ -f "$ERR" ]] && ERR_SHA="$(sha256sum "$ERR" | awk '{print $1}')"

{
    echo "analysis_id=$ANALYSIS_ID"
    echo "slurm_job_id=${SLURM_JOB_ID:-NA}"
    echo "execution_host=$(hostname)"
    echo "git_commit=$GIT_COMMIT"
    echo "git_dirty=$GIT_DIRTY"
    echo "critic2_binary=$CRITIC2_BIN"
    echo "critic2_binary_sha256=$BINARY_SHA"
    echo "input_file=$CRITIC2_INPUT"
    echo "input_sha256=$INPUT_SHA"
    echo "omp_threads=$OMP_NUM_THREADS"
    echo "return_code=$RC"
    echo "output_file=$OUT"
    echo "output_sha256=$OUT_SHA"
    echo "stderr_file=$ERR"
    echo "stderr_sha256=$ERR_SHA"
} > "$PROV"

exit "$RC"
