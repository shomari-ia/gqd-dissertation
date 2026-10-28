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

    # archive_manifest.tsv is a physical-file inventory. Therefore every
    # scientific file under archive/ is recorded, including byte-identical
    # working copies that coexist with immutable .runNNN copies.
    find archive -type f \
        ! -name '.gitkeep' \
        ! -name 'README.md' \
        -print0 |
        sort -z |
    while IFS= read -r -d '' file; do
        case "$file" in
            *.fchk) file_type="gaussian_formatted_checkpoint" ;;
            *.chk) file_type="gaussian_checkpoint" ;;
            *.log) file_type="gaussian_log" ;;
            *.wfx) file_type="wavefunction" ;;
            *.cube|*.cub) file_type="cube" ;;
            *) file_type="other" ;;
        esac

        size=$(stat -c '%s' "$file")
        sha=$(sha256sum "$file" | awk '{print $1}')
        base=$(basename "$file")
        run_id=""

        # Preserved failed-run directories use the run_id as the directory name.
        if [[ "$file" =~ ^archive/failed_runs/([^/]+)/ ]]; then
            run_id="${BASH_REMATCH[1]}"
        else
            stem="$base"

            case "$stem" in
                *.failed.chk) stem="${stem%.failed.chk}" ;;
                *.failed.log) stem="${stem%.failed.log}" ;;
                *.fchk) stem="${stem%.fchk}" ;;
                *.chk) stem="${stem%.chk}" ;;
                *.log) stem="${stem%.log}" ;;
                *.wfx) stem="${stem%.wfx}" ;;
                *.cube) stem="${stem%.cube}" ;;
                *.cub) stem="${stem%.cub}" ;;
            esac

            # Historical immutable copies carry .runNNN in the filename.
            if [[ "$stem" =~ ^(.*)\.run([0-9]{3})$ ]]; then
                root="${BASH_REMATCH[1]}"
                run_number="${BASH_REMATCH[2]}"

                case "$root" in
                    cooh_gqd_pm6_opt_v01)
                        run_id="PM6-COOH-GQD-${run_number}" ;;
                    cooh_gqd_b3lyp_optfreq_v01)
                        run_id="B3LYP-COOH-GQD-${run_number}" ;;
                    erlotinib_pm6_opt_v01)
                        run_id="PM6-ERLOTINIB-${run_number}" ;;
                    erlotinib_b3lyp_optfreq_v01)
                        run_id="B3LYP-ERLOTINIB-${run_number}" ;;
                    gefitinib_pm6_opt_v01)
                        run_id="PM6-GEFITINIB-${run_number}" ;;
                    gefitinib_b3lyp_optfreq_v01)
                        run_id="B3LYP-GEFITINIB-${run_number}" ;;
                    venetoclax_pm6_opt_v01)
                        run_id="PM6-VENETOCLAX-${run_number}" ;;
                    venetoclax_b3lyp_optfreq_v01)
                        run_id="B3LYP-VENETOCLAX-${run_number}" ;;
                    abt737_pm6_opt_v01)
                        run_id="PM6-ABT737-${run_number}" ;;
                    abt737_b3lyp_optfreq_v01)
                        run_id="B3LYP-ABT737-${run_number}" ;;
                esac
            else
                # Current working copies and corrected COOH-GQD lineages.
                case "$stem" in
                    abt737_pm6_opt_v01)
                        run_id="PM6-ABT737-002" ;;
                    abt737_b3lyp_optfreq_v01)
                        run_id="B3LYP-ABT737-001" ;;
                    cooh_gqd_b3lyp_optfreq_v01)
                        run_id="B3LYP-COOH-GQD-001" ;;
                    erlotinib_pm6_opt_v01)
                        run_id="PM6-ERLOTINIB-001" ;;
                    erlotinib_b3lyp_optfreq_v01)
                        run_id="B3LYP-ERLOTINIB-001" ;;
                    cooh_gqd_c1_erlotinib_flat_b3lyp_optfreq_v01)
                        run_id="B3LYP-COOH-GQD-ERLOTINIB-FLAT-001" ;;
                    cooh_gqd_c1_erlotinib_slipped_b3lyp_optfreq_v01)
                        run_id="B3LYP-COOH-GQD-ERLOTINIB-SLIPPED-001" ;;
                    cooh_gqd_c1_erlotinib_edge_b3lyp_optfreq_v01)
                        run_id="B3LYP-COOH-GQD-ERLOTINIB-EDGE-001" ;;
                    erlotinib_b3lyp_optfreq_magnolia_validation_v01)
                        run_id="B3LYP-ERLOTINIB-MAGNOLIA-VALIDATION-001" ;;
                    erlotinib_pm6_opt_v01_magnolia_seed)
                        run_id="B3LYP-ERLOTINIB-MAGNOLIA-VALIDATION-001" ;;
                    gefitinib_pm6_opt_v01)
                        run_id="PM6-GEFITINIB-001" ;;
                    gefitinib_b3lyp_optfreq_v01)
                        run_id="B3LYP-GEFITINIB-001" ;;
                    venetoclax_pm6_opt_v01)
                        run_id="PM6-VENETOCLAX-001" ;;
                    venetoclax_b3lyp_optfreq_v01)
                        run_id="B3LYP-VENETOCLAX-001" ;;

                    cooh_gqd_class1_c1_pm6_opt_v02)
                        run_id="PM6-COOH-GQD-C1-006" ;;
                    cooh_gqd_class2_c3_pm6_opt_v02)
                        run_id="PM6-COOH-GQD-C2-007" ;;
                    cooh_gqd_class1_c1_pm6_opt_v03)
                        run_id="PM6-COOH-GQD-C1-008" ;;
                    cooh_gqd_class2_c3_pm6_opt_v03)
                        run_id="PM6-COOH-GQD-C2-009" ;;

                    cooh_gqd_class1_c1_b3lyp_optfreq_v02)
                        run_id="B3LYP-COOH-GQD-C1-002" ;;
                    cooh_gqd_class2_c3_b3lyp_optfreq_v02)
                        run_id="B3LYP-COOH-GQD-C2-003" ;;
                    cooh_gqd_class1_c1_b3lyp_optfreq_v03)
                        run_id="B3LYP-COOH-GQD-C1-004" ;;
                    cooh_gqd_class2_c3_b3lyp_optfreq_v03)
                        run_id="B3LYP-COOH-GQD-C2-005" ;;
                esac
            fi
        fi

        if [[ -z "$run_id" ]]; then
            echo "ERROR: no run_id mapping for archived file: $file" >&2
            return 1
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



