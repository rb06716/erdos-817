# Limitations and remaining uncertainty

1. **Computer-assisted proof.** The lower bound (no admissible 7-set with maximum below the claimed value) is
   established by exhaustive search, not by a human-readable argument. Trust rests on
   * the elementary lemmas in METHODS.md (Lemma 1: reformulation; Lemma 2: one-step extension), and
   * the correctness of the search programs, supported by agreement of independent implementations
     (C increasing-order search, Rust decreasing-order search, definition-level brute force for small
     cases) on the *canonical counts* `V_k(N)` for every `N` compared, not only on the final yes/no answer.
   A common-mode error (a mistake shared by all implementations) is the main residual risk; the
   implementations share only the mathematical lemmas, which are proved in METHODS.md and checked
   numerically by `verify/bruteforce.py --equivalence`.

2. **No compact certificate for non-existence.** Unlike SAT/DRAT proofs, the exhaustive search does not emit a
   small independently checkable proof object. Re-running the search (a few CPU-hours) is the check. The
   per-`N` count vectors act as fingerprints: any re-implementation must reproduce them exactly.

3. **Hardware / transient errors.** Mitigated by two independent full runs on different code paths; both
   would have to fail in the same way for the same `N`.

4. **Dependence on the literature bound `g_3(7) ≥ 419`.** Korsky's bandwidth bound (arXiv:2606.24139) is
   only used to skip `N ≤ 418` in the first pass; the range `N ≤ 418` is also searched exhaustively so that the
   final claim does not depend on it (see results/ for the exact coverage of each implementation).

5. **Novelty.** Access to arXiv, the OEIS web site, erdosproblems.com and publisher sites was blocked from the
   research environment; novelty was assessed through the OEIS git export (dated 2026-09-22), the Erdős
   problems git database, GitHub, and web-search summaries (see PRIOR_ART.md). A computation of `g_3(7)`
   posted after 2026-09-22 or in a venue not indexed by these sources would not have been detected.

6. **Secondary results (`g_4(n)`)** rest on a single fast implementation (`src/gk_search.c`) plus
   definition-level Python brute force for the smallest cases; they are reported separately and with that
   caveat.
