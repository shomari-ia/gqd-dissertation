#!/bin/bash
#SBATCH --partition=defq
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=04:00:00
#SBATCH --output=slurm-%x-%j.out

set -euo pipefail

cd "${SLURM_SUBMIT_DIR:?Submit from repository root}"

: "${ANALYSIS_ID:?Export ANALYSIS_ID}"
: "${CRITIC2_INPUT:?Export CRITIC2_INPUT}"
: "${NCI_ROOT:?Export NCI_ROOT}"

CRITIC2_PREFIX="$HOME/.local/opt/critic2/critic2-linux-x86_64"
CRITIC2_BIN="$CRITIC2_PREFIX/usr/bin/critic2"
CRITIC2_SHARE="$CRITIC2_PREFIX/usr/share/critic2"

if [[ ! -x "$CRITIC2_BIN" ]]; then
    echo "ERROR: Critic2 executable unavailable" >&2
    exit 2
fi

if [[ ! -f "$CRITIC2_INPUT" ]]; then
    echo "ERROR: Critic2 input unavailable: $CRITIC2_INPUT" >&2
    exit 3
fi

export CRITIC_HOME="$CRITIC2_SHARE"
export OMP_NUM_THREADS="${SLURM_CPUS_PER_TASK:-8}"

OUTDIR="calculations/phase1_dft/descriptors/critic2/nci/outputs"
PROVDIR="calculations/phase1_dft/descriptors/critic2/nci/prov"
RESULTDIR="calculations/phase1_dft/descriptors/critic2/nci/results/${ANALYSIS_ID}"

mkdir -p "$OUTDIR" "$PROVDIR" "$RESULTDIR"

CRO="$OUTDIR/${ANALYSIS_ID}.cro"
ERR="$OUTDIR/${ANALYSIS_ID}.stderr.txt"
PROV="$PROVDIR/${ANALYSIS_ID}.prov"

if [[ -e "$CRO" || -e "$ERR" || -e "$PROV" ]]; then
    echo "ERROR: refusing to overwrite immutable NCI analysis artifact" >&2
    exit 4
fi

EXPECTED=(
  "${NCI_ROOT}.dat"
  "${NCI_ROOT}-dens.cube"
  "${NCI_ROOT}-grad.cube"
  "${NCI_ROOT}-pdens.cube"
  "${NCI_ROOT}.vmd"
)

for f in "${EXPECTED[@]}"; do
    if [[ -e "$f" ]]; then
        echo "ERROR: root-level NCI artifact already exists: $f" >&2
        exit 5
    fi
done

if find "$RESULTDIR" -mindepth 1 -maxdepth 1 | grep -q .; then
    echo "ERROR: NCI result directory is not empty: $RESULTDIR" >&2
    exit 6
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
"$CRITIC2_BIN" < "$CRITIC2_INPUT" > "$CRO" 2> "$ERR"
RC=$?
set -e

if [[ "$RC" -ne 0 ]]; then
    echo "ERROR: Critic2 exited with $RC" >&2
fi

if [[ "$RC" -eq 0 ]] && ! grep -qi 'ended successfully' "$CRO"; then
    echo "ERROR: Critic2 success marker absent" >&2
    RC=7
fi

if [[ "$RC" -eq 0 ]]; then
    for f in "${EXPECTED[@]}"; do
        if [[ ! -s "$f" ]]; then
            echo "ERROR: expected NCI artifact missing/empty: $f" >&2
            RC=8
            break
        fi
    done
fi

if [[ "$RC" -eq 0 ]]; then
    for f in "${EXPECTED[@]}"; do
        mv "$f" "$RESULTDIR/"
    done
fi

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
    echo "result_dir=$RESULTDIR"
    if [[ "$RC" -eq 0 ]]; then
        find "$RESULTDIR" -maxdepth 1 -type f -print0 |
          sort -z |
          xargs -0 sha256sum
    fi
} > "$PROV"

exit "$RC"
