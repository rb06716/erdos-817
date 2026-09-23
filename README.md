# g₃(7) = 474: a new exact value for Erdős Problem #817

**Result.** The Erdős–Sárközy function `g₃(n)` is the least `N` such that some `n`-element set
`A ⊆ {1,…,N}` has subset sums `H(A) = {Σ_{a∈S} a : S ⊆ A}` containing no non-constant 3-term arithmetic
progression. Previously known: `g₃(1..6) = 1, 3, 8, 22, 60, 168` and `419 ≤ g₃(7) ≤ 504`
(OEIS [A399720](https://oeis.org/A399720), Sept 2026). This package establishes

> **g₃(7) = 474**, attained by the **unique** extremal set `A = {302, 409, 447, 459, 465, 466, 474}`,

and, as by-products,

* `g₃(8) ≤ 1380` via `{878, 1192, 1299, 1335, 1349, 1353, 1356, 1380}` (previous bound `3·474 = 1422`);
* the value `a(7) = 466` suggested as possible in A399720 is excluded;
* first values of the `k = 4, 5` analogues from the same problem: `g₄(1..6) = 1, 3, 5, 14, 40, 79`,
  `g₅(1..6) = 1, 2, 4, 6, 14, 22` (secondary; see DISCOVERY.md for status).

**How.** An exhaustive search over all candidate sets, organized per maximum `N`. It uses the fact that `H(A)` is
3-AP-free iff all `3ⁿ` sums `Σ εᵢaᵢ`, `εᵢ ∈ {0,1,2}`, are distinct (proved in METHODS.md), and a bitset
of all `{−2..2}`-combinations for O(1) incremental tests. It was checked by an independently written Rust
program with a different search order: both report identical canonical counts
(`V_k(N)` = number of admissible `k`-subsets of `[1,N]` containing `N`) for every `N`.

## Documents

| file | content |
| --- | --- |
| [DISCOVERY.md](DISCOVERY.md) | the claim, novelty, significance, evidence, falsification, verification status |
| [METHODS.md](METHODS.md) | proofs of the reformulation and the search lemmas; algorithms |
| [PRIOR_ART.md](PRIOR_ART.md) | literature and database search, novelty assessment |
| [REPRODUCE.md](REPRODUCE.md) | commands to rebuild and re-run everything |
| [LIMITATIONS.md](LIMITATIONS.md) | what is and is not established |
| [research_log.md](research_log.md) | chronological log: directions considered, decisions, failures, timings |

## Layout

```
src/g3search.c        reference exhaustive search (portable)
src/g3fast2.c         optimized exhaustive search (PEXT); -DNOROOM for canonical counts  [main computation]
src/g3fast.c          intermediate version (kept for provenance)
src/g3profile.c       profile-window search, upper-bound constructions only (n = 8)
src/gk_search.c       definition-level search for general k (subset-sum bitset + AP test)
verify/g3verify_rs/   independent Rust implementation (decreasing order)                  [verification]
verify/bruteforce.py  definition-level brute force for small cases
verify/check_set.py   exact certificate checker for a given set
scripts/              run_range.sh (parallel runs), aggregate.py (tables, C-vs-Rust comparison),
                      verify_pipeline.sh, mc_valid.py (feasibility estimate)
results/              raw logs of every run, counts table, checksums
```

## Quick check (seconds)

```sh
make all
python3 verify/check_set.py 302,409,447,459,465,466,474     # certificate for g_3(7) <= 474
./bin/g3fast2_noroom 7 473 473                               # one of the 55 non-existence runs (~3 min)
```
