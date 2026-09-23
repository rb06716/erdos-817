#!/bin/bash
# finalize.sh -- build the canonical count table, run all C-vs-Rust comparisons, write checksums.
set -euo pipefail
root=$(cd "$(dirname "$0")/.." && pwd)
cd "$root"
C_HI="results/n7_scan/noroom_off0.log results/n7_scan/noroom_off1.log results/n7_scan/noroom_off2.log results/n7_scan/noroom_off3.log"
C_LO="results/n7_c_lo/c_0.log"
R_HI=$(ls results/n7_verify_rust_hi/rust_*.log)
R_LO=$(ls results/n7_verify_rust_lo/rust_*.log 2>/dev/null || true)

echo "== canonical count table (C, n = 7)"
python3 scripts/aggregate.py table 7 $C_LO $C_HI > results/n7_counts.csv
python3 - << 'EOF'
import csv
rows = list(csv.DictReader(open('results/n7_counts.csv')))
Ns = [int(r['N']) for r in rows]
assert Ns == list(range(1, len(Ns) + 1)), "N values must be 1..max without gaps"
first = min(int(r['N']) for r in rows if int(r['solutions']) > 0)
print("rows:", len(rows), "N = 1 ..", Ns[-1], "; first N with an admissible 7-set:", first)
print("admissible 7-sets per N from 474:", [(int(r['N']), int(r['V7'])) for r in rows if int(r['N']) >= 474])
EOF

echo "== C vs Rust, N = 419..478"
python3 scripts/aggregate.py compare 7 --c $C_HI --rust $R_HI
if [ -n "$R_LO" ]; then
  echo "== C vs Rust, N = 1..418"
  python3 scripts/aggregate.py compare 7 --c $C_LO --rust $R_LO
fi

echo "== certificates"
python3 verify/check_set.py 302,409,447,459,465,466,474
python3 verify/check_set.py 894,1196,1303,1341,1353,1359,1360,1368

echo "== checksums"
( find results -type f \( -name '*.log' -o -name '*.csv' -o -name '*.txt' -o -name '*.json' \) | sort | xargs sha256sum ) > results/SHA256SUMS
wc -l results/SHA256SUMS
