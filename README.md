# g₃(7) = 474: a new exact value for Erdős Problem #817

**Main result.** The Erdős–Sárközy function `g₃(n)` is the least `N` such that some `n`-element set
`A ⊆ {1,…,N}` has subset sums `H(A) = {Σ_{a∈S} a : S ⊆ A}` containing no non-constant 3-term arithmetic
progression. Previously known: `g₃(1..6) = 1, 3, 8, 22, 60, 168` and `419 ≤ g₃(7) ≤ 504`
(OEIS [A399720](https://oeis.org/A399720), September 2026). This package establishes

> **g₃(7) = 474**, attained by the **unique** extremal set `A = {302, 409, 447, 459, 465, 466, 474}`.

**Secondary results.**

* New certified upper bounds for `n = 8…14` (previous best `(168/729)·3ⁿ`):

  | n | 8 | 9 | 10 | 11 | 12 | 13 | 14 |
  | --- | --- | --- | --- | --- | --- | --- | --- |
  | g₃(n) ≤ | 1368 | 3974 | 11578 | 34088 | 100422 | 295924 | 879824 |
  | previous | 1512 | 4536 | 13608 | 40824 | 122472 | 367416 | 1102248 |

* Structure: every extremal set for `n = 4…7` is a *hole chain* `{u_n − u_i}` in which each `u_{k+1}` is
  the least (or, at most once, a later) value keeping `{u_{k+1} − u_i}` admissible. For n = 7:
  `u = 0, 8, 9, 15, 27, 65, 172, 474`. A beam search over such chains rediscovers every known optimum in
  about a second. Continuing the n = 7 chain greedily gives the bounds above.
* The 4- and 5-term analogues from the same Erdős problem (not in the OEIS; see PRIOR_ART.md for caveats):
  `g₄(1..7) = 1, 3, 5, 14, 40, 79, 225` and `g₅(1..8) = 1, 2, 4, 6, 14, 22, 60, 92`.
* The value `a(7) = 466` suggested as possible in A399720 is excluded, and `{1} ∪ 3A` (giving 504) is not
  optimal at n = 7.

**How.** An exhaustive search, organized per maximum `N`. It uses the fact that `H(A)` is 3-AP-free iff
all `3ⁿ` sums `Σ εᵢaᵢ` (`εᵢ ∈ {0,1,2}`) are distinct (proved in METHODS.md), and a bitset of all
`{−2..2}`-combinations for O(1) incremental tests. The search was re-run by an independently written Rust
program with the opposite search order. Both report identical canonical counts (`V_k(N)` = number of
admissible `k`-subsets of `[1, N]` containing `N`, e.g. `V₆(473) = 6,608,257,434`) for every `N`.

## Documents

| file | content |
| --- | --- |
| [DISCOVERY.md](DISCOVERY.md) | the claim, novelty, significance, evidence, falsification, verification status |
| [METHODS.md](METHODS.md) | proofs of the reformulation and search lemmas, window invariant, algorithms, constructions |
| [PRIOR_ART.md](PRIOR_ART.md) | literature and database search, novelty assessment |
| [REPRODUCE.md](REPRODUCE.md) | commands to rebuild and re-run everything |
| [LIMITATIONS.md](LIMITATIONS.md) | what is and is not established |
| [research_log.md](research_log.md) | chronological log: directions considered, decisions, failures, timings |
| [SUBMISSION_DRAFTS.md](SUBMISSION_DRAFTS.md) | draft OEIS / forum texts (not submitted) |

## Layout

```
src/g3fast2.c          optimized exhaustive search (PEXT); -DNOROOM = canonical counts   [main computation]
src/g3search.c         portable reference search;  src/g3fast.c  intermediate version (provenance)
src/g3profile.c        profile-window search (constructions only, n = 8)
src/gk_search.c        definition-level search for general k (subset-sum bitset + AP test)
verify/g3verify_rs/    independent Rust implementation (decreasing order)                  [verification]
verify/gk_verify.c     independent implementation for general k (pairwise AP test)
verify/bruteforce.py   definition-level brute force for small cases
verify/check_set.py    exact certificate checker for a given set
scripts/               run_range.sh, aggregate.py, finalize.sh, verify_pipeline.sh (runs and comparisons);
                       hole_dp.py, holes_all.py, beam.py, offset_*.py (chain constructions);
                       summary_table.py, conway_guy_ternary.py, mc_valid.py
results/               raw logs of every run, count tables, certificates, checksums
```

## Quick check

```sh
make all
python3 verify/check_set.py 302,409,447,459,465,466,474    # certificate for g_3(7) <= 474 (ms)
./bin/g3fast2_noroom 7 473 473                              # one of the non-existence runs (~3 min)
./bin/g3verify       7 473 473                              # same N, independent program (~8 min)
python3 scripts/beam.py 300 12 8 40                         # chain search: 8, 22, 60, 168, 474, 1368 (~1 s)
```
