#!/bin/bash
# build_run_log.sh — regenerate run_log.tsv from the provenance files that
# each job wrote about itself, joined to your hand-written run_notes.tsv.
#
#   Usage:  scripts/build_run_log.sh  [> run_log.tsv]
#           scripts/build_run_log.sh --write     (writes run_log.tsv in place)
#
# WHY THIS EXISTS
# You never hand-type run_log.tsv. Machine facts (job id, node, energies,
# checksums, commit) come from the job itself and cannot drift. Human facts
# (why you ran it, what you decided) live in run_notes.tsv, which you edit
# freely — this script never touches it.
#
# Rebuilding is safe and idempotent: run it as often as you like.

set -euo pipefail
cd "$(dirname "$0")/.."

NOTES="run_notes.tsv"
OUT="run_log.tsv"

emit() {
    printf "run_id\tdate\tsystem_id\tstage\tinput_file\tjob_id\tnode\tstatus\timag_freq\tscf_hartree\tgibbs_hartree\tgit_commit\toutput_sha256\tnotes\n"

    find calculations -type f -name '*.prov' | sort | while read -r prov; do
        # provenance is plain key=value; read it without executing anything
        get() { grep -m1 "^$1=" "$prov" | cut -d= -f2- || true; }

        run_id=$(get run_id)
        date=$(get date); date="${date%%T*}"
        input=$(get input_file)
        output=$(get output_file)
        job_id=$(get job_id)
        node=$(get node)
        commit=$(get git_commit)
        osha=$(get output_sha256)

        # stage and system are derived from the path/run_id, not typed twice
        stage=$(echo "$input" | awk -F/ '{print $3}')
        system_id=$(echo "$run_id" | cut -d- -f2- | sed 's/-[0-9]*$//')

        status="MISSING_LOG"; imag="NA"; scf="NA"; gibbs="NA"
        sumfile="$(dirname "$(dirname "$input")")/summaries/$(basename "$output" .log).summary.txt"
        if [[ -f "$sumfile" ]]; then
            status=$(grep -m1 '^qc_status' "$sumfile" | awk '{print $2}')
            imag=$(grep  -m1 '^imag_freq'  "$sumfile" | awk '{print $2}')
            scf=$(grep   -m1 '^scf_hartree' "$sumfile" | awk '{print $2}')
            gibbs=$(grep -m1 '^gibbs_hartree' "$sumfile" | awk '{print $2}')
        fi

        note=""
        if [[ -f "$NOTES" ]]; then
            note=$(awk -F'\t' -v id="$run_id" '$1==id {print $3}' "$NOTES" | head -n1)
        fi
        # a manual status in run_notes.tsv (e.g. SUPERSEDED) wins over the QC status
        if [[ -f "$NOTES" ]]; then
            manual=$(awk -F'\t' -v id="$run_id" '$1==id && $2!="" {print $2}' "$NOTES" | head -n1)
            [[ -n "$manual" ]] && status="$manual"
        fi

        printf "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" \
            "$run_id" "$date" "$system_id" "$stage" "$input" "$job_id" "$node" \
            "$status" "$imag" "$scf" "$gibbs" "$commit" "$osha" "$note"
    done
}

if [[ "${1:-}" == "--write" ]]; then
    emit > "$OUT.tmp" && mv "$OUT.tmp" "$OUT"
    echo "wrote $OUT ($(($(wc -l < "$OUT") - 1)) runs)" >&2
else
    emit
fi
