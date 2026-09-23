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
  Contains the lower-bound remark behind the question (paper not reachable here; the sharpest known lower
  bound is Korsky's `g_3(n) ≥ b_n = (√3/(2√π) + o(1))·3^n/√n`, see below).

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

## Additional checks after the result (2026-09-23)

* Web searches for the specific set `{302, 409, 447, 459, 465, 466, 474}`, for "g_3(7)", "Erdős Sárközy subset
  sums three-term progression n=7", "erdosproblems 817 forum n=7": no source reports an n = 7 value.
* `github.com/TheJustinSunPrize/awards` PR #1030 (JSP-000674 = Erdős #817), opened 2026-09-18, still open:
  records "The n = 7 run remains incomplete (N ≤ 313 excluded, against the proven b_7 = 419)".
* q-fold subset-sum-distinct literature: S. Dutta, *The greedy algorithm for dissociated sets*
  (arXiv:2601.07068, 2026) treats greedy sequences and asymptotic bounds for D_q-sets, not exact minima.
  The Conway–Guy-type constructions of Bae–Choi (2003) could not be read; as a proxy, every recurrence
  `u_{n+1} = 3u_n − u_{n−r_n}` with sets `{u_n − u_i}` was enumerated for n ≤ 8
  (`scripts/conway_guy_ternary.py`): the best admissible 7-set of that family has maximum 543 > 474.
* OEIS export: no entry contains `1,3,8,22,60,169`, `0,1,3,8,22,60,169`, `8,9,15,27,65,172`, `1368,3974`,
  `3974,11578`, `11578,34088`, `34088,100422` or `1387,4041`; the only hit for `474,1368` is an unrelated
  array-counting sequence (A250978). For the k = 4, 5 values: no entry contains `1,3,5,14,40` or
  `1,2,4,6,14,22,60` (`2,4,6,14,22` occurs only in unrelated A084685, A307676).

* Re-check on 2026-09-23 (~09:30 UTC), just before the final commit: the newer OEIS export (time.txt
  2026-09-23T03:00:19-04:00, 399,527 entries) was fetched and `scripts/oeis_novelty_check.py` re-run on it
  (output: `results/prior_art/oeis_novelty_check_2026-09-23.txt`). A399720 is unchanged
  (revision #6, Sep 14 2026, terms `1, 3, 8, 22, 60, 168`), all value strings above still have no entry, and none of
  the 390 entries changed since the 2026-09-22 export mention these values or the Erdős–Sárközy problem. The audit
  repository has no commits after dee165d. Web searches ("JSP-000674", "474" together with the problem's
  keywords) turned up nothing new.

* Hole-chain construction: in the spirit of the Conway–Guy construction (`{u_n − u_i}`) for distinct subset
  sums. The greedy algorithm studied by Dutta (arXiv:2601.07068) builds D_q-sets bottom-up (smallest
  admissible next element), which is a different rule. No source found describes the top-down "least hole"
  chain for `{0,1,2}`-sums or its values.

## Novelty statement

As of 2026-09-23 no source located by these searches reports the value of `g_3(7)`; the most recent
explicit statements (OEIS A399720, 2026-09-14; audit repository, 2026-09-18) describe it as open, with
`419 ≤ g_3(7) ≤ 504`. Searches used: "g_3(7)", "Erdős–Sárközy subset sums three-term progression",
"Erdős problem 817", "k-fold subset-sum-distinct", "2-fold subset-sum-distinct", "sums with coefficients
0,1,2 distinct smallest largest element", and the value string `1,3,8,22,60,168` in the full OEIS export.

For `k = 4, 5` (secondary results): no OEIS entry for `g_4(n)` or `g_5(n)` exists (full-text search of the export
for entries mentioning both "subset sums" and "arithmetic progression" returns only A399720 and unrelated
Stanley sequences; value strings checked above). Korsky (arXiv:2606.24139) treats `k ≥ 4` (lower bound
`g_k(n) ≫ ((k−1)/(k−2))^n n^{−log_2((k−1)/(k−2))}` and digit constructions); the paper could not be read in
full, so small exact values of `g_4`, `g_5` reported there cannot be excluded. The novelty claim for `k ≥ 4` is
therefore weaker than for `g_3(7)`.
