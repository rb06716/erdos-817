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
