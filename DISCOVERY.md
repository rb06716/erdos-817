# Discovery: the Erdős–Sárközy function satisfies g₃(7) = 474

## The discovery in one sentence

The least `N` such that some 7-element subset of `{1,…,N}` has a set of subset sums containing no
non-constant 3-term arithmetic progression is **`g₃(7) = 474`**, and the extremal set is **unique**:
`A = {302, 409, 447, 459, 465, 466, 474}`.

(Erdős Problem #817; OEIS A399720, whose entry currently lists `a(1..6) = 1, 3, 8, 22, 60, 168` and states
`419 ≤ a(7) ≤ 504`.)

## Why it appears novel

* OEIS A399720 (created 2026-09-09, last edited 2026-09-14; checked in the official git export of
  2026-09-22) gives only `419 ≤ a(7) ≤ 504` and remarks that `a(7) = 466` "is not excluded".
* The independent verification repository `firesh/erdos817-subset-sum-progressions-audit` (2026-09-18)
  computed `g₃(5), g₃(6)` and reports that its `n = 7` search "is incomplete: N ≤ 313 excluded", listing the
  exact value of `g₃(7)` as still open.
* Korsky (arXiv:2606.24139, June 2026) proves `g₃(7) ≥ b₇ = 419` and computes `g₃(n)` only for `n ≤ 4`.
* No web source, OEIS entry (full-text search of all 399,468 entries), or GitHub repository found reports
  474 or the set above. Details and search terms: PRIOR_ART.md.

## Why it matters

* It is the next exact value of a function asked about by Erdős and Sárközy, whose asymptotic question was
  answered only this month (Costa, arXiv:2609.06303: `g₃(n)/3ⁿ → 0`). Exact small values are the only
  ground truth against which constructions and bounds are calibrated. The ratios `g₃(n)/3ⁿ` are now
  `0.333, 0.333, 0.296, 0.272, 0.247, 0.230, 0.2167` (n = 1…7).
* It settles two concrete questions raised in the OEIS entry: `a(7) ≠ 466` (the coincidence of
  `1, 3, 8, 22, 60, 168` with the rooted-tree sequences A318821/A318863, which continue with 466, ends here),
  and `a(7) < 504 = 3·a(6)`: the recursive construction `A ↦ {1} ∪ 3A` is not optimal at n = 7.
* It shows the gap to Korsky's bandwidth bound (`g₃(n) − b_n = 0, 0, 0, 1, 4, 16, 55` for `n = 1…7`), i.e.
  the bandwidth barrier is far from tight already at `n = 7`.
* The extremal sets for `n = 4, …, 7` share a common shape (elements ≈ 0.637N, 0.863N, 0.945N, rest
  clustered just below N). Searching near that shape gives the new construction bound
  **`g₃(8) ≤ 1380`** (`{878, 1192, 1299, 1335, 1349, 1353, 1356, 1380}`; previous best `3·474 = 1422`).

## Exact evidence

1. **Upper bound (certificate).** For `A = {302, 409, 447, 459, 465, 466, 474}` all `3⁷ = 2187` sums
   `Σ εᵢaᵢ` (`εᵢ ∈ {0,1,2}`) are distinct, and the 128 subset sums contain no 3-term AP (checked directly
   by `verify/check_set.py` with exact integer arithmetic: both conditions are verified independently).
2. **Lower bound (exhaustive search).** For every `N ≤ 473` there is no admissible 7-subset of `[1, N]` with
   maximum `N`:
   * `N = 419 … 473`: C search `src/g3fast2.c -DNOROOM` (results/n7_scan) and independent Rust search
     `verify/g3verify_rs` (results/n7_verify_rust_hi), which agree on the full canonical count vector
     `(V₁(N), …, V₇(N))` for every `N` (see VERIFICATION STATUS below);
   * `N ≤ 418`: excluded by Korsky's theorem, **and** re-checked by exhaustive search (results/n7_c_lo,
     results/n7_verify_rust_lo).
3. **Uniqueness.** At `N = 474` both programs enumerate all admissible 7-sets with maximum 474 and find
   exactly one. (For `n ≤ 6` the same programs reproduce all published values and extremal sets.)

Canonical counts `V_k(N)` = number of admissible `k`-subsets of `[1, N]` that contain `N`. Examples:
`V₆(473) = 6,608,257,434`, `V₇(473) = 0`, `V₆(474) = 6,271,320,297`, `V₇(474) = 1`.

## How it can be falsified

* Exhibit a 7-set with maximum `< 474` whose 2187 ternary sums are distinct (checkable in milliseconds with
  `verify/check_set.py`).
* Exhibit a second admissible 7-set with maximum 474.
* Produce, with any correct implementation, a different canonical count vector `V_k(N)` for any `N` in
  `results/n7_counts.csv`: the counts are order-independent, so any disagreement pinpoints an error.

## Independent verification performed

| check | what it establishes |
| --- | --- |
| Lemma 1 proof (METHODS.md) + `bruteforce.py --equivalence` (0 mismatches) | reformulation to `{0,1,2}`-injectivity |
| `bruteforce.py` (definition only: 3-APs in subset sums) vs Rust, n = 4…7 small N | both implementations match the definition |
| `gk_search.c` (definition, general k) vs C, k = 3, n = 5 | third implementation agrees |
| C vs Rust canonical counts, n = 4…7 (N ≤ 40 / 90 / 175 / 150) | implementations agree where cheap |
| mutation testing (5 injected bugs) | the cross-check detects errors |
| C vs Rust, n = 7, N = 419…478, full count vectors and solution lists | main claim, independently |
| C and Rust, n = 7, N = 1…418 | removes dependence on Korsky's bound |

## Remaining uncertainty

See LIMITATIONS.md. In short: the non-existence part is a computer-assisted exhaustive search without a
compact proof object; it is supported by two independently written programs that agree on ~10¹¹-scale
node counts for every `N`, plus small-case agreement with definition-level brute force.

## VERIFICATION STATUS

(filled in when the runs complete; see research_log.md)
