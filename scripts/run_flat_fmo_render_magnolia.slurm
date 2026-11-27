#!/bin/bash
#SBATCH --job-name=viz_erl_flat
#SBATCH --partition=defq
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=8G
#SBATCH --time=00:30:00
#SBATCH --output=slurm-%x-%j.out
set -euo pipefail
cd "${SLURM_SUBMIT_DIR:?}"
source "$HOME/.venvs/gqd-viz/bin/activate"
export MPLBACKEND=Agg
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
OUT="calculations/phase1_dft/descriptors/orbitals/visualizations/VIS-ERL-FLAT-FMO-PILOT-001"
python3 scripts/render_flat_fmo_pilot.py --outdir "$OUT"
