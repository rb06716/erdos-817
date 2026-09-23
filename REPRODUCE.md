# Reproducing the results

Tested on Ubuntu 24.04, x86-64 (Intel Xeon with AVX-512/BMI2), gcc 13.3, rustc 1.94, Python 3.11.
Only standard tools are needed; no network access after cloning.

## 0. Build (seconds)

```sh
make all          # builds bin/g3fast2, bin/g3fast2_noroom, bin/g3search, bin/gk_search, bin/gk_verify,
                  #        bin/g3profile, bin/g3verify
```
`src/g3fast2.c` uses the BMI2 `PEXT` instruction (`-march=native`). On a CPU without BMI2 use the portable
reference `bin/g3search` (same results, ~3x slower) — see step 4.

## 1. Check the certificate for the upper bound (milliseconds)

```sh
python3 verify/check_set.py 302,409,447,459,465,466,474
# PASS n=7 max=474 ... ternary sums distinct: True (2187 sums) | H(A) 3-AP-free: True (|H|=128)
python3 verify/check_set.py 878,1192,1299,1335,1349,1353,1356,1380     # g_3(8) <= 1380
```

## 2. Sanity checks against known values (under a minute)

```sh
python3 verify/bruteforce.py --equivalence          # Lemma 1, 0 mismatches
./bin/g3fast2 6 1 168 | tail -3                      # g_3(6) = 168, two extremal sets
./bin/g3fast2 5 1 60  | tail -3                      # g_3(5) = 60
python3 verify/bruteforce.py 7 26 > /tmp/bf7.txt && ./bin/g3verify 7 1 26 > /tmp/rv7.txt \
  && diff <(grep -v SOL /tmp/bf7.txt | sed 's/ solutions=.*//') <(grep -v SOL /tmp/rv7.txt | sed 's/ solutions=.*//') && echo OK
```

## 3. The main computation (CPU-hours; embarrassingly parallel over N)

Single values of `N` can be checked in isolation (≈ 2–4 minutes each for C, ≈ 3x that for Rust, at N ≈ 450
on one 2.1 GHz core):

```sh
./bin/g3fast2_noroom 7 474 474     # finds exactly one set: SOLUTION N=474 {302,409,447,459,465,466,474}
./bin/g3fast2_noroom 7 473 473     # N=473 ... solutions=0 nodes: 1 472 109976 15952078 1195092113 6608257434 0
./bin/g3verify       7 473 473     # N=473 n=7 V: 1 472 109976 15952078 1195092113 6608257434 0 solutions=0
```

Full runs (4 parallel jobs; each command prints "done" at the end):

```sh
scripts/run_range.sh c    7 419 478 4 results/repro_c_hi       # ~1.2 h wall on 4 cores
scripts/run_range.sh rust 7 419 478 4 results/repro_rust_hi    # ~3 h wall on 4 cores
scripts/run_range.sh c    7 1   418 4 results/repro_c_lo       # ~0.5 h
scripts/run_range.sh rust 7 1   418 4 results/repro_rust_lo    # ~1.5 h
python3 scripts/aggregate.py compare 7 --c results/repro_c_hi/*.log --rust results/repro_rust_hi/*.log
python3 scripts/aggregate.py compare 7 --c results/repro_c_lo/*.log --rust results/repro_rust_lo/*.log
```

Expected: `0 mismatches`, no `SOLUTION` line for any `N ≤ 473`, exactly one for `N = 474`.
To compare against the published logs instead, pass `results/n7_scan/*.log` etc. (file list in README.md), or
compare with the CSV table:

```sh
python3 scripts/aggregate.py table 7 results/repro_c_lo/*.log results/repro_c_hi/*.log > my_counts.csv
diff my_counts.csv results/n7_counts.csv && echo "identical canonical counts"
sha256sum results/n7_counts.csv    # compare with results/SHA256SUMS
```

### Last-level cross-check where solutions exist (band check, ~1 h on one core)

```sh
for N in $(seq 474 520); do
  ./bin/g3fast2  7 $N $N 0 1 0 $(( N * 55 / 100 )) | grep -E "SOLUTION|^N=" >> my_c_band.log
  ./bin/g3verify 7 $N $N 1 0 550                   | grep -E "SOLUTION|^N=" >> my_rust_band.log
done
diff <(grep SOLUTION my_c_band.log | sort) <(grep SOLUTION my_rust_band.log | sort) && echo identical   # 12,010 sets
```
(The published run used `bin/g3verify_band`, a build of the same Rust source; `results/n7_band_crosscheck/`.)

### One-shot pipeline

`scripts/verify_pipeline.sh 4` runs stages A–D above in sequence (C and Rust, both ranges), and
`scripts/finalize.sh` rebuilds `results/n7_counts.csv`, repeats all comparisons and writes `results/SHA256SUMS`.

## 4. Portable / slower alternatives

* `bin/g3search 7 N N` (no PEXT, default room pruning) visits a subset of the NOROOM tree; it must report
  the same solutions. Node counts of `g3search` equal those of `bin/g3fast2` (room-pruned mode).
* `bin/gk_search 3 n Nlo Nhi` works directly from the definition (subset-sum bitset + AP test); practical for
  `n ≤ 6` or small `N`; its per-level counts equal `bin/g3fast2_noroom`'s.

## 5. Secondary results

```sh
# upper bounds for n = 8..14 (hole chains); certificates
python3 scripts/beam.py 300 12 12 40            # n = 3..12: 8 22 60 168 474 1368 3974 11578 34088 100422 (~1 min)
python3 scripts/offset_recursion.py             # greedy chains from several seeds
python3 verify/check_set.py 894,1196,1303,1341,1353,1359,1360,1368
# k = 4, 5 (two independent programs must agree)
./bin/gk_search 4 6 1 79 1                      # g_4(6) = 79, witness {2,29,45,74,77,79}
./bin/gk_search 5 7 1 60 0 > a.log; ./bin/gk_verify 5 7 1 60 > b.log   # g_5(7) = 60, 4 extremal sets
diff <(grep -v SOL a.log | sed 's/ time=.*//') <(grep -v SOL b.log) && echo "counts identical"
python3 scripts/summary_table.py                # table of values, Korsky bounds, ratios
```
