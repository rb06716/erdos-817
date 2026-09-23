#!/bin/bash
# run_checks.sh -- fast consistency checks (about 2 minutes); run via `make check`.
#
# Checks the reformulation against the raw definition, both certificates, the independent implementations
# against each other and against definition-level brute force on small cases, the known values g_3(5), g_3(6)
# (including the Bae-Choi 2003 n = 6 correction), the k = 4, 5 programs, the hole-chain construction, and one
# n = 7 value against the published count table. The decisive n = 7 values are checked by `make verify`.
# Prints PASS/FAIL per check; exit status 0 iff all pass.
set -u
cd "$(dirname "$0")/.."
T=$(mktemp -d)
trap 'rm -rf "$T"' EXIT
pass=0; fail=0
check() {                          # check "description" command...
    local name=$1; shift
    if "$@" > "$T/out" 2>&1; then echo "PASS  $name"; pass=$((pass + 1))
    else echo "FAIL  $name"; sed 's/^/      /' "$T/out" | tail -5; fail=$((fail + 1)); fi
}

check "Lemma 1: reformulation agrees with the definition (random + exhaustive)" \
    bash -c "python3 verify/bruteforce.py --equivalence | grep -q 'mismatches: 0'"
check "certificate: g_3(7) <= 474 via {302,409,447,459,465,466,474}" \
    python3 verify/check_set.py 302,409,447,459,465,466,474
check "certificate: g_3(8) <= 1368 via {894,1196,1303,1341,1353,1359,1360,1368}" \
    python3 verify/check_set.py 894,1196,1303,1341,1353,1359,1360,1368

python3 verify/bruteforce.py 7 26 > "$T/bf7" && ./bin/g3verify 7 1 26 > "$T/rv7" && ./bin/g3fast2_noroom 7 1 26 > "$T/c7"
check "n = 7, N <= 26: definition-level brute force = Rust = C (canonical counts)" \
    bash -c "diff <(grep -v SOL $T/bf7 | sed 's/ solutions=.*//') <(grep -v SOL $T/rv7 | sed 's/ solutions=.*//') &&
             python3 scripts/aggregate.py compare 7 --c $T/c7 --rust $T/rv7"

./bin/g3fast2_noroom 6 1 175 > "$T/c6" && ./bin/g3verify 6 1 175 > "$T/r6"
check "n = 6, N <= 175: C = Rust (canonical counts and solution lists)" \
    python3 scripts/aggregate.py compare 6 --c "$T/c6" --rust "$T/r6"
check "g_3(6) = 168 with exactly two extremal sets" \
    bash -c "[ \"\$(grep -m1 -o 'SOLUTION N=[0-9]*' $T/c6)\" = 'SOLUTION N=168' ] &&
             [ \$(grep -c '^SOLUTION N=168 ' $T/c6) -eq 2 ]"
check "Bae-Choi (2003) correction: {109,147,161,166,168,169} is the only admissible 6-set with max 169" \
    bash -c "[ \"\$(grep '^SOLUTION N=169 ' $T/c6)\" = 'SOLUTION N=169 {109,147,161,166,168,169}' ]"
./bin/g3fast2_noroom 5 1 70 > "$T/c5"
check "g_3(5) = 60" bash -c "[ \"\$(grep -m1 -o 'SOLUTION N=[0-9]*' $T/c5)\" = 'SOLUTION N=60' ]"

./bin/g3fast2_noroom 7 300 300 > "$T/c300" && ./bin/g3verify 7 300 300 > "$T/r300"
check "n = 7, N = 300: C and Rust reproduce the published row of results/n7_counts.csv" \
    bash -c "grep -q '^300,' results/n7_counts.csv &&
             python3 scripts/aggregate.py compare 7 --c $T/c300 --rust $T/r300 &&
             [ \"\$(python3 scripts/aggregate.py table 7 $T/c300 | tail -1)\" = \"\$(grep '^300,' results/n7_counts.csv)\" ]"

check "k = 4: g_4(6) = 79 (first solution of gk_search at N = 79)" \
    bash -c "./bin/gk_search 4 6 1 79 1 | grep -q 'SOLUTION k=4 N=79 '"
./bin/gk_search 5 7 1 60 0 > "$T/a5" && ./bin/gk_verify 5 7 1 60 > "$T/b5"
check "k = 5, n = 7, N <= 60: gk_search = gk_verify (counts), four extremal sets at N = 60" \
    bash -c "diff <(grep -v SOL $T/a5 | sed 's/ time=.*//') <(grep -v SOL $T/b5) &&
             [ \$(grep -c 'SOLUTION k=5 N=60 ' $T/a5) -eq 4 ]"

check "hole-chain beam search reproduces 8, 22, 60, 168, 474, 1368" \
    bash -c "python3 scripts/beam.py 300 12 8 40 | grep -o 'best M=[0-9]*' | sed 's/best //' | tr '\n' ' ' |
             grep -q 'M=8 M=22 M=60 M=168 M=474 M=1368'"

echo
echo "$pass passed, $fail failed"
[ "$fail" -eq 0 ]
