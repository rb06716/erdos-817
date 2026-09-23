# Methods

## 1. The quantity being computed

Erdős Problem #817 (Erdős 1991; Erdős–Sárközy 1992). For a finite set `A` of positive integers let

    H(A) = { sum_{a in S} a : S ⊆ A }            (the set of subset sums)

and let `g_3(n)` be the least `N` such that some `n`-element `A ⊆ {1,…,N}` has `H(A)` free of
non-constant 3-term arithmetic progressions (`u < v < w`, `u + w = 2v`). OEIS A399720 lists
`g_3(1..6) = 1, 3, 8, 22, 60, 168`.

## 2. Reformulation (proved here; also Korsky 2026, Prop. 4.1)

**Lemma 1.** For a set `A = {a_1,…,a_n}` of positive integers the following are equivalent:

1. `H(A)` contains no non-constant 3-term AP;
2. there is no non-zero `δ ∈ {−2,−1,0,1,2}^n` with `Σ δ_i a_i = 0`;
3. the map `ε ↦ Σ ε_i a_i` is injective on `{0,1,2}^n`.

*Proof.* (2)⇔(3): `ε ≠ ε'` collide iff `δ = ε − ε'` is a non-zero relation, and every
`δ ∈ {−2..2}^n` is such a difference.

(1)⇒(2) by contraposition. Let `δ ≠ 0` with `Σ δ_i a_i = 0`.
*Case A: some `δ_i` is odd.* For every coordinate pick `(s_u, s_w, s_v) ∈ {0,1}^3` with
`s_u + s_w − 2 s_v = δ_i`: `δ_i = 2 → (1,1,0)`, `1 → (1,0,0)`, `0 → (0,0,0)`, `−1 → (1,0,1)`,
`−2 → (0,0,1)`. With `S_u, S_w, S_v` the resulting index sets and `u, w, v` their sums,
`u + w − 2v = Σ δ_i a_i = 0`. At odd coordinates `s_u − s_w = 1`, elsewhere `0`, so
`u − w = Σ_{δ_i odd} a_i > 0`: the progression `w < v < u` is non-constant.
*Case B: all `δ_i` even.* Then `δ = 2δ'` with `δ' ∈ {−1,0,1}^n \ {0}` and `Σ δ'_i a_i = 0`:
the disjoint non-empty sets `P = {δ'_i = 1}` and `M = {δ'_i = −1}` have equal sums `X > 0`, and
`0, X, 2X` (sums of `∅`, `P`, `P ∪ M`) is a non-constant 3-AP in `H(A)`.

(2)⇒(1). If `u + w = 2v` with `u = Σ_{S_u}`, `w = Σ_{S_w}`, `v = Σ_{S_v}`, then
`δ = 1_{S_u} + 1_{S_w} − 2·1_{S_v} ∈ {−2..2}^n` satisfies `Σ δ_i a_i = 0`. If `δ = 0` then
`1_{S_u} + 1_{S_w} = 2·1_{S_v}` forces `S_u = S_w = S_v`, i.e. a constant progression. ∎

`verify/bruteforce.py --equivalence` re-checks Lemma 1 numerically (all subsets of `[1,14]` of size ≤ 4 and
3000 random sets): 0 mismatches. `verify/bruteforce.py` works *only* from definition (1).

Call `A` **admissible** when it satisfies Lemma 1. Admissibility is hereditary (subsets of admissible
sets are admissible), and `g_3(n) = min{ max A : A admissible, |A| = n }`.

## 3. The one-step extension lemma

For a finite set `B` define the symmetric set `D_B = { Σ_{b∈B} c_b b : c ∈ {−2..2}^B }`.

**Lemma 2.** If `B` is admissible and `x ∉ B` is a positive integer, then `B ∪ {x}` is admissible iff
`x ∉ D_B` and `2x ∉ D_B`. Moreover `D_{B∪{x}} = D_B + {0, ±x, ±2x}`.

*Proof.* A relation on `B ∪ {x}` with `c_x = 0` is a relation on `B`. With `c_x ∈ {±1, ±2}` it reads
`c_x x = −Σ c_b b ∈ D_B`; since `D_B = −D_B`, this happens iff `x ∈ D_B` or `2x ∈ D_B`. The second
statement is the definition of `D`. ∎

## 4. Exhaustive search (`src/g3fast2.c`)

For each `N` the program enumerates **all** admissible `n`-sets with maximum exactly `N`:

* `N` is placed first (`D_1 = {0, ±N, ±2N}`), then the remaining elements `b_1 < b_2 < … < b_{n−1} < N`
  are added in increasing order. By Lemma 2 each step only needs two bit look-ups in the bitset `D_L`.
  Because admissibility is hereditary, every admissible set with maximum `N` is reached along exactly one
  path (its elements sorted), so the enumeration is complete.
* **Candidate scan.** The legal next elements in a window `[s, s+ℓ)` are `~(D[s..s+ℓ) | D[2s, 2s+2, …])`;
  the even-position read is done with the BMI2 `PEXT` instruction.
* **Last two levels.** With `D_{n−2}` known and the `(n−1)`-th element `y` accepted, the last element `x`
  must satisfy `x − jy ∉ D_{n−2}` and `2x − jy ∉ D_{n−2}` for `j ∈ {−2..2}` (because
  `D_{n−1} = D_{n−2} + {0, ±y, ±2y}`), which is evaluated with five shifted word windows instead of
  materialising `D_{n−1}`.
* **Windowing.** `D_L` is only materialised on positions that can still be read: level `n−2` is read
  at positions in `[−N, 4N]`, and computing level `L+1` on `[lo, hi]` needs level `L` on
  `[lo − 2N, hi + 2N]`; the true support `[−2Σ, 2Σ]` is also used. Everything outside is kept zero.
* **Window invariant (why windowing is exact).** Let `[λ_L, ρ_L]` be the needed range of level `L`
  (`[−N, 4N]` for `L = n−2`, widened by `2N` on both sides per level upward). *Claim:* every stored bit of
  level `L` at a position `p ∈ [λ_L, ρ_L]` equals the true `D_L(p)`. *Induction:* level 1 is computed from
  level 0 = `{0}`, which is exact everywhere. For level `L+1` and `p ∈ [λ_{L+1}, ρ_{L+1}]`: if `|p|` exceeds
  the true support bound `2Σ_{L+1}`, the word is either zeroed or computed from source bits that are all
  zero, and indeed `D_{L+1}(p) = 0`; otherwise the bit is computed from source positions `p ± a, p ± 2a`,
  which lie in `[λ_L, ρ_L]` because `a < N`, hence are exact. The last level reads only positions
  `x − jy ∈ [−N, 3N]` and `2x − jy ∈ [2, 4N−4]` (for `y < x < N`, `|j| ≤ 2`) and candidate positions in
  `[1, 2N]`, all inside `[λ_{n−2}, ρ_{n−2}] = [−N, 4N]`.
* **Modes.** Default: "room" pruning (the next element must leave space for the remaining ones).
  `-DNOROOM`: no room pruning, so the per-depth node counts are the canonical numbers
  `V_k(N) = #{admissible k-subsets of [1..N] containing N}` (k = 1..n), which do not depend on the search
  order. All reported production runs use `-DNOROOM`.

The simpler reference implementation `src/g3search.c` (no PEXT, full-range bitsets) produces identical node
counts to `g3fast2.c` on every tested case.

## 5. Independent verification (`verify/g3verify_rs`, Rust)

Written separately, with deliberately different design decisions:

* elements are added in **decreasing** order (maximum first);
* difference sets stored on symmetric windows `[−r_L, r_L]`, no PEXT, word-level scan of the zero bits of `D`;
* last level evaluated from `D_{n−2}` with its own chunked-window code;
* no room pruning: it reports the canonical counts `V_k(N)` for every `N`.

Agreement criterion: for every `N` checked, the full vector `(V_1(N), …, V_7(N))` and the list of
admissible sets with maximum `N` must be identical between the C and the Rust program.

A third, definition-level check (`verify/bruteforce.py`) enumerates all subsets and tests 3-AP-freeness of
`H(A)` directly; it is only feasible for small `N` and is used to validate both fast programs.

## 6. Upper-bound certificates

An admissible set is certified by `verify/check_set.py`, which (a) enumerates all `3^n` sums and checks
they are distinct, and (b) enumerates all `2^n` subset sums and checks directly that there is no 3-term AP.
Both are exact integer computations.

## 7. Upper-bound constructions (not used for any lower bound)

* **Band / profile search** (`g3fast2 … minelem`, `src/g3profile.c`): the same exhaustive DFS restricted to
  sets whose non-maximal elements lie in prescribed windows (per mille of the maximum). It is complete
  *within the windows* only, so it can certify existence but never non-existence.
* **Observed profile.** The extremal sets for n = 4…7, divided by their maximum:
  `{14,19,21,22}/22 = .636 .864 .955 1`; `{38,52,57,59,60}/60 = .633 .867 .950 .983 1`;
  `{107,145,159,162,164,168}/168 = .637 .863 .946 .964 .976 1`;
  `{302,409,447,459,465,466,474}/474 = .637 .863 .943 .968 .981 .983 1`.
  Windows `600:700 830:900 920:970` plus `940:1000` for the rest reproduce the n = 6, 7 extremal sets in
  well under a second and give the n = 8 construction with maximum 1380.
* **Offset form (explains the profile).** Write `A = {M} ∪ {M − b : b ∈ B}`. A relation
  `Σ cᵢaᵢ = 0` becomes `M·s = Σ_{b∈B} c_b b` with `s = c_M + Σ c_b`. Hence `A` is admissible iff
  (i) `B` has no relation `Σ c_b b = 0` with `c ∈ {−2..2}^B \ {0}` and `|Σ c_b| ≤ 2` (the `s = 0` case, the
  coefficient of `M` absorbing the imbalance), and (ii) for `s = 1, 2, …`: `sM ∉ {Σ c_b b : s − 2 ≤ Σ c_b ≤ s + 2}`.
  In particular, if `B` satisfies (i) then `A` is admissible for every `M > 2ΣB`. The extremal sets have
  `B` of total size ≈ 0.6·M (e.g. n = 7: `B = {8, 9, 15, 27, 65, 172}`, `ΣB = 296`, `M = 474`), so only
  `s = ±1` matters and `M` is the first "hole" of the set in (ii) above `max B`.
