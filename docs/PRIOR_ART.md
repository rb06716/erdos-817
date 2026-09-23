# Prior art and novelty assessment

**Search history.**
* **First pass (2026-09-22/23):** made under egress restrictions. arxiv.org, oeis.org, erdosproblems.com,
  researchgate, scispace, semanticscholar, springer and sciencedirect could not be fetched directly. Sources
  were reached through:
  1. the official OEIS git export `github.com/oeis/oeisdata` (all 399,468 entries of the 2026-09-22 export,
     then all 399,527 of the 2026-09-23 export, searched locally);
  2. `github.com/teorth/erdosproblems` (the problem database);
  3. public GitHub repositories;
  4. web-search result summaries.
* **Second pass (afternoon of 2026-09-23, full internet access):** these sources were read directly:
  * the erdosproblems.com problem page, proof-claims page (with its comments), discussion thread and forum
    rules;
  * the live OEIS;
  * the arXiv sources of Korsky, Costa and Dutta;
  * a scan of Bae–Choi (2003);
  * Finch's *Errata and Addenda*.

  Still not obtained: Erdős–Sárközy (1992); the publisher blocks automated download.

  The second pass's findings are marked **(2nd pass)** below.
* **Third pass (evening of 2026-09-23, pre-publication audit):** J. Bae, *On generalized subset-sum-distinct
  sequences*, Int. J. Pure Appl. Math. 1(3) (2002) 335–343, was found at the URL given in Korsky's reference
  list (https://www.ijpam.eu/contents/2002-1-3/8/8.pdf) and read in full. The forum thread, the proof claims,
  OEIS A399720 and arXiv were re-checked at about 18:15–18:45 UTC. Findings are marked **(3rd pass)**.

## The problem

* **Erdős Problem #817** (erdosproblems.com/817). Source: P. Erdős, *Problems and results in combinatorial
  analysis and combinatorial number theory*, Graph theory, combinatorics, and applications, Vol. 1
  (Kalamazoo 1988), Wiley 1991, 397–406. It asks to estimate `g_k(n)`, and in particular whether
  `g_3(n) ≫ 3^n`.
  * **The site's status (2nd pass):** "**OPEN** — This is open, and cannot be resolved with a finite
    computation". There is one proof claim (Costa, classified as *partial*).
  * The git database (teorth/erdosproblems) also says open.
* **P. Erdős, A. Sárközy**, *Arithmetic progressions in subset sums*, Discrete Math. 102 (1992) 249–264.
  * The problem page says they proved `g_3(n) ≫ 3^n/n^{O(1)}`.
  * On the forum, Korsky locates on p. 261 the argument that the `3^n` ternary sums lie in an interval of
    length `nN`.
  * The paper itself was not obtained.
  * The sharpest known lower bound is Korsky's `g_3(n) ≥ b_n = (√3/(2√π) + o(1))·3^n/√n`.

## Recent work (2026)

| source | date | content relevant here |
| --- | --- | --- |
| S. Korsky, *Arithmetic progression-free subset-sum sets*, arXiv:2606.24139 (read in full, 2nd pass) | 2026-06-23 | Prop. 4.1 (reformulation as `{0,1,2}`-injectivity), Thm 1.1 lower bound `g_3(n) ≥ b_n` (bandwidth of the ternary grid; `b_7 = 419`), Remark "Small values": `g_3(1..4) = 1,3,8,22` only; `k ≥ 4`: asymptotic lower bound and digit constructions, **no small exact values**. |
| S. Costa, *A negative answer to the Erdős-Sárkőzy question*, arXiv:2609.06303 (read, 2nd pass) | 2026-09-05 | Thm 1.1 / Cor. 1.2: `liminf g_3(n)/3^n = 0`; a Lean verification of the Formal Conjectures statement is in Zenodo 10.5281/zenodo.22638810. No small values. On erdosproblems.com this is a **partial** proof claim: Xiao Hu (6 Sep) notes that Erdős asked for an estimate, and the moderator reclassified it. |
| erdosproblems.com forum thread #817, M. Czech ("m-czech") | 2026-09-09 | `g_3(5) = 60`, `g_3(6) = 168` (witnesses `{38,52,57,59,60}`, `{107,145,159,162,166,168}`), `419 ≤ g_3(7) ≤ 504`; "the value `g_3(7)` would decide whether the coincidence [with A318821/A318863, which continue with 466] persists (the search for n = 7 is beyond the simple enumeration used here)". **(3rd pass)** The same post also shows that `{1} ∪ 3A` gives `g_3(n+1) ≤ 3g_3(n)`, so Costa's liminf gives `lim g_3(n)/3^n = 0` (item 1), and notes (remark (b)) that for n ≤ 5 an optimal set is `{G_n − G_k}` with `G = 0,1,3,8,22,60`, "the same 'offsets from the maximum reproduce the sequence' phenomenon as in the Conway–Guy sets for distinct subset sums", a pattern that breaks at n = 6 (offsets `{0,2,6,9,23,61}`). |
| erdosproblems.com forum thread #817, S. Costa ("enomis_costa88") | 2026-09-17 | `g_3(n) ≪ 3^n/n^{1/3}`, more precisely `≤ ((3/4)^{1/3} + o(1))·3^n/n^{1/3}`, from a variation of B. Alexeev's construction for Erdős Problem #1. (Earlier versions of this file wrongly attributed this to Korsky and dated the n = 5, 6 values 17 Sep; both errors were copied from the audit repository's report.) |
| **erdosproblems.com forum thread #817, carlomitchener** | **2026-09-23, 06:41 forum time** | "**g_3(7) <= 474**: the 7-set {302, 409, 447, 459, 465, 466, 474} has 2187 distinct ternary digit sums (checked from the definition), so … g_3(n)/3^n stays below 0.216736 for n >= 7." Same set as ours, found independently (our repository was private). **This is the first public report of the upper bound.** It gives no lower bound and no uniqueness. |
| OEIS **A399720** (M. Czech) | created 2026-09-09, last edit 2026-09-14 | Terms `1, 3, 8, 22, 60, 168`; comment: "`419 <= a(7) <= 504` … `a(7) = 466` is not excluded"; keywords `hard,more,new`. Unchanged on the live site on 2026-09-23 (2nd pass). |
| GitHub `firesh/erdos817-subset-sum-progressions-audit` (commit dee165d, 2026-09-18) | 2026-09-18 | Independent exhaustive computation of `g_3(5)`, `g_3(6)`; states "**The n = 7 search is incomplete: N ≤ 313 excluded**", "Still open …: the exact value `g_3(7)` and beyond". |

## Related concepts under other names

* **q-fold subset-sum-distinct sets** (all sums with coefficients in `{0,…,q}` distinct). Case `q = 2` is
  exactly the admissibility condition used here.
  * **Bae (2002), read in the 3rd pass:** J. Bae, *On generalized subset-sum-distinct sequences*, Int. J. Pure
    Appl. Math. 1(3) (2002) 335–343, https://www.ijpam.eu/contents/2002-1-3/8/8.pdf. It introduces k-SSD sets
    (Def. 2.1); its counterfeit-coin puzzle (§2) asks exactly for distinct sums `Σ εᵢaᵢ`, `εᵢ ∈ {0,1,2}`.
    * **n = 6 (pp. 337–338):** "Lots of calculations shows that {109, 147, 161, 166, 168, 169} is the unique
      answer" for a 2-SSD 6-set of minimal height. Bae–Choi (2003) repeat this verbatim without citing it.
      It is wrong (below).
    * **n = 7 (p. 341, proof of Thm 3.6):** the 2-SSD 7-set {308, 417, 455, 469, 474, 476, 477}, obtained "by
      routine calculations, or by using similar construction of Conway-Guy sequence". No minimality is
      claimed, but it implies `g_3(7) ≤ 477 < 504`, which A399720 and the forum did not notice. It is one of
      the two admissible 7-sets with maximum 477 found here, and the greedy first-hole chain set from `u_1 = 1`.
    * No content for `k ≥ 4` in our sense (its k bounds the coefficients, not the progression length).
  * **Bae–Choi (2003), read in the 2nd pass:** J. Bae & S. Choi, *A generalization of a subset-sum-distinct
    sequence*, J. Korean Math. Soc. 40 (2003) 757–768, doi:10.4134/JKMS.2003.40.5.757.
    * **Definition:** their "k-SSD" (Def. 2.1) is equivalent to having no non-zero relation with coefficients
      in `{−k..k}` (their Lemma 3.2). So 2-SSD = admissible.
    * **Their claim for n = 6 (§2, p. 759, repeating Bae 2002):** "Lots of calculations shows that {109, 147,
      161, 166, 168, 169} is the unique answer" for a 2-SSD 6-set of minimal height. That would mean
      `g_3(6) = 169`.
    * **Why it is wrong:** our exhaustive search gives `g_3(6) = 168`, attained by two sets, in agreement with
      A399720, M. Czech and the audit repository. Their set is the unique admissible 6-set with maximum
      exactly 169 (`results/prior_art/bae_choi_n6_check.txt`).
    * **n = 7:** they give no value.
    * **Their construction:** `S_2^n` has maxima `1, 3, 9, 25, 73, 213, 621, 1845` for n = 1…8, against 474
      and ≤ 1368 here for n = 7, 8.
    * **Other literature:** Semantic Scholar lists only one citing work, Finch's *Errata and Addenda to
      Mathematical Constants* (arXiv:2001.00578), which cites it without values.
  * **Other Bae papers:** J. Bae (1996, 1998) treat ordinary (1-fold) subset-sum-distinct sets.
  * **Dutta (2026), read in full in the 2nd pass:** S. Dutta, *The greedy algorithm for dissociated sets*
    (arXiv:2601.07068). His "D_k sets" (no non-zero relation with coefficients in `{−k..k}`) are the same
    notion. The paper proves density bounds and studies the bottom-up greedy algorithm. It has no tables and
    no exact minima.
* **Distinct subset sums** (binary analog, OEIS A276661): values known up to `n = 10` (a(10) = 309,
  P. W. Dyson, 2025).
* **The value string `1,3,8,22,60,168`:** the only OEIS hits are A399720 and two unrelated rooted-tree
  sequences, A318821/A318863 (which continue `466`). A399720 itself notes this coincidence.

## Additional checks after the result (2026-09-23)

* **Web searches** (first pass): queries for the specific set `{302, 409, 447, 459, 465, 466, 474}`, for
  "g_3(7)", "Erdős Sárközy subset sums three-term progression n=7" and "erdosproblems 817 forum n=7". None
  found an n = 7 value. The forum itself could not be read then; see the 2nd pass.
* **Awards repository:** `github.com/TheJustinSunPrize/awards` PR #1030 (JSP-000674 = Erdős #817), opened
  2026-09-18, still open. It records "The n = 7 run remains incomplete (N ≤ 313 excluded, against the proven
  b_7 = 419)".
* **Conway–Guy-type recurrences** (proxy for Bae–Choi before it could be read): every recurrence
  `u_{n+1} = 3u_n − u_{n−r_n}` with sets `{u_n − u_i}` was enumerated for n ≤ 8
  (`scripts/conway_guy_ternary.py`). The best admissible 7-set of that family has maximum 543 > 474.
  Bae–Choi's own construction (read later) gives 621.
* **OEIS export:**
  * no entry contains `1,3,8,22,60,169`, `0,1,3,8,22,60,169`, `8,9,15,27,65,172`, `1368,3974`,
    `3974,11578`, `11578,34088`, `34088,100422` or `1387,4041`;
  * `474,1368` has no whole-term match (a plain substring search only hits a term boundary inside A250978,
    `…040474,13682…`);
  * for the k = 4, 5 values, no entry contains `1,3,5,14,40` or `1,2,4,6,14,22,60`. (`2,4,6,14,22` occurs
    only in unrelated A084685 and A307676.)

* **Re-check at ~09:30 UTC on 2026-09-23:**
  * **Newer OEIS export:** time.txt 2026-09-23T03:00:19-04:00, 399,527 entries. `scripts/oeis_novelty_check.py`
    was re-run on it (output: `results/prior_art/oeis_novelty_check_2026-09-23.txt`).
    * A399720 is unchanged (revision #6, Sep 14 2026, terms `1, 3, 8, 22, 60, 168`).
    * All value strings above still have no entry.
    * None of the 390 entries changed since the 2026-09-22 export mentions these values or the
      Erdős–Sárközy problem.
  * **Audit repository:** no commits after dee165d.
  * **Web searches** ("JSP-000674", "474" together with the problem's keywords): nothing new.
  * **Missed at the time:** the forum post of the upper bound (see the table), because the forum could not
    be read then.

* **Second pass (afternoon of 2026-09-23, full access):**
  * **Forum:** the problem page, proof claims and discussion thread were read directly; their content is in
    the table above.
  * **Forum rules (quoted):** "AI assistance in generating ideas or helping to formulate the text of a comment
    is allowed, but should be disclosed. The contents of all comments, including any mathematical claims,
    should be independently verified by a human before posting here. If you do not understand the
    mathematics yourself, please do not post it here. Long proofs (or partial proofs) should not be posted
    here in full - instead, post a link".
  * **Live OEIS searches** (control query `1,3,8,22,60,168` returns A318821, A318863, A399720): no results for
    `1,3,5,14,40,79`, `1,2,4,6,14,22,60,92`, `302,409,447,459,465,466,474`, `8,22,60,168,474`,
    `1,3,8,22,60,169`, `109,147,161,166,168,169` or `1,3,9,25,73,213`.
  * **arXiv API searches** ("subset sums" with "progression", "subset-sum-distinct", "Erdős–Sárközy",
    "Erdős problem 817", newest first): nothing after Costa's preprint of 2026-09-05.
  * **Papers:** Korsky, Costa, Dutta and Bae–Choi are summarised above.

* **Third pass (evening of 2026-09-23, about 18:15–18:45 UTC):**
  * **Bae (2002):** found and read (see "Related concepts"); it changes the credit for the n = 6 claim and adds
    the implicit bound `g_3(7) ≤ 477`.
  * **Forum thread #817:** still 8 posts; the latest is carlomitchener's (06:41 on 23 Sep). No post gives a lower
    bound above 419, uniqueness, anything for n = 8 or anything for k ≥ 4. M. Czech's remarks (item 1 and
    remark (b)) are now summarised in the table above.
  * **Proof claims:** still only Costa's (partial). **OEIS A399720:** revision #6 (14 Sep 2026), terms
    `1, 3, 8, 22, 60, 168`, no pending changes. **arXiv:** nothing relevant after Costa's preprint.
  * **Audit repository:** HEAD still dee165d; awards PR #1030 still open.

* **Hole-chain construction.** It is in the spirit of the Conway–Guy construction (`{u_n − u_i}`) for
  distinct subset sums, as is Bae–Choi's `S_2^n` (a fixed recurrence in the same offset form).
  **(3rd pass)** The offset form of the small optima and the Conway–Guy analogy were noted by M. Czech on the
  forum (9 Sep 2026, remark (b), n ≤ 5), and Bae (2002) already contains the n = 6 and n = 7 sets of the
  greedy chain from 1 (maxima 169, 477). The greedy algorithm studied by Dutta builds the sets bottom-up
  (smallest admissible next element), which is a different rule. New here: the "hole" formulation (every
  prefix of the chain gives an admissible set), the verification that every extremal set for n ≤ 7 is a hole
  chain, and the chain seeded by (8, 9, 15) with its values 1368, …, 879824.

## Novelty statement

As of the last re-check (about 18:30 UTC on 2026-09-23):
* **The exact value is unreported.** No source reports `g_3(7)` itself, and none gives a lower bound above
  Korsky's 419 or the uniqueness of the extremal set.
* **The upper bound is already public.** `g_3(7) ≤ 474`, with the same set, was posted independently on the
  forum on 2026-09-23 by carlomitchener. That is the first public report of the upper bound, and it must be
  credited.
* **A weaker upper bound was implicit since 2002.** Bae (2002) exhibits an admissible 7-set with maximum 477
  (not claimed minimal), so `g_3(7) ≤ 477`.
* **What remains new here:** the matching lower bound, uniqueness and hence the exact value; the n = 8…14
  upper bounds; the hole-chain structure (extending M. Czech's offset-form remark); the `k = 4, 5` values; and
  the correction of the n = 6 claim of Bae (2002) and Bae–Choi (2003).

Search terms included "g_3(7)", "Erdős–Sárközy subset sums three-term progression", "Erdős problem 817",
"k-fold subset-sum-distinct", "2-fold subset-sum-distinct", "dissociated" and "sums with coefficients 0,1,2
distinct smallest largest element". Value strings were searched in the full OEIS export and the live OEIS.

**For `k = 4, 5`** (secondary results):
* no OEIS entry for `g_4(n)` or `g_5(n)` exists (export full-text search and live searches);
* Korsky's paper, read in full, has small values only for `g_3`, n ≤ 4;
* the forum thread #817 contains no k ≥ 4 values.

The earlier caveat that Korsky might report small `g_4`, `g_5` values is therefore withdrawn. Bae (2002), since
read, has no k ≥ 4 values.
