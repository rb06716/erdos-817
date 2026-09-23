#!/bin/bash
# run_range.sh PROGRAM n NLO NHI JOBS OUTDIR
#   PROGRAM: c    -> bin/g3fast2_noroom (canonical counts, all admissible sets)
#            rust -> bin/g3verify       (independent implementation, canonical counts)
#   Splits N = NLO..NHI over JOBS interleaved processes (N = NLO + JOBS*j + k), logs to OUTDIR/<prog>_k.log
set -euo pipefail
prog=$1; n=$2; lo=$3; hi=$4; jobs=$5; out=$6
root=$(cd "$(dirname "$0")/.." && pwd)
mkdir -p "$out"
pids=()
for ((k = 0; k < jobs; k++)); do
  case $prog in
    c)    "$root/bin/g3fast2_noroom" "$n" "$lo" "$hi" 0 "$jobs" "$k" > "$out/c_$k.log" & ;;
    rust) "$root/bin/g3verify" "$n" "$lo" "$hi" "$jobs" "$k" > "$out/rust_$k.log" & ;;
    *) echo "unknown program $prog" >&2; exit 2 ;;
  esac
  pids+=($!)
done
for p in "${pids[@]}"; do wait "$p"; done
echo "done: $prog n=$n N=$lo..$hi -> $out"
