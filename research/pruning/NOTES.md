# Research notes: can pruning make g₃(8) reachable?

Status: exploratory (2026-09-23). Nothing here affects the published results; the programs in this directory are
research prototypes, not built by `make`:
```sh
cc -O3 -march=native -DNOROOM -o research/pruning/g3tail3 research/pruning/g3tail3.c   # usage as g3fast2;
                              # -DNOROOM is required (canonical counts); on Apple clang use -mcpu=native
cc -O3 -o research/pruning/mc_counts research/pruning/mc_counts.c -lm                 # usage: mc_counts k N samples seed
```

## 1. How big is the g₃(8) computation? (calibrated)

To prove g₃(8) = 1368 (the conjectured value), every N = 1169…1367 must be excluded; 1169 = b₈ is Korsky's bound.
The exhaustive search for a fixed N visits every admissible k-set containing N, i.e. `V_k(N)` nodes at level k.

**Estimating the node counts.** `mc_counts.c` estimates `V_k(N)` by Monte Carlo: it samples random k-sets
containing N and tests admissibility exactly. Validation against the exact counts:

| quantity | Monte Carlo | exact |
| --- | --- | --- |
| V₆(473) | 6.57·10⁹ | 6.61·10⁹ |
| V₅(473) | 1.194·10⁹ | 1.195·10⁹ |
| V₆(400) | 1.004·10⁹ | 1.011·10⁹ |

Estimates (2·10⁶ samples each):

| N | V₅(N) | V₆(N) | V₇(N) |
| --- | --- | --- | --- |
| 700 | 6.7·10⁹ | 1.5·10¹¹ | 4.8·10⁸ |
| 1000 | 3.1·10¹⁰ | 1.9·10¹² | 2.7·10¹¹ |
| 1169 | 6.3·10¹⁰ | 5.7·10¹² | 3.6·10¹² |
| 1270 | 8.7·10¹⁰ | 9.0·10¹² | 9.7·10¹² |
| 1367 | 1.2·10¹¹ | 1.5·10¹³ | 3.0·10¹³ |

**Totals and cost.**
* **Per N:** about 1–4.5·10¹³ nodes at levels 6–7.
* **Over all 199 values of N:** about **4·10¹⁵ nodes**.
* **Measured speed:** `g3fast2`, n = 8, runs at about 53–69 ns per node at N = 300–400 (N = 300: 9–10 s for
  1.7·10⁸ nodes; N = 400: 103 s for 1.5·10⁹ nodes). Near N ≈ 1300 we assume 70–100 ns (not measured).
* **CPU cost:** about **9–13 CPU-years** (4·10¹⁵ nodes × 70–100 ns), i.e. 2–3 years on 4 cores.

**Tree shape.** Level 5→6 branches about 100 ways (legal 6th elements), level 6→7 about 1, level 7→8 zero
(for N < g₃(8)). Almost all the work is visiting admissible 6- and 7-sets.

## 2. Ideas examined

1. **Three-level tail** (`g3tail3.c`). The last three elements are chosen from D₅ with shifted windows, so D₆ is
   never materialised.
   * *Correctness:* output identical to `g3fast2 -DNOROOM` for n = 4, 5, 6 at all N ≤ 40/80/180, for n = 7 at
     N = 300, 419, and for n = 8 at N = 300, 400.
   * *Speed:* no gain. n = 8, N = 400: 120 s vs 106 s. n = 7, N = 419: 284 s vs 113 s (pair loop).
   * *Lesson:* the cost per node (about 50–100 ns) is dominated by per-node overhead, not by the bitset width.
     Restructuring gives constant factors of at most about 2×.
2. **All N at once** ("offset form" `a_i = N − u_i`). A relation reads `δ·u = (Σδ)N`, so only the
   `Σδ = 0` part is independent of N. The idea was to search over offset vectors u, keeping a mask of the N
   for which the prefix is still admissible.
   * *Best case:* 199× (one tree instead of 199).
   * *In practice:* at the deep levels, admissibility is decided mostly by the `Σδ ≠ 0` conditions, which
     depend on N. A random 6-set shape is admissible for only a few percent of the N values, so the per-N trees
     share little. The expected gain is small, and the per-node state (one bitset per σ, or one mask per N)
     costs more.
3. **Local-density / packing bounds for partial sets.**
   * *The idea:* if the ternary sums of a partial set P had dense clusters, the remaining elements' sums would
     have to spread the translates apart. That would give a lower bound on their size, and so a pruning test.
   * *Why it fails:* for 5 of 8 elements, `T(P)` has 243 points spread over ≳ 9000 integers (density ≈ 0.03).
     The full set's density constraint (6561 points in ≈ 2·10⁴) only appears when nearly all elements are
     present. The same holds for the bandwidth argument restricted to sub-grids.
   * *Conclusion:* **the obstruction is invisible before the last one or two levels**, so no early cut-off of
     this type exists.
4. **Pair-graph / clique look-ahead at level 5.** The remaining three elements must be pairwise-compatible
   legal singles, so one could search the compatibility graph on the ~100 legal singles. That graph is sparse
   (average degree 1–4). But building it costs about as much as the current bit-parallel scans, which already
   enumerate exactly these pairs. No net gain.
5. **"7-set first, then N"** (`N` is a hole of `D_{A∖{N}}`). This handles all N per 7-set. But the number of
   admissible 7-sets with maximum ≤ 1366 is about 3·10¹⁵, the same order as the per-N approach.

**Summary.** Every exact method found here enumerates the admissible 6- or 7-sets, about 10¹⁵–10¹⁶ in total. No
pruning idea found reduces that count by the needed 100–1000×. Such a reduction would seem to need new
mathematics: a lower-bound argument that works for partial configurations, which is exactly what Korsky's
"bandwidth barrier" remark says is missing.

## 3. What would make g₃(8) feasible: massively parallel hardware

The search maps naturally onto a GPU:
* one thread block per 5-set, with D₅ (about 13 000 bits for N ≈ 1300) held in shared memory;
* one thread per legal 6th element, doing about 10 window reads plus bit operations;
* the rare 7th/8th candidates handled inline.

**Estimate.** About 4·10¹⁵ node visits × about 200 integer operations, on an A100 at about 10¹³ integer ops/s,
gives about 1 day at full efficiency. With the 5–20 % efficiency typical of divergent tree search, that is
**about 5–20 days on one A100**, uncertain by a factor of about 3–5.

**What that means in practice:**
* about 110–450 A100-hours (≈ 22 h of full-efficiency work at 20 % to 5 % efficiency);
* cloud cost roughly a few hundred to about two thousand dollars;
* Colab Pro's roughly 7 A100-hours a month is not enough; Pro+ or a cluster allocation would be.

**Validation plan for such an implementation:** reproduce the exact canonical counts `V_k(N)` of
`results/n7_counts.csv` (n = 7, all N) and the CPU counts for n = 8 at small N before any production run.

## 4. Other values of the same problem

g₄(8) and g₅(9) look similarly out of reach on CPU. A rough extrapolation of the k = 4 counts puts g₄(8) at
N ≈ 600 at about 10¹¹–10¹² admissible 6/7-sets per N. The 4-AP test per node is also more expensive than the
ternary-sum test. This has not been measured.
