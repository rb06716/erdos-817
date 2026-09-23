# Drafts for communicating the result (NOT submitted anywhere)

These are drafts for the repository owner. Nothing has been posted to OEIS, erdosproblems.com or elsewhere.

**Before posting anywhere:**
* **Credit the upper bound.** carlomitchener posted `g_3(7) <= 474` with the same set in the Erdős Problems
  forum thread #817 on 23 Sep 2026. That post is the first public report of the upper bound. What is new here
  is the matching lower bound and the uniqueness, and hence the exact value. (An admissible 7-set with maximum
  477 already appears in Bae (2002), so `g_3(7) <= 477` was implicit there; the drafts below credit it.)
* **Follow the forum rules** (quoted from erdosproblems.com/forum):
  * "AI assistance in generating ideas or helping to formulate the text of a comment is allowed, but should
    be disclosed."
  * "The contents of all comments, including any mathematical claims, should be independently verified by a
    human before posting here. If you do not understand the mathematics yourself, please do not post it here."
  * "Long proofs (or partial proofs) should not be posted here in full - instead, post a link."

  This package was produced by an AI agent (Claude), so the poster should disclose that. The poster should
  also verify the claims personally before posting:
  * **Minimum:** `python3 verify/verify_result.py quick`, about 10 min.
  * **Better:** `python3 verify/verify_result.py critical`, a few hours, which re-runs every N = 419…478.

  Either can be run in Google Colab with `verify/colab_verify_standalone.ipynb` (no GitHub access needed) or
  `verify/colab_verify.ipynb`, no local setup needed. Say in the post what was run.
  * **Status (2026-09-23):** the repository owner ran `quick` (7/7 PASS) and `critical` (all 60 values of N
    identical, 7/7 PASS) on Google Colab; see `results/external_verification/`.
* **Post as a comment in the discussion thread, not as a proof claim.** The problem asks for an estimate of
  `g_k(n)`, which "cannot be resolved with a finite computation". An exact small value is data for it, not a
  (partial) solution.

## 1. OEIS A399720: facts for an extension (write the text yourself)

**OEIS policy** ([Use of AI for OEIS Submissions is Forbidden](https://oeis.org/wiki/Use_of_AI_for_OEIS_Submissions_is_Forbidden),
approved 29 Aug 2026): every submission needs a human author who has verified the terms, comments and links. Using
AI to generate the full text of comments, pasting AI-generated text into the editorial discussion ("pink boxes"),
and crediting AI as an author are all forbidden. The items below are therefore **facts to write from, not text to
paste**; write the comments in your own words and answer editors' questions yourself.

* **Data:** the terms become `1, 3, 8, 22, 60, 168, 474`. Add an extension line in the OEIS style, e.g.
  `a(7) from _Ryan Brown_, Sep 23 2026` (with the date you submit).
* **About a(7):**
  * a(7) = 474, and {302, 409, 447, 459, 465, 466, 474} is the only 7-set attaining it: its 2187 sums with
    coefficients 0, 1, 2 are pairwise distinct;
  * no 7-subset of [1..473] qualifies. This was shown by exhaustive search with two independently written programs
    (C and Rust, opposite search orders), which agree on the number of qualifying k-subsets of [1..N] containing N
    for every N <= 478 (e.g. 6608257434 qualifying 6-subsets of [1..473] contain 473; none extends to a 7-set);
  * this settles the entry's remark that a(7) = 466 was not excluded;
  * credit: the upper bound a(7) <= 474, with the same set, was first posted by carlomitchener (Erdős Problems
    forum, thread #817, Sep 23 2026); the qualifying set {308, 417, 455, 469, 474, 476, 477} in Bae (2002) already
    implies a(7) <= 477 < 504.
* **About n = 6:** there are exactly two extremal sets, {107,145,159,162,164,168} and {107,145,159,162,166,168}.
  Bae (2002) and Bae and Choi (2003) state that {109,147,161,166,168,169} is the unique qualifying 6-set of minimal
  height; in fact it is the unique qualifying 6-set with maximum exactly 169.
* **Optional (upper bounds):** a(8) <= 1368, a(9) <= 3974, a(10) <= 11578, a(11) <= 34088, a(12) <= 100422, via
  A_n = {u_n - u_i : 0 <= i < n} with u = 0, 8, 9, 15, 27, 65, 172, 474, 1368, 3974, 11578, 34088, 100422.
* **Links (%H lines; bibliographic data, fine to use as given):**
  ```
  Jaegug Bae, <a href="https://www.ijpam.eu/contents/2002-1-3/8/8.pdf">On generalized subset-sum-distinct sequences</a>, Int. J. Pure Appl. Math. 1 (2002), 335-343.
  Jaegug Bae and Sungjin Choi, <a href="https://doi.org/10.4134/JKMS.2003.40.5.757">A generalization of a subset-sum-distinct sequence</a>, J. Korean Math. Soc. 40 (2003), 757-768.
  Ryan Brown, <a href="https://doi.org/ZENODO-DOI">Computations for g_3(7) = 474 (Erdős Problem #817)</a>, Zenodo, 2026.
  ```
  Replace `ZENODO-DOI` with the DOI of the v1.0.0 release (or link https://github.com/rb06716/erdos-817).

## 2. Possible new OEIS entries

Facts only, as in §1: a new entry needs your own name line, definition and comments.

* **g_4(n)**: `1, 3, 5, 14, 40, 79, 225`.
  * Definition: least N such that some n-subset of [1..N] has subset sums with no nonconstant 4-term AP
    (Erdős Problem #817 with k = 4).
  * a(6) = 79, attained only by {2,29,45,74,77,79}.
  * a(7) = 225, attained by exactly six sets: {2,90,135,193,220,222,225}, {4,90,135,206,215,219,225},
    {7,90,135,202,213,220,225}, {14,90,135,201,215,224,225}, {16,90,135,204,211,220,225},
    {17,90,135,205,222,223,225}.
* **g_5(n)**: `1, 2, 4, 6, 14, 22, 60, 92` (k = 5).
  * a(7) = 60, attained by exactly four sets: {1,39,44,55,56,59,60}, {1,5,39,55,56,59,60},
    {9,10,44,53,54,59,60}, {2,5,39,55,57,58,60}.
  * a(8) = 92, attained only by {10,11,67,77,78,81,82,92}.
* **Greedy "first-hole" chain from u_1 = 1**: `0, 1, 3, 8, 22, 60, 169, 477, 1387, 4041, 11785, 34709, 102263`.
  * Definition: u_{k+1} is the least integer > u_k such that {u_{k+1} - u_i : 0 <= i <= k} has distinct
    {0,1,2}-sums.
  * It equals A399720 for n <= 5.
  * Its n = 6 and n = 7 sets, {109,147,161,166,168,169} and {308,417,455,469,474,476,477}, both appear in
    Bae (2002).

## 3. Note for the Erdős Problems forum (thread #817, as a discussion comment)

The forum allows AI help with the wording if it is disclosed (the last paragraph does this), but asks that the
poster understands and has verified every claim. Edit it into your own words where you prefer, and replace
`ZENODO-DOI` with the DOI of the v1.0.0 release.

> Following carlomitchener's upper bound g_3(7) <= 474: an exhaustive search shows that this is sharp, so
> g_3(7) = 474, and {302, 409, 447, 459, 465, 466, 474} is the unique extremal set. In particular
> g_3(7) != 466, so the coincidence with A318821/A318863 noted above ends at n = 7.
>
> Every N <= 473 was searched by two independent programs, which agree on the number of admissible
> k-subsets of [1..N] containing N for every N <= 478. This does not rely on Korsky's bound. Code, logs and
> count tables: https://github.com/rb06716/erdos-817 (archived as https://doi.org/ZENODO-DOI)
>
> Two side remarks. First, extending m-czech's remark (b) above: the extremal sets for n = 4…7 all have the
> form {u_n − u_i}, where each u_{k+1} is an admissible "hole" for {u_1..u_k}. Continuing the n = 7 chain
> greedily gives g_3(8) <= 1368, g_3(9) <= 3974, g_3(10) <= 11578, g_3(11) <= 34088 and g_3(12) <= 100422.
> Second, Bae (Int. J. Pure Appl. Math. 1 (2002)) and Bae and Choi (J. Korean Math. Soc. 40 (2003)) state that
> {109,147,161,166,168,169} is the unique minimal 6-set of this kind. In fact g_3(6) = 168, as above. Bae (2002)
> also gives the admissible 7-set {308,417,455,469,474,476,477}, so g_3(7) <= 477 < 504 already follows from it.
>
> Disclosure: the search, the programs and this text were produced with an AI agent (Claude). I re-ran the
> verification myself on Google Colab (`verify/verify_result.py critical`). That covered the certificate check
> and the exhaustive search for every N = 419…478, i.e. every N above Korsky's bound g_3(7) ≥ 419. It
> reproduced all published count vectors and the unique set at N = 474. Below 419 the claim rests on Korsky's
> theorem and on the package's two independent programs, which also cover N = 1…418.
