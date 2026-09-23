# Limitations and remaining uncertainty

## Main result (g₃(7) = 474)

1. **Computer-assisted proof.** The upper bound is a certificate (an explicit set checked by exact
   arithmetic, directly against Erdős's definition). The lower bound (no admissible 7-set with maximum
   below 474) is established by exhaustive search, not by a human-readable argument. Trust rests on
   * two elementary lemmas proved in METHODS.md (Lemma 1: reformulation as `{0,1,2}`-injectivity; Lemma 2:
     one-step extension test), both also checked numerically against the raw definition; and
   * the correctness of the search programs, supported by agreement of independently written
     implementations (C, increasing order; Rust, decreasing order) on the *canonical count vectors*
     `V_k(N)` for every `N`, not only on the final yes/no answer, plus agreement with definition-level
     programs (Python brute force; `gk_search.c`) on smaller instances, including the n = 6 optimum.

   A common-mode error (a mistake shared by all implementations) is the main residual risk. The
   implementations share only the two lemmas. All programs in this package were written by the same author
   (an AI agent), so their independence lies in code structure, language and search order, not authorship.
   External anchors: the programs reproduce the independently published values `g₃(1..6)` (Korsky; the
   firesh audit repository; forum posts) and the extremal sets reported there, e.g. both n = 6 sets
   {107,145,159,162,164,168} and {107,145,159,162,166,168}. A third-party program (the audit repository's
   `g3.c`) exists but is far too slow for N ≈ 470. An independent re-implementation by a different person
   would be the most valuable further check.

2. **No compact certificate for non-existence.** Unlike SAT/DRAT proofs, the exhaustive search does not emit a
   small independently checkable proof object. The check is to re-run the search (a few CPU-hours per
   implementation for the critical range). The per-`N` count vectors act as fingerprints, and any
   re-implementation must reproduce them exactly.

3. **Hardware / transient errors.** Mitigated by two independent full runs on different code paths. Both
   would have to fail in the same way for the same `N`.

4. **Literature bound `g₃(7) ≥ 419`** (Korsky, arXiv:2606.24139). The first pass used it to skip `N ≤ 418`.
   That range was then searched exhaustively by both implementations (identical count vectors for all
   418 values), so the final claim does not depend on the theorem.

5. **Mutation testing** showed that bugs confined to the last search level are invisible when no solutions
   exist, which is the case for n = 7 and every N < 474. The final level of both programs was therefore
   also exercised where solutions exist: n = 6 over N ≤ 175, n = 7 at N = 474…478 (complete solution lists),
   and a band-restricted run over N = 474…520 in which both programs list the same 12,010 admissible 7-sets.

6. **Novelty.** arXiv, the OEIS web site, erdosproblems.com and publisher sites could not be fetched from the
   research environment. Novelty was assessed through the OEIS git export (dated 2026-09-22; re-checked against
   the 2026-09-23 export), the Erdős problems git database, GitHub, and web-search summaries (PRIOR_ART.md). The
   most recent public statements found (2026-09-14 and 2026-09-18) describe `g₃(7)` as open. A computation posted
   after the morning of 2026-09-23, or in a venue not indexed by these sources, would not have been detected.
   Bae–Choi (2003) could not be read; the Conway–Guy-type family it studies was re-enumerated as a proxy.

## Secondary results

7. **Upper bounds for n = 8…12** are certified constructions (exact checks), so they are upper bounds with no
   uncertainty. Whether they are *optimal* is unknown. The beam search is restricted to "hole chains", which
   contain every known optimum (n ≤ 7) but not every admissible set, and exhaustive search for n = 8 is far
   beyond the computation done here (roughly 10¹⁴ admissible 7-subsets per value of the maximum near 1360,
   extrapolating the n = 7 counts).

8. **Structural statements** ("all extremal sets for n ≤ 7 are hole chains") are verified facts for n ≤ 7 and
   an empirical pattern beyond that.

9. **`g₄`, `g₅` values** rest on two independent C implementations (increasing vs. decreasing order;
   bitset shifted-AND vs. pairwise AP detection) that agree on all canonical counts for the reported ranges.
   Python brute force independently confirms the smaller cases (k = 4: n ≤ 5; k = 5: n ≤ 6).
   `g₄(7) = 225`: each of the six extremal sets is checked directly against the definition: 98 distinct
   subset sums, no 4-term AP. Non-existence for N ≤ 224 was established twice:
   * by `gk_search`: N = 80…224, stopping at the first solution, with N ≤ 79 excluded by `g₄(6) = 79`;
   * by a full `gk_verify` enumeration of N = 1…225.

   The two programs give identical count vectors for all 145 shared values of N (80…224). At N = 225
   `gk_verify` lists six sets. A full `gk_search` enumeration at N = 225, to cross-check that list, is still
   running. As for g₃, both programs were written by the same author, and the novelty caveat for k ≥ 4 in
   PRIOR_ART.md applies.
