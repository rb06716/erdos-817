# Discovery: the Erdős–Sárközy function satisfies g₃(7) = 474

## The discovery in one sentence

The least `N` for which some 7-element subset of `{1,…,N}` has subset sums containing no non-constant
3-term arithmetic progression is **`g₃(7) = 474`**, and the extremal set is **unique**:
**`A = {302, 409, 447, 459, 465, 466, 474}`**.

Context: Erdős Problem #817; OEIS A399720 currently lists `a(1..6) = 1, 3, 8, 22, 60, 168` and states
`419 ≤ a(7) ≤ 504`.

**Credit for the upper bound.** The same set was found independently by carlomitchener and posted as
`g₃(7) ≤ 474` in the Erdős Problems forum thread #817 on 23 Sep 2026 (06:41 forum time). This package's
search had found it at 00:20 UTC that day, but its repository was private, so **the forum post is the first
public report of the upper bound**. As far as we can find, this package's own new contributions are:
* the matching lower bound, i.e. no admissible 7-set with maximum ≤ 473;
* uniqueness of the extremal set;
* hence the exact value.

This problem is not solved here. Erdős Problem #817 asks for an *estimate* of `g_k(n)`, which "cannot be
resolved with a finite computation" (erdosproblems.com). Exact small values are data for it, not a solution.

## Statement as a theorem

**Theorem 1.** `g₃(7) = 474`. Moreover `A* = {302, 409, 447, 459, 465, 466, 474}` is the only 7-element subset
of `{1,…,474}` whose subset sums contain no non-constant 3-term arithmetic progression.

*Proof (computer-assisted).*
* *Upper bound, `g₃(7) ≤ 474`.* The `3⁷ = 2187` sums `Σ εᵢaᵢ` with `ε ∈ {0,1,2}⁷` over the elements of `A*` are
  pairwise distinct, so `H(A*)` has no non-constant 3-AP by Lemma 1 (METHODS.md §2). `verify/check_set.py`
  checks this with exact integer arithmetic. It also checks the definition directly: the 128 subset sums
  contain no 3-AP. This half is a certificate that anyone can check in milliseconds.
* *Lower bound and uniqueness.* By Lemma 1 a 7-set qualifies iff it is admissible. For every `N ≤ 474` the
  search enumerates all admissible 7-subsets of `[1, N]` with maximum `N`.
  * *Why the enumeration is complete:* admissibility is hereditary, so every admissible set is reached by
    adding its elements one at a time in sorted order. Lemma 2 (§3) decides each step exactly, and the
    window invariant (§4) shows that the bitset windowing is exact.
  * *Result:* there is no admissible 7-set for `N ≤ 473`, and exactly one, `A*`, for `N = 474`. ∎

The second half has no short human-readable proof. Its correctness rests on Lemmas 1 and 2, which are proved
by hand in METHODS.md, and on the search programs. Two independently written implementations ran the search
(C, increasing order; Rust, decreasing order). They report identical canonical count vectors
`(V₁(N), …, V₇(N))` and identical solution lists for every `N ≤ 478`. The evidence and the checks are listed
below.

**Also proved in this package:**
* **By certificates** (fully rigorous): `g₃(n) ≤ 1368, 3974, 11578, 34088, 100422, 295924, 879824` for
  `n = 8, …, 14`.
* **Computer-assisted, two programs:** `g₄(6) = 79`, `g₄(7) = 225`, `g₅(7) = 60`, `g₅(8) = 92` (item 3 below).

**Not proved (conjectures):**
* `g₃(8) = 1368`;
* the claim that extremal sets are hole chains for all `n` (verified for `n ≤ 7`).

## Secondary results (same package, weaker status where noted)

1. **New upper bounds** (explicit, certified sets). The previous best was `(168/729)·3ⁿ`, or `(474/2187)·3ⁿ`
   from the upper bound `g₃(7) ≤ 474` (as also noted in carlomitchener's forum post):

   | n | 8 | 9 | 10 | 11 | 12 | 13 | 14 |
   | --- | --- | --- | --- | --- | --- | --- | --- |
   | new bound | **1368** | **3974** | **11578** | **34088** | **100422** | **295924** | **879824** |
   | previous (168/729)·3ⁿ | 1512 | 4536 | 13608 | 40824 | 122472 | 367416 | 1102248 |

   All are of the form `A_n = {u_n − u_i : 0 ≤ i < n}` with
   `u = (0, 8, 9, 15, 27, 65, 172, 474, 1368, 3974, 11578, 34088, 100422, 295924, 879824)`, where from
   `u_4 = 27` on every term is the least admissible "hole". All are certified by `verify/check_set.py`
   (e.g. n = 14: all 4,782,969 ternary sums distinct, and the 16,384 subset sums contain no 3-AP).

   **Conjecture: g₃(8) = 1368.** Evidence (not a proof): (a) a beam search over hole chains up to width 20,000
   finds nothing below 1368; (b) an exhaustive search over *all* admissible 8-sets whose elements lie in the
   windows observed for every known optimum (per mille of the maximum: 600–700, 830–900, 920–970, then
   940–1000) finds none with maximum 1300, 1301, 1320, 1340 or 1360–1367, and exactly one with maximum 1368:
   the set above (`results/n8_upper/profile8_*.log`).
2. **Structure ("hole chains").** Every extremal set for `n = 4, 5, 6, 7` (two each for n = 4, 5, 6; the unique
   one for n = 7) has the form `{u_n − u_i}` where each `u_{k+1}` is an admissible "hole" for
   `{u_1,…,u_k}` (i.e. `{u_{k+1} − u_i : i ≤ k}` is itself admissible). A beam search restricted to such chains
   (`scripts/beam.py`, seconds) reproduces **every** known exact value `8, 22, 60, 168, 474` together with
   the extremal sets, and gives the n = 8–14 bounds above. Chains are common but not universal (87–95 % of
   admissible sets near the optimum for n = 5, 6), so for `n ≥ 8` these are upper bounds, not claimed optima.
3. **The 4- and 5-term analogues** from the same Erdős problem. There are no OEIS entries (full-text search of the
   export and live OEIS searches, 2026-09-23). Korsky's paper, read in full, gives small values only for `g₃`
   with `n ≤ 4`, and the forum thread #817 gives none for `k ≥ 4`:
   `g₄(1..7) = 1, 3, 5, 14, 40, 79, 225` (unique extremal set `{2, 29, 45, 74, 77, 79}` at n = 6);
   `g₅(1..8) = 1, 2, 4, 6, 14, 22, 60, 92` (unique extremal set `{10, 11, 67, 77, 78, 81, 82, 92}` at n = 8).
   * **`g₄(7) = 225`** has exactly six extremal sets. All six contain `90, 135, 225` (note `90 + 135 = 225`)
     and have 98 distinct subset sums:
     `{2,90,135,193,220,222,225}`, `{4,90,135,206,215,219,225}`, `{7,90,135,202,213,220,225}`,
     `{14,90,135,201,215,224,225}`, `{16,90,135,204,211,220,225}`, `{17,90,135,205,222,223,225}`.
   * **How it was checked:** `verify/gk_verify.c` enumerated every N = 1…225. `src/gk_search.c` covers
     N = 80…224; below 80, `g₄(6) = 79` rules out any 7-set. The two programs have identical count vectors
     on all 145 shared values of N. Both find nothing for N ≤ 224. At N = 225 both enumerated everything
     and list the same six sets, with identical count vectors. Each set is also checked directly against
     the definition. Files: `results/gk/g4_n7_verify/`, summary in `compare_output.txt`.
   * **Other exact values:** two independent programs (`src/gk_search.c`, `verify/gk_verify.c`) agree on
     all canonical counts (for g₅(8): all N ≤ 92). A Python brute force also confirms n ≤ 5 (k = 4) and
     n ≤ 6 (k = 5).
4. **A correction to an earlier claim (n = 6).** Bae and Choi (J. Korean Math. Soc. 40 (2003) 757–768, §2,
   p. 759) study "2-fold subset-sum-distinct" sets, which are exactly the admissible sets. They state that
   "lots of calculations" show `{109, 147, 161, 166, 168, 169}` to be the unique such 6-set of minimal
   height, which would mean `g₃(6) = 169`. **This is incorrect.**
   * **The true value:** `g₃(6) = 168`, attained by `{107,145,159,162,164,168}` and `{107,145,159,162,166,168}`.
     OEIS A399720 lists the second of these.
   * **Their set:** it is the unique admissible 6-set with maximum exactly 169. It is the greedy "first-hole"
     chain set `{169 − u_i}` with `u = 0, 1, 3, 8, 22, 60, 169`.
   * **Reproduce:** `./bin/g3fast2_noroom 6 168 169`; output in `results/prior_art/bae_choi_n6_check.txt`.
   * **n = 7:** they give no value.

## Why it appears novel

* **OEIS A399720** (created 2026-09-09, last edited 2026-09-14) gives only `419 ≤ a(7) ≤ 504` and remarks
  that `a(7) = 466` "is not excluded". Checked in the git exports of 2026-09-22 and 2026-09-23 and on the live
  site on the afternoon of 2026-09-23.
* **Erdős Problems forum thread #817** (read directly on 2026-09-23):
  * M. Czech (9 Sep) gives `g₃(5) = 60`, `g₃(6) = 168` and `419 ≤ g₃(7) ≤ 504`, and says `n = 7` is beyond
    their search.
  * carlomitchener (23 Sep) posts the upper bound `g₃(7) ≤ 474` with the same set (see "Credit" above).
  * No post gives a lower bound above 419, the exact value, or uniqueness.
* **The verification repository** `firesh/erdos817-subset-sum-progressions-audit` (2026-09-18) computed
  `g₃(5), g₃(6)` and reports its `n = 7` search as incomplete (only `N ≤ 313` excluded), listing `g₃(7)` as open.
* **Korsky** (arXiv:2606.24139, June 2026; read in full) proves `g₃(7) ≥ b₇ = 419` and computes `g₃(n)`
  only for `n ≤ 4`.
* **Bae–Choi (2003)** is the only earlier source found with an exact minimum for these sets. It covers only
  n = 6, and its value there is wrong (item 4 above).
* **Nothing else** reports the exact value, the lower bound, uniqueness or the chain sequence. Sources
  searched: the OEIS (full-text search of all 399,527 entries, plus live searches), arXiv, the forum and the
  web. Details: PRIOR_ART.md.

## Why it matters

* **The next exact value.** It is the next exact value of a function asked about by Erdős and Sárközy.
  * Their "in particular" question, whether `g₃(n) ≫ 3ⁿ`, was answered negatively only this month (Costa,
    arXiv:2609.06303). Together with monotonicity this gives `g₃(n)/3ⁿ → 0`.
  * erdosproblems.com lists Costa's result as a *partial* proof claim, because the problem asks for an
    estimate. The true order of `g₃(n)` remains open.
  * Exact small values are the only ground truth for calibrating constructions and bounds.
* **The 466 question.** It settles the question left open in the OEIS entry and the forum thread:
  `a(7) ≠ 466`. So the coincidence of `1, 3, 8, 22, 60, 168` with the rooted-tree sequences
  A318821/A318863, which continue with 466, ends here. Only the lower bound can show this.
* **504 is not optimal.** It also shows `a(7) < 504 = 3·a(6)`: the recursive construction `A ↦ {1} ∪ 3A` is
  not optimal at n = 7. The forum post of the upper bound shows this too.
* The gap to Korsky's bandwidth lower bound grows: `g₃(n) − b_n = 0, 0, 0, 1, 4, 16, 55` for `n = 1…7`.
* The normalised values `g₃(n)·√n/3ⁿ = 0.543, 0.552, 0.565, 0.573` (n = 4…7), and the new upper bounds
  (≤ 0.590, 0.606, 0.620, 0.638, 0.655 for n = 8…12), are data for the open question of the true order of
  `g₃(n)` between `c·3ⁿ/√n` (lower bound, Korsky) and `O(3ⁿ/n^{1/3})` (best upper bound, posted on the forum by
  Costa on 17 Sep 2026, adapting B. Alexeev's construction for Erdős Problem #1).
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
   * `N ≤ 418`: excluded by Korsky's theorem, and independently by both exhaustive searches
     (`results/n7_c_lo/`, `results/n7_verify_rust_lo/`, identical count vectors), so the result does not
     depend on that theorem.
3. **Uniqueness.** At `N = 474` both programs enumerate all admissible 7-sets with maximum 474 and find
   exactly one.

Canonical counts: `V_k(N)` = number of admissible `k`-subsets of `[1, N]` containing `N`. Examples:
`V₆(473) = 6,608,257,434`, `V₇(473) = 0`; `V₆(474) = 6,271,320,297`, `V₇(474) = 1`. Over `N = 419…473`
the search examined 207,290,610,257 admissible 6-sets and 49,173,696,632 admissible 5-sets (over all
`N ≤ 473`: 274,105,685,447 and 95,595,217,293); none extends to an admissible 7-set.

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
| Band check, n = 7, N = 474…520: 12,010 solutions, identical in C and Rust | last search level correct where solutions exist |
| Reference program `g3search.c` (no windowing/PEXT) at N = 473, 474: output identical to `g3fast2` (same mode), incl. the unique set | windowing and PEXT logic of the main program |
| Third-party `g3.c` (firesh audit repository, different author): no admissible 7-subset of [1..200] | agreement with an externally written program where it is fast enough |
| Run by the repository owner (a human) on different hardware: `verify_result.py quick` in Google Colab (Intel, 8 vCPUs), 2026-09-23: 7/7 PASS (`results/external_verification/`) | reproducibility on another machine, run by a human: certificates, Lemma 1 test, g₃(5), g₃(6), and the exact count vectors at N = 473, 474 (same code, so this guards against environment and hardware errors, not against a shared logic error) |
| Independent external find: carlomitchener (forum thread #817, 23 Sep 2026) posted the same set as `g₃(7) ≤ 474`, checked from the definition | external confirmation of the certificate; consistent with uniqueness (any admissible 7-set with maximum 474 must be this one) |
| **C = Rust, n = 7, N = 419…478** (full count vectors and solution lists) | **main claim, two independent programs** |
| **C = Rust, n = 7, N = 1…418** | removes dependence on Korsky's bound |
| Conway–Guy-type ternary recurrences (all `u_{n+1} = 3u_n − u_{n−r}`) | no construction of this family beats 474 (none below 543) |

## Remaining uncertainty

See LIMITATIONS.md. The non-existence part is a computer-assisted exhaustive search without a compact proof
object. It is supported by two independently written programs that agree on count vectors of order 10⁹–10¹⁰
for every N, plus agreement with definition-level brute force on smaller instances.

## VERIFICATION STATUS

| range of N | C (`g3fast2 -DNOROOM`) | Rust (`g3verify`) | comparison |
| --- | --- | --- | --- |
| 419 … 478 | complete (`results/n7_scan/`) | complete (`results/n7_verify_rust_hi/`) | identical count vectors and solution lists (60 values, 0 mismatches) |
| 1 … 418 | complete (`results/n7_c_lo/`) | complete (`results/n7_verify_rust_lo/`) | identical count vectors; no admissible 7-set |
| band check 474 … 520 (other elements ≥ 0.55 N) | `results/n7_band_crosscheck/c_band.log` | `rust_band.log` | identical solution lists: 47 values of N, 12,010 admissible 7-sets, 0 mismatches (exercises the last search level of both programs) |

**Result of `scripts/finalize.sh`:** 478 values of N compared, 0 mismatches; the first N with an admissible
7-set is 474. `results/n7_counts.csv` (SHA-256 `e54df8b158490ee84f3932d449caec038681f979db50d1c953af4ed5de0e6369`)
holds the canonical counts for N = 1…478. Over N = 1…473 each program enumerated 274,105,685,447 admissible 6-sets
and 95,595,217,293 admissible 5-sets, none of which extends to an admissible 7-set. Total cost: C 4.0 CPU-hours,
Rust about 2.5× that (2.1 GHz Xeon cores).

Solutions found by both programs for N = 474…478: N = 474: {302,409,447,459,465,466,474}; N = 475:
{307,414,452,466,469,473,475}; N = 476: none; N = 477: {308,417,455,469,474,476,477},
{309,416,454,468,471,473,477}; N = 478: none.
