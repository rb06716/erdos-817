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
