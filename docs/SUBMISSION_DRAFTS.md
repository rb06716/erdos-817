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

## 1. OEIS A399720: proposed extension

```
%S A399720 1,3,8,22,60,168,474
%C A399720 a(7) = 474, attained only by {302, 409, 447, 459, 465, 466, 474}. This refutes the possibility
            a(7) = 466 mentioned above. (That {1} U 3A, giving 504, is not optimal for n = 7 already follows
            from the qualifying set {308, 417, 455, 469, 474, 476, 477} of Bae (2002).)
            Two independent exhaustive searches (C and Rust, different search orders) agree on
            the number of admissible k-subsets of [1..N] containing N for every N <= 478
            (e.g. 6608257434 admissible 6-subsets of [1..473] containing 473, none extendable).
            The upper bound a(7) <= 474, with the same set, was first posted by carlomitchener on the
            Erdős Problems forum (thread #817, Sep 23 2026).
%C A399720 a(8) <= 1368, a(9) <= 3974, a(10) <= 11578, a(11) <= 34088, a(12) <= 100422, via
            A_n = {u_n - u_i : 0 <= i < n} with u = 0, 8, 9, 15, 27, 65, 172, 474, 1368, 3974, 11578, 34088,
            100422 (u_1..u_3 = 8, 9, 15; for k >= 3 each u_{k+1} is the least integer > u_k such that
            {u_{k+1} - u_i : 0 <= i <= k} qualifies).
%C A399720 For n = 6 there are exactly two extremal sets: {107,145,159,162,164,168} and {107,145,159,162,166,168}.
%C A399720 The qualifying sets are the 2-fold subset-sum-distinct sets of Bae (2002) and Bae and Choi (2003).
            Both state that {109,147,161,166,168,169} is the unique such 6-set of minimal height, but
            a(6) = 168; their set is the unique qualifying 6-set with maximum exactly 169.
%e A399720 a(7) = 474: the 2187 sums 302*c_1 + 409*c_2 + 447*c_3 + 459*c_4 + 465*c_5 + 466*c_6 + 474*c_7
            with c_i in {0,1,2} are pairwise distinct, and no 7-element subset of [1..473] has this property.
%H A399720 Jaegug Bae, <a href="https://www.ijpam.eu/contents/2002-1-3/8/8.pdf">On generalized subset-sum-distinct
            sequences</a>, Int. J. Pure Appl. Math. 1 (2002), 335-343.
%H A399720 Jaegug Bae and Sungjin Choi, <a href="https://doi.org/10.4134/JKMS.2003.40.5.757">A generalization of
            a subset-sum-distinct sequence</a>, J. Korean Math. Soc. 40 (2003), 757-768.
%H A399720 [your name, as OEIS requires], <a href="https://github.com/rb06716/erdos-817">Computations for
            g_3(7) = 474 (Erdős Problem #817)</a>, GitHub repository, 2026.
```

## 2. Possible new OEIS entries

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

> Following carlomitchener's upper bound g_3(7) <= 474: an exhaustive search shows that this is sharp, so
> g_3(7) = 474, and {302, 409, 447, 459, 465, 466, 474} is the unique extremal set. In particular
> g_3(7) != 466, so the coincidence with A318821/A318863 noted above ends at n = 7.
>
> Every N <= 473 was searched by two independent programs, which agree on the number of admissible
> k-subsets of [1..N] containing N for every N <= 478. This does not rely on Korsky's bound. Code, logs and
> count tables: https://github.com/rb06716/erdos-817
>
> Two side remarks. First, extending m-czech's remark (b) above: the extremal sets for n = 4…7 all have the
> form {u_n − u_i}, where each u_{k+1} is an admissible "hole" for {u_1..u_k}. Continuing the n = 7 chain
> greedily gives g_3(8) <= 1368, g_3(9) <= 3974, g_3(10) <= 11578, g_3(11) <= 34088 and g_3(12) <= 100422.
> Second, Bae (Int. J. Pure Appl. Math. 1 (2002)) and Bae and Choi (J. Korean Math. Soc. 40 (2003)) state that
> {109,147,161,166,168,169} is the unique minimal 6-set of this kind. In fact g_3(6) = 168, as above. Bae (2002)
> also gives the qualifying 7-set {308,417,455,469,474,476,477}, so 504 was already beaten there.
>
> Disclosure: the search, the programs and this text were produced with an AI agent (Claude). I re-ran the
> verification myself on Google Colab (`verify/verify_result.py critical`). That covered the certificate check
> and the exhaustive search for every N = 419…478, i.e. every N above Korsky's bound g_3(7) ≥ 419. It
> reproduced all published count vectors and the unique set at N = 474. Below 419 the claim rests on Korsky's
> theorem and on the package's two independent programs, which also cover N = 1…418.
