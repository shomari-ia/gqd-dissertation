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

if [[ ! -f "$CRITIC2_INPUT" ]]; then
    echo "ERROR: missing Critic2 input: $CRITIC2_INPUT" >&2
    exit 2
fi

CRITIC2_PREFIX="$HOME/.local/opt/critic2/critic2-linux-x86_64"
CRITIC2_BIN="$CRITIC2_PREFIX/usr/bin/critic2"
CRITIC2_SHARE="$CRITIC2_PREFIX/usr/share/critic2"

if [[ ! -x "$CRITIC2_BIN" ]]; then
    echo "ERROR: Critic2 executable unavailable: $CRITIC2_BIN" >&2
    exit 3
fi

if [[ ! -d "$CRITIC2_SHARE/atomdens" ]]; then
    echo "ERROR: Critic2 atomic-density resources unavailable:" >&2
    echo "       $CRITIC2_SHARE/atomdens" >&2
    exit 4
fi

# Portable critic2 tarball resource location.
# Do not use the source-tree -r .../dat convention here.
export CRITIC_HOME="$CRITIC2_SHARE"

export OMP_NUM_THREADS="${SLURM_CPUS_PER_TASK:-8}"

OUTDIR="calculations/phase1_dft/descriptors/critic2/outputs"
PROVDIR="calculations/phase1_dft/descriptors/critic2/prov"

mkdir -p "$OUTDIR" "$PROVDIR"

OUTPUT="$OUTDIR/${ANALYSIS_ID}.cro"
PROV="$PROVDIR/${ANALYSIS_ID}.prov"

if [[ -e "$OUTPUT" || -e "$PROV" ]]; then
    echo "ERROR: refusing to overwrite immutable analysis artifact" >&2
    exit 5
fi

# Refuse to overwrite structured result files requested by the input.
mapfile -t JSON_OUTPUTS < <(
    awk '
    BEGIN {IGNORECASE=1}
    /HIRSHFELD/ {
        for (i=1; i<=NF; i++) {
            if (toupper($i)=="JSON" && i<NF) {
                print $(i+1)
            }
        }
    }' "$CRITIC2_INPUT"
)

for result in "${JSON_OUTPUTS[@]:-}"; do
    [[ -z "$result" ]] && continue

    if [[ -e "$result" ]]; then
        echo "ERROR: refusing to overwrite result: $result" >&2
        exit 6
    fi

    mkdir -p "$(dirname "$result")"
done

GIT_COMMIT="$(git rev-parse HEAD)"

if [[ -n "$(git status --porcelain)" ]]; then
    GIT_DIRTY=true
else
    GIT_DIRTY=false
fi

INPUT_SHA="$(
    sha256sum "$CRITIC2_INPUT" |
    awk '{print $1}'
)"

BINARY_SHA="$(
    sha256sum "$CRITIC2_BIN" |
    awk '{print $1}'
)"

SOURCE_FCHK="$(
    grep -oE \
      'archive/wfn/[^[:space:]]+\.fchk' \
      "$CRITIC2_INPUT" |
    head -n 1 ||
    true
)"

SOURCE_FCHK_SHA="NA"

if [[ -n "$SOURCE_FCHK" && -f "$SOURCE_FCHK" ]]; then
    SOURCE_FCHK_SHA="$(
        sha256sum "$SOURCE_FCHK" |
        awk '{print $1}'
    )"
fi

set +e

"$CRITIC2_BIN" \
  "$CRITIC2_INPUT" \
  "$OUTPUT"

RC=$?

set -e

OUTPUT_SHA="NA"

if [[ -f "$OUTPUT" ]]; then
    OUTPUT_SHA="$(
        sha256sum "$OUTPUT" |
        awk '{print $1}'
    )"
fi

{
    echo "analysis_id=$ANALYSIS_ID"
    echo "slurm_job_id=${SLURM_JOB_ID:-NA}"
    echo "execution_host=$(hostname)"

    echo "critic2_binary=$CRITIC2_BIN"
    echo "critic2_binary_sha256=$BINARY_SHA"
    echo "critic_home=$CRITIC_HOME"

    echo "omp_threads=$OMP_NUM_THREADS"

    echo "input_file=$CRITIC2_INPUT"
    echo "input_sha256=$INPUT_SHA"

    echo "source_fchk=$SOURCE_FCHK"
    echo "source_fchk_sha256=$SOURCE_FCHK_SHA"

    echo "git_commit=$GIT_COMMIT"
    echo "git_dirty=$GIT_DIRTY"

    echo "return_code=$RC"

    echo "output_file=$OUTPUT"
    echo "output_sha256=$OUTPUT_SHA"

} > "$PROV"

if [[ "$RC" -ne 0 ]]; then
    echo "ERROR: Critic2 exited with $RC" >&2
    exit "$RC"
fi

if ! grep -qi \
    'ended successfully' \
    "$OUTPUT"
then
    echo "ERROR: Critic2 success marker absent" >&2
    exit 7
fi

echo "PASS: $ANALYSIS_ID"
echo "Output: $OUTPUT"
echo "Provenance: $PROV"
