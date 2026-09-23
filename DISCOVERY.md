# Discovery: the Erdős–Sárközy function satisfies g₃(7) = 474

## The discovery in one sentence

The least `N` for which some 7-element subset of `{1,…,N}` has subset sums containing no non-constant
3-term arithmetic progression is **`g₃(7) = 474`**, and the extremal set is **unique**:
**`A = {302, 409, 447, 459, 465, 466, 474}`**.

Context: Erdős Problem #817; OEIS A399720 currently lists `a(1..6) = 1, 3, 8, 22, 60, 168` and states
`419 ≤ a(7) ≤ 504`.

## Secondary results (same package, weaker status where noted)

1. **New upper bounds** (explicit, certified sets; previously best: `(168/729)·3ⁿ`, or `(474/2187)·3ⁿ` once
   `g₃(7)` is known):

   | n | 8 | 9 | 10 | 11 | 12 | 13 | 14 |
   | --- | --- | --- | --- | --- | --- | --- | --- |
   | new bound | **1368** | **3974** | **11578** | **34088** | **100422** | **295924** | **879824** |
   | previous (168/729)·3ⁿ | 1512 | 4536 | 13608 | 40824 | 122472 | 367416 | 1102248 |

   All are of the form `A_n = {u_n − u_i : 0 ≤ i < n}` with
   `u = (0, 8, 9, 15, 27, 65, 172, 474, 1368, 3974, 11578, 34088, 100422, 295924, 879824)`, where from
   `u_4 = 27` on every term is the least admissible "hole". All are certified by `verify/check_set.py`
   (e.g. n = 14: all 4,782,969 ternary sums distinct, and the 16,384 subset sums contain no 3-AP).
2. **Structure ("hole chains").** Every extremal set for `n = 4, 5, 6, 7` (two each for n = 4, 5, 6; the unique
   one for n = 7) has the form `{u_n − u_i}` where each `u_{k+1}` is an admissible "hole" for
   `{u_1,…,u_k}` (i.e. `{u_{k+1} − u_i : i ≤ k}` is itself admissible). A beam search restricted to such chains
   (`scripts/beam.py`, seconds) reproduces **every** known exact value `8, 22, 60, 168, 474` together with
   the extremal sets, and gives the n = 8–14 bounds above. Chains are common but not universal (87–95 % of
   admissible sets near the optimum for n = 5, 6), so for `n ≥ 8` these are upper bounds, not claimed optima.
3. **The 4- and 5-term analogues** from the same Erdős problem (no OEIS entries exist):
   `g₄(1..6) = 1, 3, 5, 14, 40, 79` (unique extremal set `{2, 29, 45, 74, 77, 79}` at n = 6; `g₄(7) ≥ 174`),
   `g₅(1..7) = 1, 2, 4, 6, 14, 22, 60`. Two independent programs (`src/gk_search.c`, `verify/gk_verify.c`)
   agree on all canonical counts; for n ≤ 5 (k = 4) and n ≤ 6 (k = 5) also a Python brute force.

## Why it appears novel

* OEIS A399720 (created 2026-09-09, last edited 2026-09-14; checked in the official git export dated
  2026-09-22) gives only `419 ≤ a(7) ≤ 504` and remarks that `a(7) = 466` "is not excluded".
* The verification repository `firesh/erdos817-subset-sum-progressions-audit` (2026-09-18) computed
  `g₃(5), g₃(6)` and reports its `n = 7` search as incomplete (only `N ≤ 313` excluded), listing `g₃(7)` as open.
* Korsky (arXiv:2606.24139, June 2026) proves `g₃(7) ≥ b₇ = 419` and computes `g₃(n)` only for `n ≤ 4`.
* No web source, OEIS entry (full-text search of all 399,468 entries), or GitHub repository found reports
  474, the extremal set, the chain sequence, or any `g₄`/`g₅` values. Details: PRIOR_ART.md.

## Why it matters

* It is the next exact value of a function asked about by Erdős and Sárközy, whose asymptotic question was
  answered only this month (Costa, arXiv:2609.06303: `g₃(n)/3ⁿ → 0`). Exact small values are the only
  ground truth for calibrating constructions and bounds.
* It settles two questions raised in the OEIS entry: `a(7) ≠ 466` (so the coincidence of
  `1, 3, 8, 22, 60, 168` with the rooted-tree sequences A318821/A318863, which continue with 466, ends here),
  and `a(7) < 504 = 3·a(6)`: the recursive construction `A ↦ {1} ∪ 3A` is not optimal at n = 7.
* The gap to Korsky's bandwidth lower bound grows: `g₃(n) − b_n = 0, 0, 0, 1, 4, 16, 55` for `n = 1…7`.
* The normalised values `g₃(n)·√n/3ⁿ = 0.543, 0.552, 0.565, 0.573` (n = 4…7), and the new upper bounds
  (≤ 0.590, 0.606, 0.620, 0.638, 0.655 for n = 8…12), are data for the open question of the true order of
  `g₃(n)` between `c·3ⁿ/√n` (lower bound) and `O(3ⁿ/n^{1/3})` (best upper bound).
* The chain structure gives a fast, apparently near-optimal construction for larger `n`, a ternary analogue
  of the Conway–Guy construction for distinct subset sums.

Full table: `scripts/summary_table.py`.

## Exact evidence for g₃(7) = 474

1. **Upper bound (certificate).** For `A = {302, 409, 447, 459, 465, 466, 474}` all `3⁷ = 2187` sums
   `Σ εᵢaᵢ` (`εᵢ ∈ {0,1,2}`) are distinct, and the 128 subset sums contain no 3-term AP. Both are checked
   directly with exact integer arithmetic (`verify/check_set.py`; sorted sum lists and SHA-256 hashes in
   `results/certificates/`). This half does not depend on any reformulation.
2. **Lower bound (exhaustive search).** For every `N ≤ 473` there is no admissible 7-subset of `[1, N]` with
   maximum `N`:
   * `N = 419 … 473`: the C search (`src/g3fast2.c -DNOROOM`, `results/n7_scan/`) and the independent Rust
     search (`verify/g3verify_rs`, `results/n7_verify_rust_hi/`) agree on the full canonical count vector
     `(V₁(N), …, V₇(N))` for every `N`; `V₇(N) = 0` throughout;
   * `N ≤ 418`: excluded by Korsky's theorem, and additionally by exhaustive search (`results/n7_c_lo/`).
3. **Uniqueness.** At `N = 474` both programs enumerate all admissible 7-sets with maximum 474 and find
   exactly one.

Canonical counts: `V_k(N)` = number of admissible `k`-subsets of `[1, N]` containing `N`. Examples:
`V₆(473) = 6,608,257,434`, `V₇(473) = 0`; `V₆(474) = 6,271,320,297`, `V₇(474) = 1`. Over `N = 419…473`
the search examined 207,290,610,257 admissible 6-sets and 49,173,696,632 admissible 5-sets; none extends.

## How it can be falsified

* Exhibit a 7-set with maximum `< 474` whose 2187 ternary sums are distinct (checkable in milliseconds with
  `verify/check_set.py`), or a second admissible 7-set with maximum 474.
* Produce, with any correct implementation, a different canonical count vector `V_k(N)` for any `N` in
  `results/n7_counts.csv`. The counts do not depend on search order, so any disagreement pinpoints an error.

## Independent verification performed

| check | what it establishes |
| --- | --- |
| Proof of Lemma 1 (METHODS.md) + `bruteforce.py --equivalence` (0 mismatches) | reformulation to `{0,1,2}`-injectivity |
| `bruteforce.py` (definition only) = Rust verifier, n = 4…7 small N | both match the raw definition |
| `gk_search.c` (definition only: subset-sum bitsets + 3-AP test) = C, n = 5 (N ≤ 62) and n = 6 at N = 167, 168 | reformulation + fast code agree with the definition at the n = 6 optimum |
| C = Rust canonical counts and solution lists, n = 4…7 (N ≤ 40 / 90 / 175 / 150) | implementations agree where cheap |
| Mutation testing (5 injected bugs, all detected at n = 6) | the cross-check is sensitive |
| **C = Rust, n = 7, N = 419…478** (full count vectors and solution lists) | **main claim, two independent programs** |
| C, n = 7, N = 1…418 | removes dependence on Korsky's bound |
| Conway–Guy-type ternary recurrences (all `u_{n+1} = 3u_n − u_{n−r}`) | no construction of this family beats 474 (none below 543) |

## Remaining uncertainty

See LIMITATIONS.md. The non-existence part is a computer-assisted exhaustive search without a compact proof
object. It is supported by two independently written programs that agree on count vectors of order 10⁹–10¹⁰
for every N, plus agreement with definition-level brute force on smaller instances.

## VERIFICATION STATUS

| range of N | C (`g3fast2 -DNOROOM`) | Rust (`g3verify`) | comparison |
| --- | --- | --- | --- |
| 419 … 478 | complete (`results/n7_scan/`) | complete (`results/n7_verify_rust_hi/`) | identical count vectors and solution lists (`scripts/aggregate.py compare`) |
| 1 … 418 | complete (`results/n7_c_lo/`), no admissible 7-set | see `results/n7_verify_rust_lo/` | see research_log.md (final entry) |
| band check 474 … 520 (elements ≥ 0.55 N) | `results/n7_band_crosscheck/c_band.log` | `rust_band.log` | identical solution lists |

Solutions found by both programs for N = 474…478: N = 474: {302,409,447,459,465,466,474}; N = 475:
{307,414,452,466,469,473,475}; N = 476: none; N = 477: {308,417,455,469,474,476,477},
{309,416,454,468,471,473,477}; N = 478: none.
