#!/usr/bin/env python3
"""
check_set.py -- exact certificate check for a candidate set A (Erdos Problem #817).

Checks, with exact integer arithmetic and no shortcuts:
  (a) the 3^n sums  sum_i e_i a_i  (e in {0,1,2}^n)  are pairwise distinct;
  (b) the subset-sum set H(A) = { sum_{a in S} a : S subset of A } contains no nonconstant 3-term AP
      (u < v < w with u + w = 2v), checked by testing every pair (u, w) of subset sums.
(a) and (b) are equivalent by Lemma 1 of METHODS.md; both are checked independently.

usage: python3 check_set.py 1,321,435,477,486,492,504  [more sets ...]
exit status 0 iff every set passes both checks.
"""
import itertools
import sys


def ternary_distinct(A):
    sums = [sum(e * a for e, a in zip(eps, A)) for eps in itertools.product((0, 1, 2), repeat=len(A))]
    return len(sums) == len(set(sums)), len(sums)


def subset_sums_3ap_free(A):
    H = set()
    for r in range(len(A) + 1):
        for S in itertools.combinations(A, r):
            H.add(sum(S))
    Hs = sorted(H)
    Hset = set(Hs)
    for i, u in enumerate(Hs):
        for w in Hs[i + 1:]:
            if (u + w) % 2 == 0 and (u + w) // 2 in Hset:
                return False, len(Hs), (u, (u + w) // 2, w)
    return True, len(Hs), None


def main():
    ok_all = True
    for arg in sys.argv[1:]:
        A = [int(t) for t in arg.replace('{', '').replace('}', '').split(',') if t.strip()]
        if len(set(A)) != len(A) or min(A) <= 0:
            print("INVALID INPUT", A)
            ok_all = False
            continue
        t_ok, t_cnt = ternary_distinct(A)
        h_ok, h_cnt, witness = subset_sums_3ap_free(A)
        status = "PASS" if (t_ok and h_ok) else "FAIL"
        print("%s n=%d max=%d A=%s | ternary sums distinct: %s (%d sums) | H(A) 3-AP-free: %s (|H|=%d)%s"
              % (status, len(A), max(A), sorted(A), t_ok, t_cnt, h_ok, h_cnt,
                 "" if witness is None else " witness AP %s" % (witness,)))
        ok_all &= (t_ok and h_ok)
    sys.exit(0 if ok_all else 1)


if __name__ == "__main__":
    main()
