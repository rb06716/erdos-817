#!/bin/bash
# verify_pipeline.sh -- the full n = 7 computation used for the claim g_3(7) = 474, in the order it was run.
#
#   stage A: C (g3fast2 -DNOROOM)   N = 419..478   (4 interleaved processes)   [results/n7_scan]
#   stage B: Rust (g3verify)        N = 419..478                               [results/n7_verify_rust_hi]
#   stage C: C                      N = 1..418                                 [results/n7_c_lo]
#   stage D: Rust                   N = 1..418                                 [results/n7_verify_rust_lo]
#   then:    scripts/aggregate.py compare / table
#
# usage: scripts/verify_pipeline.sh [JOBS=4] [stages=ABCD]
set -euo pipefail
root=$(cd "$(dirname "$0")/.." && pwd)
jobs=${1:-4}
stages=${2:-ABCD}
cd "$root"
make -s all
[[ $stages == *A* ]] && scripts/run_range.sh c    7 419 478 "$jobs" results/n7_scan_repro
[[ $stages == *B* ]] && scripts/run_range.sh rust 7 419 478 "$jobs" results/n7_verify_rust_hi
[[ $stages == *C* ]] && scripts/run_range.sh c    7 1   418 "$jobs" results/n7_c_lo
[[ $stages == *D* ]] && scripts/run_range.sh rust 7 1   418 "$jobs" results/n7_verify_rust_lo
echo "all requested stages done"
