# Drafts for communicating the result (NOT submitted anywhere)

These are drafts for the repository owner. Nothing has been posted to OEIS, erdosproblems.com or elsewhere.

## 1. OEIS A399720: proposed extension

```
%S A399720 1,3,8,22,60,168,474
%C A399720 a(7) = 474, attained only by {302, 409, 447, 459, 465, 466, 474}. This refutes the possibility
            a(7) = 466 mentioned above and shows that the construction {1} U 3A (giving 504) is not optimal
            for n = 7. Two independent exhaustive searches (C and Rust, different search orders) agree on
            the number of admissible k-subsets of [1..N] containing N for every N <= 478
            (e.g. 6608257434 admissible 6-subsets of [1..473] containing 473, none extendable).
%C A399720 a(8) <= 1368, a(9) <= 3974, a(10) <= 11578, a(11) <= 34088, a(12) <= 100422, via
            A_n = {u_n - u_i : 0 <= i < n} with u = 0, 8, 9, 15, 27, 65, 172, 474, 1368, 3974, 11578, 34088,
            100422 (u_1..u_3 = 8, 9, 15; for k >= 3 each u_{k+1} is the least integer > u_k such that
            {u_{k+1} - u_i : 0 <= i <= k} qualifies).
%C A399720 For n = 6 there are exactly two extremal sets: {107,145,159,162,164,168} and {107,145,159,162,166,168}.
%e A399720 a(7) = 474: the 2187 sums 302*c_1 + 409*c_2 + 447*c_3 + 459*c_4 + 465*c_5 + 466*c_6 + 474*c_7
            with c_i in {0,1,2} are pairwise distinct, and no 7-element subset of [1..473] has this property.
%H A399720 <link to the published research package>
```

## 2. Possible new OEIS entries

* **g_4(n)**: `1, 3, 5, 14, 40, 79` (least N such that some n-subset of [1..N] has subset sums with no
  nonconstant 4-term AP; Erdős Problem #817 with k = 4). a(6) = 79 attained only by {2,29,45,74,77,79};
  a(7) >= 174.
* **g_5(n)**: `1, 2, 4, 6, 14, 22, 60` (k = 5). a(7) = 60 attained by exactly four sets:
  {1,39,44,55,56,59,60}, {1,5,39,55,56,59,60}, {9,10,44,53,54,59,60}, {2,5,39,55,57,58,60}.
* **Greedy "first-hole" chain from u_1 = 1**: `0, 1, 3, 8, 22, 60, 169, 477, 1387, 4041, 11785, 34709, 102263`
  (u_{k+1} = least integer > u_k such that {u_{k+1} - u_i : 0 <= i <= k} has distinct {0,1,2}-sums);
  equals A399720 for n <= 5.

## 3. Note for the Erdős Problems forum (thread #817)

> An exhaustive search gives g_3(7) = 474, with the unique extremal set {302, 409, 447, 459, 465, 466, 474}.
> Every N in [419, 473] was searched by two independent programs, and N <= 418 as well (not relying on
> Korsky's bound). The programs agree on the number of admissible k-subsets containing N for every N. Code,
> logs and count tables are at <link>. The extremal sets for n = 4…7 all have the form
> {u_n − u_i} where each u_{k+1} is an admissible "hole" for {u_1..u_k}. Continuing the n = 7 chain greedily
> gives g_3(8) ≤ 1368, g_3(9) ≤ 3974, g_3(10) ≤ 11578, g_3(11) ≤ 34088, g_3(12) ≤ 100422.
