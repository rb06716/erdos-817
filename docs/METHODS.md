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
  the even-position read is done with the BMI2 `PEXT` instruction (or an equivalent portable shift-and-mask
  routine when BMI2 is unavailable or `-DNO_PEXT` is set; identical results).
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
* **Observed profile.** One extremal set for each n = 4…7, divided by its maximum (the other n = 6 set fits the
  same profile; the other n = 4 and n = 5 sets, {7,19,21,22} and {19,52,57,59,60}, have smallest element
  ≈ 0.32·max):
  `{14,19,21,22}/22 = .636 .864 .955 1`; `{38,52,57,59,60}/60 = .633 .867 .950 .983 1`;
  `{107,145,159,162,164,168}/168 = .637 .863 .946 .964 .976 1`;
  `{302,409,447,459,465,466,474}/474 = .637 .863 .943 .968 .981 .983 1`.
  Windows `600:700 830:900 920:970` plus `940:1000` for the rest reproduce the n = 6, 7 extremal sets in
  well under a second. For n = 8, a coarse stop-at-first scan (M = 1420, 1400, 1380, …) first found a set with
  maximum 1380; a full enumeration inside the windows later found none for M = 1361…1367 and exactly one for
  M = 1368, the hole-chain set of §8 (`results/n8_upper/profile8_*.log`).
* **Offset form (explains the profile).** Write `A = {M} ∪ {M − b : b ∈ B}`. A relation
  `Σ cᵢaᵢ = 0` becomes `M·s = Σ_{b∈B} c_b b` with `s = c_M + Σ c_b`. Hence `A` is admissible iff
  (i) `B` has no relation `Σ c_b b = 0` with `c ∈ {−2..2}^B \ {0}` and `|Σ c_b| ≤ 2` (the `s = 0` case, the
  coefficient of `M` absorbing the imbalance), and (ii) for `s = 1, 2, …`: `sM ∉ {Σ c_b b : s − 2 ≤ Σ c_b ≤ s + 2}`
  (negative `s` give the same conditions under `c ↦ −c`).
  In particular, if `B` satisfies (i) then `A` is admissible for every `M > 2ΣB`. All known extremal sets have
  `ΣB < M` (≈ 0.6·M on the profile above, e.g. n = 7: `B = {8, 9, 15, 27, 65, 172}`, `ΣB = 296`, `M = 474`;
  0.86·M and 0.88·M for {7,19,21,22} and {19,52,57,59,60}), so only `s = ±1` matters and `M` is the first
  "hole" of the set in (ii) above `max B`.

## 8. Hole chains (constructions; `scripts/holes_all.py`, `scripts/beam.py`, `scripts/hole_dp.py`)

The offset form of the small optima was first noted by M. Czech (Erdős Problems forum, thread #817, 9 Sep
2026): for n ≤ 5 an optimal set is `{G_n − G_k}` with `G = 0, 1, 3, 8, 22, 60`, as for the Conway–Guy sets. The
chains below generalise this.

For a finite set `B` of positive integers call `M > max B` a **hole** of `B` if
`A = {M} ∪ {M − b : b ∈ B}` is admissible. By §7, `M` is a hole iff `B` satisfies condition (i) and
`sM ∉ F_s(B) = {Σ c_b b : c ∈ {−2..2}^B, s−2 ≤ Σ c_b ≤ s+2}` for every `s ≥ 1`. Every `M > 2ΣB` is a hole
when (i) holds. `hole_dp.py` computes the sets `E_t = {Σ c_b b : Σ c_b = t}` by dynamic programming
(bitsets indexed by `(t, value)`), tests (i) incrementally (a new element `x` violates (i) iff
`c·x ∈ ⋃_{t ∈ [c−2, c+2]} E_t` for `c ∈ {1, 2}`), and lists all holes up to `2ΣB + 1`.

**Lemma 3 (the chain never gets stuck).** If `M` is a hole of `B`, then `B ∪ {M}` satisfies condition (i);
hence `B ∪ {M}` has holes (every integer `> 2(ΣB + M)`).

*Proof.* A violation is a nonzero `c` on `B ∪ {M}` with `c_M M + Σ c_b b = 0` and `|c_M + Σ c_b| ≤ 2`.
If `c_M = 0` it violates (i) for `B`, which is impossible because `M` is a hole. Otherwise put
`c_0 = −(c_M + Σ c_b) ∈ [−2, 2]`. Then `c_0 M + Σ c_b (M − b) = M(c_0 + Σ c_b) − Σ c_b b = −c_M M − Σ c_b b = 0`
is a relation on `A = {M} ∪ (M − B)`. It is nonzero, since `c_b ≡ 0` would force `c_M M = 0`, i.e. `c_M = 0`.
This contradicts admissibility of `A`. ∎

A **hole chain** is `0 = u_0 < u_1 < … < u_n` where each `u_{k+1}` is a hole of `{u_1,…,u_k}`. It yields the
admissible `n`-set `{u_n − u_i : 0 ≤ i < n}`. The *greedy* chain takes the least hole each time.
`beam.py W K NMAX S0` keeps the `W` chains with the smallest current maximum, extends each by its first `K`
holes, and starts from all seeds `u_1 ≤ S0`. Chains are a restricted family (87–95 % of admissible sets near
the optimum for n = 5, 6 are chains), so beam results are upper bounds. For n ≤ 7 they coincide with the
exhaustively verified optima.
