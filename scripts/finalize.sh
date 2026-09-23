#!/bin/bash
# finalize.sh -- maintainer script: rebuild the canonical count table from the published logs, repeat all
# C-vs-Rust comparisons, check the certificates, and rewrite results/SHA256SUMS. It rewrites the tracked files
# results/n7_counts.csv (which must come out unchanged: check `git diff`) and results/SHA256SUMS, which covers
# every *tracked* *.log/*.csv/*.txt/*.json under results/ (git add new result files first).
set -euo pipefail
root=$(cd "$(dirname "$0")/.." && pwd)
cd "$root"
C_HI=$(ls results/n7_scan/noroom_off*.log)
C_LO=$(ls results/n7_c_lo/*.log)
R_HI=$(ls results/n7_verify_rust_hi/rust_*.log)
R_LO=$(ls results/n7_verify_rust_lo/rust_*.log 2>/dev/null || true)

echo "== canonical count table (C, n = 7)"
tmp=$(mktemp)
trap 'rm -f "$tmp"' EXIT
python3 scripts/aggregate.py table 7 $C_LO $C_HI > "$tmp"
python3 - "$tmp" << 'PYEOF'
import csv, sys
rows = list(csv.DictReader(open(sys.argv[1])))
Ns = [int(r['N']) for r in rows]
assert Ns == list(range(1, len(Ns) + 1)), "N values must be 1..max without gaps"
first = min(int(r['N']) for r in rows if int(r['solutions']) > 0)
print("rows:", len(rows), "N = 1 ..", Ns[-1], "; first N with an admissible 7-set:", first)
print("admissible 7-sets per N from 474:", [(int(r['N']), int(r['V7'])) for r in rows if int(r['N']) >= 474])
PYEOF
cat "$tmp" > results/n7_counts.csv

echo "== C vs Rust, N = 419..478"
python3 scripts/aggregate.py compare 7 --c $C_HI --rust $R_HI
if [ -n "$R_LO" ]; then
  echo "== C vs Rust, N = 1..418"
  python3 scripts/aggregate.py compare 7 --c $C_LO --rust $R_LO
fi

echo "== certificates"
python3 verify/check_set.py 302,409,447,459,465,466,474
python3 verify/check_set.py 894,1196,1303,1341,1353,1359,1360,1368

echo "== checksums (tracked files only; check with: sha256sum -c results/SHA256SUMS, from the repository root)"
git ls-files -z results | grep -z -E '\.(log|csv|txt|json)$' | LC_ALL=C sort -z | xargs -0 sha256sum > results/SHA256SUMS
wc -l results/SHA256SUMS
