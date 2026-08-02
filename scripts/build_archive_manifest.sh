#!/bin/bash
# build_archive_manifest.sh — deterministically inventory large scientific
# files stored under archive/ but excluded from Git.
#
# Usage:
#   scripts/build_archive_manifest.sh
#   scripts/build_archive_manifest.sh --write
#   scripts/build_archive_manifest.sh --verify
#
# --write  writes archive_manifest.tsv
# --verify checks every recorded file against its stored SHA-256 checksum.

set -euo pipefail
cd "$(dirname "$0")/.."

OUT="archive_manifest.tsv"

emit() {
    printf "file_path\tfile_type\tsize_bytes\tsha256\trun_id\n"

    find archive -type f \
        ! -name '.gitkeep' \
        ! -name 'README.md' \
        -print0 |
    sort -z |
    while IFS= read -r -d '' file; do
        case "$file" in
            *.chk) file_type="gaussian_checkpoint" ;;
            *.log) file_type="gaussian_log" ;;
            *.wfx) file_type="wavefunction" ;;
            *.cube|*.cub) file_type="cube" ;;
            *) file_type="other" ;;
        esac

        size=$(stat -c '%s' "$file")
        sha=$(sha256sum "$file" | awk '{print $1}')

        run_number=$(basename "$file" |
            sed -n 's/.*\.run\([0-9][0-9][0-9]\)\..*/\1/p')

        if [[ -n "$run_number" ]]; then
            run_id="PM6-COOH-GQD-${run_number}"
        else
            run_id="UNASSIGNED"
        fi

        printf "%s\t%s\t%s\t%s\t%s\n" \
            "$file" "$file_type" "$size" "$sha" "$run_id"
    done
}

verify() {
    if [[ ! -f "$OUT" ]]; then
        echo "ERROR: $OUT does not exist. Run with --write first." >&2
        exit 1
    fi

    failures=0

    while IFS=$'\t' read -r file file_type size expected_sha run_id; do
        [[ "$file" == "file_path" ]] && continue

        if [[ ! -f "$file" ]]; then
            echo "MISSING: $file"
            failures=$((failures + 1))
            continue
        fi

        actual_size=$(stat -c '%s' "$file")
        actual_sha=$(sha256sum "$file" | awk '{print $1}')

        if [[ "$actual_size" != "$size" ]]; then
            echo "SIZE_MISMATCH: $file"
            failures=$((failures + 1))
        elif [[ "$actual_sha" != "$expected_sha" ]]; then
            echo "CHECKSUM_MISMATCH: $file"
            failures=$((failures + 1))
        else
            echo "PASS: $file"
        fi
    done < "$OUT"

    if [[ "$failures" -gt 0 ]]; then
        echo "Archive verification failed: $failures problem(s)." >&2
        exit 1
    fi

    echo "Archive verification passed."
}

case "${1:-}" in
    --write)
        emit > "${OUT}.tmp"
        mv "${OUT}.tmp" "$OUT"
        echo "wrote $OUT ($(($(wc -l < "$OUT") - 1)) files)" >&2
        ;;
    --verify)
        verify
        ;;
    "")
        emit
        ;;
    *)
        echo "Usage: $0 [--write|--verify]" >&2
        exit 1
        ;;
esac



