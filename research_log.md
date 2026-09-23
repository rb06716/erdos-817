# Research log

All times are container-local (UTC), 2026-09-22 onward. Entries are appended chronologically.

## 2026-09-22 — Session start, environment and resource survey

- Hardware: 4 vCPU (Intel Xeon @ 2.10GHz, AVX-512, BMI2), 15 GB RAM, ~30 GB disk.
- Toolchain: gcc 13.3, clang, rustc, go, Python 3.11 (+ numpy, scipy, sympy, networkx, python-sat installed via pip),
  PARI/GP 2.15.4 and nauty 2.8.8 installed via apt.
- Network: restrictive egress. WebSearch works (search-engine summaries); WebFetch/curl work for github.com,
  raw.githubusercontent.com, PyPI, crates, npm. Blocked: arxiv.org, oeis.org, wikipedia, semanticscholar, dblp,
  erdosproblems.com, springer, sciencedirect, etc.
- Key workaround: the complete OEIS database is mirrored at github.com/oeis/oeisdata (export timestamp
  2026-09-22T03:00:19-04:00). Sparse-cloned `seq/` (399,468 entries) for novelty checks and problem mining.

## Candidate directions considered (initial ranking)

Scored informally on novelty x tractability x verifiability x usefulness / cost.

1. Exact values of open extremal quantities listed in OEIS with keyword `hard`/`more`, few terms,
   solvable by exhaustive search / SAT with a certificate. (High verifiability; novelty checkable against OEIS.)
2. Automated falsification of OEIS conjectures (Colin Barker / Hardin empirical recurrences, Zhi-Wei Sun
   representation conjectures). (High novelty if a counterexample is found; low usefulness; lottery-like.)
3. Counterexamples to graph-theory conjectures (Graffiti / AutoGraphiX / recent arXiv) via nauty enumeration.
   (Literature access is badly limited by egress policy.)
4. Record constructions (codes, designs, packings): certificate trivially checkable, but record tables
   (codetables.de, La Jolla covering repository, Brouwer tables) are unreachable -> novelty unverifiable. Deprioritized.
5. Knot invariants with unknown values (KnotInfo via PyPI `database_knotinfo`). Crowded (DeepMind RL 2024,
   Brittenham-Hermiller 2025).

Mined OEIS: 634 `hard` extremal sequences with <= 14 terms; 268 entries referencing Erdős problems.
Shortlist:
- A399720 (Erdős Problem #817, Erdős–Sárközy function g_3(n)): terms 1,3,8,22,60,168; entry created
  2026-09-09 states 419 <= a(7) <= 504 and that a(7) = 466 "is not excluded".
- A391599 (Erdős–Lovász minimum intersecting n-uniform family with cover number n): 1,3,6,9,13; a(6) open.
  Likely much harder (hypergraph search on ~20 vertices).

## Decision 1: pursue g_3(7) (A399720, Erdős #817)

Reasons: explicitly open (OEIS 2026-09-09; audit repo firesh/erdos817-subset-sum-progressions-audit,
2026-09-18, reports "n = 7 search is incomplete: N <= 313 excluded"); a finite exhaustive computation;
upper bound certificate is an explicit 7-set; lower bound certifiable by independent reimplementations and
deterministic node counts; ties to an active Erdős problem.

Formulation (Korsky 2026, Prop 4.1; re-derived below): H(A) (subset sums) is 3-AP-free iff the map
eps -> sum eps_i a_i is injective on {0,1,2}^n, iff there is no nonzero c in {-2,...,2}^n with sum c_i a_i = 0.
g_3(n) = min over such A of max(A).

Feasibility estimate (Monte Carlo, `mc_valid.py`): fraction of random k-subsets of [1,460] that are valid:
k=5: 0.49, k=6: 0.016, k=7: < 2.5e-6. Estimated valid 5-subsets of [1,460] ~ 8e10, valid 6-subsets ~ 2e11.
A plain DFS is therefore ~1e11 nodes: feasible in hours on 4 cores only with cheap per-node work.

## 2026-09-22/23 — Search program development and validation

- `src/g3search.c`: reference DFS (max N first, then increasing elements; bitset D of {-2..2}-combinations;
  Lemma 2 of METHODS.md). Reproduces g_3(3..6) = 8, 22, 60, 168.
  Finding: at N = 168 there are exactly two admissible 6-sets, {107,145,159,162,164,168} and
  {107,145,159,162,166,168} (the OEIS lists only the second; the audit repo lists both).
- `src/g3fast2.c`: windowed bitsets + PEXT candidate scans; identical node counts to g3search.c;
  ~2.6x faster. `-DNOROOM` gives canonical counts V_k(N) (admissible k-subsets of [1..N] containing N).
- Timing (n=7): N=150: 0.16 s, 200: 0.96 s, 250: 4.2 s, 300: 16.9 s (g3search); g3fast2 at N=300: 6.4 s.
  Growth ~ N^7.6; N~420: ~95 s per N per core.
- `verify/g3verify_rs` (Rust, decreasing order, symmetric windows, no PEXT): canonical counts identical to
  `g3fast2 -DNOROOM` for n=4 (N<=40), n=5 (N<=90), n=6 (N<=175), n=7 (N<=150), and identical solution lists.
- `verify/bruteforce.py` (definition-level: subset sums tested for 3-APs, no reformulation): identical canonical
  counts and solution lists to the Rust verifier for n=4 (N<=30), n=5 (N<=45), n=6 (N<=32), n=7 (N<=26).
  Equivalence test of Lemma 1: 0 mismatches.
- `src/gk_search.c` (definition-level for general k, subset-sum bitset + AP detection): for k=3, n=5,
  N=55..60 canonical counts identical to g3fast2 -DNOROOM.

## 2026-09-23 00:02 — First n=7 scan (room-pruned mode), N = 419..434: no admissible 7-sets.
Kept in `results/n7_roompruned_partial/`. Restarted at 00:12 in -DNOROOM mode (canonical counts, ~4% more
nodes) so that every N can be cross-checked number-for-number against the Rust verifier:
`results/n7_scan/noroom_off{0..3}.log` (4 interleaved processes, N = 419 + 4j + off).

## Side exploration: g_4(n)
Definition-level brute force (Python) and gk_search.c: g_4(1..5) = 1, 3, 5, 14, 40, witnesses {1}, {1,3},
{1,4,5}, {1,9,13,14}, {1,13,35,39,40}. No OEIS entry for g_4. To be extended after the main computation.

## 2026-09-23 00:20 — Upper bound g_3(7) <= 474 (new; previous best 504)

- Observation (n = 4, 5, 6 extremal sets): elements as fractions of the maximum follow a common profile,
  min ~0.636, next ~0.864, next ~0.95, rest clustered near 1 (e.g. 107/168, 145/168, 159/168; 38/60, 52/60, 57/60;
  14/22, 19/22, 21/22).
- Added optional `minelem` argument to g3fast2.c (band-restricted search; NOT used for lower bounds).
- Band probe (`results/n7_probe/band_probe.sh`): for N = 431, 432, ... search 7-sets with max N and all other
  elements >= floor(0.55 N), stop at first hit. First hit: N = 474,
  A = {302, 409, 447, 459, 465, 466, 474}  (ratios 0.637, 0.863, 0.943, 0.968, 0.981, 0.983, 1).
  `verify/check_set.py` PASS: all 2187 ternary sums distinct; H(A) (128 subset sums) has no 3-AP.
  Hence g_3(7) <= 474. (The halved variant {151, 409, ...} fails: contains a 3-AP.)
- The exhaustive scan must therefore clear N = 419..473 (and N <= 418 for independence from Korsky's bound).
- Rust verifier optimised (branch-free slice passes, target-cpu=native, cheaper stale-word clearing):
  N=250 n=7 now 4.5 s (was 21 s); still identical canonical counts on all regression ranges.
- g_4(6) = 79 (witness {2,29,45,74,77,79}; N = 41..78 exhausted by gk_search.c). g_4(7) search running at nice 19.

## 2026-09-23 00:45 — Mutation test of the cross-check (sensitivity of the verification)

Five deliberate bugs injected into copies of g3fast2.c (-DNOROOM), compared against the Rust verifier:
| mutation | n=6, N<=175: N values with mismatching counts | n=7, N<=130 |
| --- | --- | --- |
| M1 skip the `2x notin D` test in candidate scans | 172/175 | 127/130 |
| M2 drop the j=2 window in the last level | 31/175 | 0/130 |
| M3 materialise level n-2 only up to 3N (needs 4N) | 12/175 | 0/130 |
| M4 drop the +-2a shifts in the D update | detected (runs killed early: far larger trees) | detected |
| M5 skip the `2x+2y` look-up in the last level | 12/175 | 0/130 |
Lesson: bugs confined to the last level only show up where admissible n-sets exist. For n=7 all V_7(N)=0 below
the answer, so the final verification must ALSO compare complete solution lists at N >= 474 (where n=7 solutions
exist), exercising the last level of both programs. Added to the plan.

Secondary: g_5(1..6) = 1, 2, 4, 6, 14, 22 (gk_search.c and Python brute force agree; witnesses {1}, {1,2}, {1,3,4},
{1,4,5,6}, {2,9,11,12,14}, {1,4,5,17,21,22}).

## 2026-09-23 01:05 — Profile-window search; n = 8 upper bound; N = 466 excluded

- `src/g3profile.c`: copy of g3fast2.c with per-element windows (per mille of N), for constructions only.
  Sanity: recovers {302,409,447,459,465,466,474} at N=474 in 0.1 s and both n=6 extremal sets instantly.
- n=8, windows 600:700 830:900 920:970 940:1000 x4 (results/n8_upper/profile8_coarse.log), first hit per M:
  M=1420 {892,1213,1313,1351,1363,1369,1378,1420}; M=1400 {888,1212,1327,1341,1351,1356,1369,1400};
  M=1380 {878,1192,1299,1335,1349,1353,1356,1380}; M=1360: none inside the windows.
  check_set.py PASS for the 1380 and 1400 sets (6561 ternary sums distinct; 256 subset sums 3-AP-free).
  => g_3(8) <= 1380 (previous best: 3 * g_3(7) <= 3 * 474 = 1422).
- Exhaustive n=7 scan: N=466 has NO admissible 7-set (V_7(466)=0), so a(7) != 466; the coincidence with the
  rooted-tree sequences A318821/A318863 noted in A399720 breaks at n = 7.

## 2026-09-23 01:20–01:40 — Main exhaustive result and start of independent verification

C (g3fast2 -DNOROOM), n = 7, results/n7_scan/noroom_off{0..3}.log:
- N = 419..473: V_7(N) = 0 for every N (no admissible 7-set with maximum N).
- N = 474: V_7 = 1, the unique set {302, 409, 447, 459, 465, 466, 474}.
- N = 475: 1 set {307,414,452,466,469,473,475}; N = 476: 0; N = 477: 2 sets {308,417,455,469,474,476,477},
  {309,416,454,468,471,473,477}; N = 478: 0.  (Processes stopped after N = 478.)
- Per-N wall time 90–300 s on a shared core; total ~4.5 CPU-hours for N = 419..478.
=> with Korsky's bound g_3(7) >= 419: g_3(7) = 474.

Independent verification launched (01:26): Rust verifier, N = 419..478, 4 interleaved processes
(results/n7_verify_rust_hi). First four values N = 419..422: full count vectors identical to C
(e.g. V_6(419) = 1,993,148,211; V_6(422) = 1,804,473,543).
C run for N = 1..418 started (results/n7_c_lo) to remove the dependence on Korsky's bound.

Prior-art re-check after the result: web searches for "474" with the extremal set, for "g_3(7)", for
2-fold subset-sum-distinct / D_q-set computations (Bae; Bae–Choi 2003; Dutta arXiv:2601.07068): nothing
reports g_3(7) or this set; latest sources (OEIS 2026-09-14, audit repo 2026-09-18) still list it as open.

## 2026-09-23 01:50 — Code review of g3fast2.c
Line-by-line review of the window invariants (every position in [needlo[L], needhi[L]] of level L holds the true
D_L bit; proof by induction on L recorded in METHODS.md section 4) and of the last-level read ranges
(x - jy in [-N, 3N], 2x - jy in [2, 4N-4]). One latent issue found: the scratch buffer in window_even()
(44 words) would overflow for candidate windows longer than 1408 bits. Never triggered by any run in this
package (n=7 runs have N <= 520; n=8 runs use narrow windows), but fixed (52 words + explicit Nhi <= 1536
guard). Rebuilt binaries give byte-identical outputs on regression ranges.

## 2026-09-23 01:40 — Offset analysis of the extremal sets (scripts/offset_analysis.py)
With A = {M} u {M - b : b in B}: all extremal sets satisfy condition (i) (no relation with |sum c| <= 2), and M
is exactly the FIRST admissible value above max B:
- n=7: B = {8,9,15,27,65,172}; allowed M in (172, 592]: 474, 486, 492, 493, 498, ... (97 values) -> M = 474.
- n=6: B = {4,6,9,23,61} -> first allowed M = 168; B = {2,6,9,23,61} -> 168.
- n=5: B = {1,3,8,22} -> 60.
So g_3(n) = min over offset sets B (|B| = n-1, condition (i)) of the first hole of
F(B) = {M : M in F_1(B) or 2M in F_2(B)} above max B.

## 2026-09-23 01:45 — Scale of the n = 7 computation; scheduling note; k >= 4 double-check
- Totals over N = 419..473 (C, canonical counts): admissible 5-sets 49,173,696,632; admissible 6-sets
  207,290,610,257; admissible 7-sets 0. Table: results/n7_counts_c_419-478.csv.
- Scheduling: the container has kernel autogroups enabled, so `nice` has no effect across separately
  launched sessions; the "nice 19" g_4(7) search had been taking a full core. Paused it at N = 173
  (results/gk/g4_n7_partial_N80-173.log: no admissible 7-set with max <= 173 for k = 4).
- verify/gk_verify.c (decreasing order, sorted sum list, pairwise AP test) vs src/gk_search.c (increasing
  order, bitset + shifted-AND AP test): identical canonical counts and solution lists for
  k=3 n=5 N<=62; k=4 n=5 N<=45; k=4 n=6 N<=80; k=5 n=5 N<=20; k=5 n=6 N<=25.
  => g_4(6) = 79 with UNIQUE extremal set {2,29,45,74,77,79}; g_5(6) = 22.
- Rust verifier gained an optional band argument (separate binary bin/g3verify_band; default behaviour
  unchanged) for cheap last-level cross-checks at N >= 474 where solutions exist.

## 2026-09-23 01:55 — Falsification attempt via Conway–Guy-type constructions (scripts/conway_guy_ternary.py)
Bae & Choi (2003) prove that "Conway–Guy-like" sequences are k-fold subset-sum-distinct (paper not reachable).
Exhaustive over all recurrences u_{n+1} = 3u_n - u_{n-r_n} (r_n in 1..n, u_0=0, u_1=1) with sets
S_n = {u_n - u_i : i < n}: the smallest admissible S_n has max 1, 3, 8, 23, 64, 189, 543, 1565 for n = 1..8.
No such set beats g_3(n) for n <= 7 (consistent with the exhaustive search), and none beats the new n = 8
construction (1380). So this construction family neither contradicts nor anticipates g_3(7) = 474.
