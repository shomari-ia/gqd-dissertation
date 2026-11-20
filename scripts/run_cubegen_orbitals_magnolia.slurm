#!/bin/bash
#SBATCH --partition=defq
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=8G
#SBATCH --time=01:00:00
#SBATCH --output=slurm-%x-%j.out

set -euo pipefail

cd "${SLURM_SUBMIT_DIR:?Submit from repository root}"

: "${ANALYSIS_ID:?Export ANALYSIS_ID}"
: "${FCHK:?Export FCHK}"
: "${SYSTEM_TAG:?Export SYSTEM_TAG}"

if [[ ! -f "$FCHK" ]]; then
    echo "ERROR: formatted checkpoint not found: $FCHK" >&2
    exit 2
fi

OUTDIR="calculations/phase1_dft/descriptors/orbitals/results/${ANALYSIS_ID}"
PROVDIR="calculations/phase1_dft/descriptors/orbitals/prov"
mkdir -p "$OUTDIR" "$PROVDIR"

HOMO="$OUTDIR/${SYSTEM_TAG}_homo.cube"
LUMO="$OUTDIR/${SYSTEM_TAG}_lumo.cube"
PROV="$PROVDIR/${ANALYSIS_ID}.prov"

if [[ -e "$HOMO" || -e "$LUMO" || -e "$PROV" ]]; then
    echo "ERROR: refusing to overwrite orbital artifact" >&2
    exit 3
fi

export g16root="/usr/local/apps/gaussian/g16-c02-avx2"
GAUSSIAN_BUILD="g16-c02-avx2"

set +e
set +u
. "$g16root/g16/bsd/g16.profile"
PROFILE_RC=$?
set -u
set -e

if ! command -v cubegen >/dev/null 2>&1; then
    echo "ERROR: cubegen unavailable after Gaussian environment load" >&2
    exit 4
fi

SCRATCH_ROOT="/local"
if [[ ! -d "$SCRATCH_ROOT" || ! -w "$SCRATCH_ROOT" ]]; then
    echo "ERROR: /local scratch unavailable" >&2
    exit 5
fi

SCRDIR="$SCRATCH_ROOT/${USER}.${SLURM_JOB_ID}.cubegen"
if [[ -e "$SCRDIR" ]]; then
    echo "ERROR: refusing scratch reuse: $SCRDIR" >&2
    exit 6
fi
mkdir -m 700 "$SCRDIR"
export GAUSS_SCRDIR="$SCRDIR"
trap 'rm -rf "$SCRDIR"' EXIT

if ! git diff --quiet || ! git diff --cached --quiet; then
    GIT_DIRTY=true
else
    GIT_DIRTY=false
fi

GIT_COMMIT="$(git rev-parse HEAD)"
FCHK_SHA="$(sha256sum "$FCHK" | awk '{print $1}')"
CUBEGEN_PATH="$(command -v cubegen)"

set +e
cubegen 0 MO=HOMO "$FCHK" "$HOMO" 0 h
RC_HOMO=$?
cubegen 0 MO=LUMO "$FCHK" "$LUMO" 0 h
RC_LUMO=$?
set -e

if [[ "$RC_HOMO" -ne 0 || "$RC_LUMO" -ne 0 ]]; then
    echo "ERROR: cubegen failure HOMO=$RC_HOMO LUMO=$RC_LUMO" >&2
    RC=7
elif [[ ! -s "$HOMO" || ! -s "$LUMO" ]]; then
    echo "ERROR: HOMO/LUMO cube missing or empty" >&2
    RC=8
else
    RC=0
fi

{
    echo "analysis_id=$ANALYSIS_ID"
    echo "slurm_job_id=${SLURM_JOB_ID:-NA}"
    echo "execution_host=$(hostname)"
    echo "git_commit=$GIT_COMMIT"
    echo "git_dirty=$GIT_DIRTY"
    echo "gaussian_build=$GAUSSIAN_BUILD"
    echo "gaussian_profile_rc=$PROFILE_RC"
    echo "cubegen_path=$CUBEGEN_PATH"
    echo "source_fchk=$FCHK"
    echo "source_fchk_sha256=$FCHK_SHA"
    echo "system_tag=$SYSTEM_TAG"
    echo "homo_cube=$HOMO"
    echo "lumo_cube=$LUMO"
    echo "cubegen_homo_rc=$RC_HOMO"
    echo "cubegen_lumo_rc=$RC_LUMO"
    echo "return_code=$RC"
    if [[ -s "$HOMO" ]]; then
        echo "homo_sha256=$(sha256sum "$HOMO" | awk '{print $1}')"
    fi
    if [[ -s "$LUMO" ]]; then
        echo "lumo_sha256=$(sha256sum "$LUMO" | awk '{print $1}')"
    fi
} > "$PROV"

exit "$RC"
