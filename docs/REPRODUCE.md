# Reproducing the results

Tested on Ubuntu 24.04, x86-64 (Intel Xeon with AVX-512/BMI2), gcc 13.3, rustc 1.94, Python 3.11; the
`quick` and `critical` verifications were also run by the repository owner on Google Colab (Intel, 8 vCPUs).
Only standard tools are needed: a C compiler, Rust/cargo (for the independent verifier) and Python 3. The
verification tools use only the Python standard library; the construction scripts in `scripts/` (and hence
`make check`) also need NumPy: `python3 -m pip install -r requirements.txt`. No network access is needed after
cloning and installing. All commands are run from the repository root.

## Fast checks

```sh
make all       # build everything (section 0)
make check     # ~2 min: 12 consistency checks (tests/run_checks.sh), prints PASS/FAIL per check
make verify    # = python3 verify/verify_result.py quick (below)
```
GitHub Actions runs `make all` and `make check` on every push (`.github/workflows/checks.yml`), and
`verify_result.py quick --rust` when the programs or the published data change, or on demand
(`.github/workflows/verify.yml`).

## One-command verification (recommended for a human verifier)

```sh
python3 verify/verify_result.py quick       # ~5-15 min: builds, certificates, Lemma 1, g_3(5), g_3(6),
                                            #   exhaustive search at N = 473, 474 vs. the published table
python3 verify/verify_result.py critical    # hours: every N = 419..478 (with Korsky's bound g_3(7) >= 419)
python3 verify/verify_result.py full        # hours: every N = 1..478 (without it)
```
Add `--rust` (any mode) to also run the independent Rust verifier at N = 473, 474. Every check prints
PASS/FAIL, and the exit status is 0 only if all pass. Runs are resumable: there is one log per N in `--out`,
default `results/verify_run/` (git-ignored). The same checks run in Google Colab with no local setup; see
`verify/colab_verify.ipynb`, where a CPU runtime is enough. To open it in Colab: File → Open notebook → GitHub,
then enter `rb06716/erdos-817`. Alternatively, upload the file unchanged.

No GitHub access at all: upload `verify/colab_verify_standalone.ipynb` to Colab. It contains compressed copies
of the programs and the published count table, and prints their SHA-256 for comparison with the repository.
Rebuild it with `python3 scripts/make_standalone_notebook.py`.

Colab without the notebook file: paste this into one cell of a new notebook and run it.
```python
import os
if not os.path.exists('/content/erdos-817'):
    !git clone --depth 1 https://github.com/rb06716/erdos-817 /content/erdos-817
os.chdir('/content/erdos-817')
!python3 verify/verify_result.py quick
```

## 0. Build (seconds)

```sh
make all          # builds bin/g3fast2, bin/g3fast2_noroom, bin/g3search, bin/gk_search, bin/gk_verify,
                  #        bin/g3profile, bin/g3verify
```
`src/g3fast2.c` and `src/g3profile.c` use the BMI2 `PEXT` instruction when `-march=native` enables it.
Otherwise, e.g. on ARM / Apple Silicon, they compile a portable replacement that gives identical results. On Apple clang use
`make CFLAGS="-O3 -mcpu=native"`. On AMD Zen 1/2, where `PEXT` is microcoded and slow, build with
`make CFLAGS="-O3 -march=native -DNO_PEXT"`; `verify_result.py` does this automatically.

The portable path was checked against the PEXT build:
* 10⁸ random words;
* identical output for n = 5, 6 (N ≤ 175, both search modes);
* identical output for n = 7 at N = 473, 474, matching `results/n7_counts.csv`;
* `g3profile`: identical output for n = 5, 6, 7 (profile windows) and for the n = 8 window search at M = 1368
  (the published line of `results/n8_upper/profile8_fine.log`).

## 1. Check the certificate for the upper bound (milliseconds)

```sh
python3 verify/check_set.py 302,409,447,459,465,466,474
# PASS n=7 max=474 ... ternary sums distinct: True (2187 sums) | H(A) 3-AP-free: True (|H|=128)
python3 verify/check_set.py 894,1196,1303,1341,1353,1359,1360,1368     # g_3(8) <= 1368
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

Single values of `N` can be checked in isolation (≈ 2–4 minutes each for C, ≈ 1–3× that for Rust depending on
the CPU, at N ≈ 450 on one 2.1 GHz core):

```sh
./bin/g3fast2_noroom 7 474 474     # finds exactly one set: SOLUTION N=474 {302,409,447,459,465,466,474}
./bin/g3fast2_noroom 7 473 473     # N=473 ... solutions=0 nodes: 1 472 109976 15952078 1195092113 6608257434 0
./bin/g3verify       7 473 473     # N=473 n=7 V: 1 472 109976 15952078 1195092113 6608257434 0 solutions=0
```

Full runs (4 parallel jobs; each command prints "done" at the end):

```sh
R=results/verify_run                                             # git-ignored
scripts/run_range.sh c    7 419 478 4 $R/repro_c_hi       # ~1.2 h wall on 4 cores
scripts/run_range.sh rust 7 419 478 4 $R/repro_rust_hi    # ~3 h wall on 4 cores
scripts/run_range.sh c    7 1   418 4 $R/repro_c_lo       # ~0.5 h
scripts/run_range.sh rust 7 1   418 4 $R/repro_rust_lo    # ~1.5 h
python3 scripts/aggregate.py compare 7 --c $R/repro_c_hi/*.log --rust $R/repro_rust_hi/*.log
python3 scripts/aggregate.py compare 7 --c $R/repro_c_lo/*.log --rust $R/repro_rust_lo/*.log
```

Expected: `0 mismatches`, no `SOLUTION` line for any `N ≤ 473`, exactly one for `N = 474`.
To compare against the published logs instead, pass `results/n7_scan/*.log` etc. (file list in
`results/README.md`), or compare with the CSV table:

```sh
python3 scripts/aggregate.py table 7 $R/repro_c_lo/*.log $R/repro_c_hi/*.log > /tmp/my_counts.csv
diff /tmp/my_counts.csv results/n7_counts.csv && echo "identical canonical counts"
sha256sum results/n7_counts.csv    # compare with results/SHA256SUMS
```

### Last-level cross-check where solutions exist (band check, ~1 h on one core)

```sh
for N in $(seq 474 520); do
  ./bin/g3fast2  7 $N $N 0 1 0 $(( N * 55 / 100 )) | grep -E "SOLUTION|^N=" >> /tmp/my_c_band.log
  ./bin/g3verify 7 $N $N 1 0 550                   | grep -E "SOLUTION|^N=" >> /tmp/my_rust_band.log
done
diff <(grep SOLUTION /tmp/my_c_band.log | sort) <(grep SOLUTION /tmp/my_rust_band.log | sort) && echo identical   # 12,010 sets
```
(The published run used `bin/g3verify_band`, a byte-identical copy of `bin/g3verify`; see
`results/n7_band_crosscheck/`.)

### One-shot pipeline

`scripts/verify_pipeline.sh 4` runs the four `run_range.sh` stages above in sequence, writing to
`results/verify_run/pipeline/{c_hi,rust_hi,c_lo,rust_lo}` (git-ignored); compare them with the `aggregate.py`
commands above. `scripts/finalize.sh` is the maintainer script that rebuilt `results/n7_counts.csv` and
`results/SHA256SUMS` from the published logs; it rewrites those tracked files.

### Novelty check against the OEIS export (optional; ~1.6 GB download)

```sh
python3 scripts/oeis_novelty_check.py      # sparse-clones github.com/oeis/oeisdata, searches all value strings
```

## 4. Portable / slower alternatives

* `bin/g3search 7 N N` (no PEXT, default room pruning) visits a subset of the NOROOM tree; it must report
  the same solutions. Node counts of `g3search` equal those of `bin/g3fast2` (room-pruned mode).
* `bin/gk_search 3 n Nlo Nhi` works directly from the definition (subset-sum bitset + AP test); practical for
  `n ≤ 6` or small `N`; its per-level counts equal `bin/g3fast2_noroom`'s.

## 5. Secondary results

```sh
# upper bounds for n = 8..14 (hole chains) and their certificates
python3 scripts/beam.py 300 12 12 40            # n = 3..12: 8 22 60 168 474 1368 3974 11578 34088 100422 (~30 s)
python3 -c "import sys; sys.path.insert(0, 'scripts'); from hole_dp import first_hole; B = [8,9,15,27,65,172,474,1368,3974,11578,34088,100422]; M13 = first_hole(B)[0]; print(M13, first_hole(B + [M13])[0])"   # n = 13, 14: 295924 879824 (~3 s)
python3 verify/check_set.py $(python3 -c "u = [0,8,9,15,27,65,172,474,1368,3974,11578,34088,100422,295924,879824]; print(' '.join(','.join(str(u[n] - u[i]) for i in range(n)) for n in range(8, 15)))")   # certificates n = 8..14: 7 x PASS (~20 s)
python3 scripts/offset_recursion.py             # greedy first-hole continuations of the n = 3, 5, 6, 7 optima
python3 scripts/make_certificates.py /tmp/cert  # sum lists + SHA-256 as in results/certificates/ (compare)
# k = 4, 5 (two independent programs must agree)
./bin/gk_search 4 6 1 79 1                      # g_4(6) = 79, witness {2,29,45,74,77,79}
./bin/gk_search 5 7 1 60 0 > /tmp/a.log; ./bin/gk_verify 5 7 1 60 > /tmp/b.log   # g_5(7) = 60, 4 extremal sets
diff <(grep -v SOL /tmp/a.log | sed 's/ time=.*//') <(grep -v SOL /tmp/b.log) && echo "counts identical"
./bin/gk_search 5 8 1 92 0 > /tmp/c.log; ./bin/gk_verify 5 8 1 92 > /tmp/d.log   # g_5(8) = 92 (~1 h for gk_verify)
diff <(grep -v SOL /tmp/c.log | sed 's/ time=.*//') <(grep -v SOL /tmp/d.log) && echo "counts identical"
# g_4(7) = 225 (per N: up to ~50 min for gk_search, ~25 min for gk_verify at N ≈ 225; ~19 CPU-hours for all N)
./bin/gk_verify 4 7 224 224                     # N=224 k=4 n=7 V: 1 222 23925 1485698 31344180 18019553 0
./bin/gk_search 4 7 225 225 0                   # all extremal sets at N = 225; compare with gk_verify 4 7 225 225
python3 results/gk/g4_n7_verify/compare.py     # compares the published logs of both programs
python3 scripts/summary_table.py                # table of values, Korsky bounds, ratios
# Bae (2002) / Bae–Choi (2003) claim check: all admissible 6-sets with maximum <= 169 (seconds)
./bin/g3fast2_noroom 6 1 169 | grep SOLUTION     # two sets at 168, one ({109,...,169}) at 169
./bin/g3verify 6 166 169 | grep SOLUTION         # same, independent program
```
