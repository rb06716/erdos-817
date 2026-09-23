# Prior art and novelty assessment

Search performed 2026-09-22/23. Egress restrictions: arxiv.org, oeis.org, erdosproblems.com, researchgate,
scispace, semanticscholar, springer and sciencedirect could not be fetched directly. Sources were reached
through (i) the official OEIS git export `github.com/oeis/oeisdata` (export timestamp 2026-09-22T03:00:19-04:00,
all 399,468 entries searched locally), (ii) `github.com/teorth/erdosproblems` (problem database, cloned
2026-09-22), (iii) public GitHub repositories, and (iv) web-search result summaries.

## The problem

* **Erdős Problem #817** (erdosproblems.com/817). Source: P. Erdős, *Problems and results in combinatorial
  analysis and combinatorial number theory*, Graph theory, combinatorics, and applications, Vol. 1
  (Kalamazoo 1988), Wiley 1991, 397–406. Asks to estimate `g_k(n)`, in particular whether `g_3(n) ≫ 3^n`.
  Database status (teorth/erdosproblems, `data/problems.yaml`): **open**, last update 2025-08-31.
* **P. Erdős, A. Sárközy**, *Arithmetic progressions in subset sums*, Discrete Math. 102 (1992) 249–264.
  Lower bound of the form `3^n / n^{O(1)}`.

## Recent work (2026)

| source | date | content relevant here |
| --- | --- | --- |
| S. Korsky, *Arithmetic progression-free subset-sum sets*, arXiv:2606.24139 | 2026-06-23 | Prop. 4.1 (reformulation as `{0,1,2}`-injectivity), Thm 1.1 lower bound `g_3(n) ≥ b_n` (bandwidth of the ternary grid; `b_7 = 419`), values `g_3(1..4) = 1,3,8,22`, digit constructions. |
| S. Costa, *A negative answer to the Erdős–Sárközy question*, arXiv:2609.06303 | 2026-09-05 | `liminf g_3(n)/3^n = 0` (with a Lean certificate, Zenodo 10.5281/zenodo.22638810). |
| erdosproblems.com forum thread #817 (as quoted by the audit repository below) | 2026-09-17 | `g_3(5) = 60`, `g_3(6) = 168`; `g_3(n) ≪ 3^n/n^{1/3}` (Korsky, adapting B. Alexeev). |
| OEIS **A399720** (M. Czech) | created 2026-09-09, last edit 2026-09-14 | Terms `1, 3, 8, 22, 60, 168`; comment: "`419 <= a(7) <= 504` … `a(7) = 466` is not excluded"; keywords `hard,more,new`. |
| GitHub `firesh/erdos817-subset-sum-progressions-audit` (commit dee165d, 2026-09-18) | 2026-09-18 | Independent exhaustive computation of `g_3(5)`, `g_3(6)`; states "**The n = 7 search is incomplete: N ≤ 313 excluded**", "Still open …: the exact value `g_3(7)` and beyond". |

## Related concepts under other names

* **q-fold subset-sum-distinct sets** (all sums with coefficients in `{0,…,q}` distinct): J. Bae (1996, 1998),
  J. Bae & S. Choi, *A generalization of a subset-sum-distinct sequence*, J. Korean Math. Soc. 40 (2003).
  `q = 2` is exactly the admissibility condition used here. These papers study Conway–Guy-type
  constructions and asymptotics; no source found (and none cited by Korsky 2026, OEIS A399720 or the audit
  repository, all of which were aware of Bae's notion) gives exact minima for `n ≥ 5`.
* **Distinct subset sums** (binary analog, OEIS A276661): values known up to `n = 10` (a(10) = 309,
  P. W. Dyson, Oct 2025).
* OEIS search for the value string `1,3,8,22,60,168` finds only A399720 and two unrelated rooted-tree
  sequences A318821/A318863 (which continue `466`); this coincidence is noted in A399720.

## Novelty statement

As of 2026-09-22 no source located by these searches reports the value of `g_3(7)`; the most recent
explicit statements (OEIS A399720, 2026-09-14; audit repository, 2026-09-18) describe it as open, with
`419 ≤ g_3(7) ≤ 504`. Searches used: "g_3(7)", "Erdős–Sárközy subset sums three-term progression",
"Erdős problem 817", "k-fold subset-sum-distinct", "2-fold subset-sum-distinct", "sums with coefficients
0,1,2 distinct smallest largest element", and the value string `1,3,8,22,60,168` in the full OEIS export.

For `k = 4` (secondary result): no OEIS entry for `g_4(n)` exists (full-text search of the export for
entries mentioning both "subset sums" and "arithmetic progression" returns only A399720 and unrelated
Stanley sequences).
