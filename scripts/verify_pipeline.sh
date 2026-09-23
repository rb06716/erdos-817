#!/bin/bash
# verify_pipeline.sh -- re-run the full n = 7 computation behind g_3(7) = 474, in the order it was originally run,
# writing to a separate git-ignored directory (the published logs in results/ are never touched):
#
#   stage A: C (g3fast2 -DNOROOM)   N = 419..478   -> OUT/c_hi     (published: results/n7_scan)
#   stage B: Rust (g3verify)        N = 419..478   -> OUT/rust_hi  (published: results/n7_verify_rust_hi)
#   stage C: C                      N = 1..418     -> OUT/c_lo     (published: results/n7_c_lo)
#   stage D: Rust                   N = 1..418     -> OUT/rust_lo  (published: results/n7_verify_rust_lo)
#
# then compare, e.g.  python3 scripts/aggregate.py compare 7 --c OUT/c_hi/*.log --rust OUT/rust_hi/*.log
#
# usage: scripts/verify_pipeline.sh [JOBS=4] [stages=ABCD] [OUT=results/verify_run/pipeline]
set -euo pipefail
root=$(cd "$(dirname "$0")/.." && pwd)
jobs=${1:-4}
stages=${2:-ABCD}
out=${3:-results/verify_run/pipeline}
cd "$root"
make -s all
[[ $stages == *A* ]] && scripts/run_range.sh c    7 419 478 "$jobs" "$out/c_hi"
[[ $stages == *B* ]] && scripts/run_range.sh rust 7 419 478 "$jobs" "$out/rust_hi"
[[ $stages == *C* ]] && scripts/run_range.sh c    7 1   418 "$jobs" "$out/c_lo"
[[ $stages == *D* ]] && scripts/run_range.sh rust 7 1   418 "$jobs" "$out/rust_lo"
echo "all requested stages done -> $out"
