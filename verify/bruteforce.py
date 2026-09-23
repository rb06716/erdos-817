#!/usr/bin/env python3
"""
bruteforce.py -- definition-level brute force for small cases (independent of the fast searches).

Works directly from Erdos' original definition (Erdos Problem #817):
    H(A) = { sum_{a in S} a : S subset of A }   (as a SET of integers)
    A is good  <=>  H(A) contains no nonconstant 3-term arithmetic progression u < v < w, u + w = 2v.
It does NOT use the {0,1,2}-injectivity reformulation; instead it checks that reformulation separately
(test_equivalence) so the two characterisations are validated against each other.

For each N it enumerates ALL n-subsets of [1..N] containing N and reports how many are good, plus the
canonical counts V_k(N) (number of good k-subsets of [1..N] containing N) for k = 1..n, which must agree
with src/g3fast2.c compiled with -DNOROOM and with verify/g3verify_rs.

usage: python3 verify/bruteforce.py n Nmax           (prints one line per N = 1..Nmax)
       python3 verify/bruteforce.py --equivalence    (random + exhaustive equivalence test)
"""
import itertools
import random
import sys


def subset_sums(A):
    sums = {0}
    for a in A:
        sums |= {s + a for s in sums}
    return sums


def has_3ap(values):
    """True iff the finite set `values` contains u < v < w with u + w = 2v."""
    vals = sorted(values)
    vs = set(vals)
    m = len(vals)
    for i in range(m):
        u = vals[i]
        for j in range(i + 1, m):
            w = vals[j]
            if (u + w) % 2 == 0 and (u + w) // 2 in vs:
                return True
    return False


def good_by_definition(A):
    return not has_3ap(subset_sums(A))


def ternary_injective(A):
    seen = set()
    for e in itertools.product((0, 1, 2), repeat=len(A)):
        s = sum(ei * ai for ei, ai in zip(e, A))
        if s in seen:
            return False
        seen.add(s)
    return True


def test_equivalence(trials=3000, seed=12345):
    rng = random.Random(seed)
    bad = 0
    # exhaustive: all subsets of [1..14] of size 1..4
    for k in range(1, 5):
        for A in itertools.combinations(range(1, 15), k):
            if good_by_definition(A) != ternary_injective(A):
                bad += 1
                print("MISMATCH", A)
    # random larger sets
    for _ in range(trials):
        k = rng.randint(2, 6)
        M = rng.choice([20, 50, 100, 300])
        A = rng.sample(range(1, M + 1), k)
        if good_by_definition(A) != ternary_injective(A):
            bad += 1
            print("MISMATCH", A)
    print("equivalence test mismatches:", bad)
    return bad == 0


def counts_for_N(n, N):
    """V_k(N), k = 1..n: good k-subsets of [1..N] that contain N (by the definition)."""
    V = []
    sols = []
    for k in range(1, n + 1):
        c = 0
        for B in itertools.combinations(range(1, N), k - 1):
            A = B + (N,)
            if good_by_definition(A):
                c += 1
                if k == n:
                    sols.append(A)
        V.append(c)
    return V, sols


def main():
    if len(sys.argv) >= 2 and sys.argv[1] == "--equivalence":
        ok = test_equivalence()
        sys.exit(0 if ok else 1)
    n = int(sys.argv[1])
    Nmax = int(sys.argv[2])
    for N in range(1, Nmax + 1):
        V, sols = counts_for_N(n, N)
        for s in sols:
            print("SOLUTION N=%d {%s}" % (N, ",".join(map(str, s))))
        print("N=%d n=%d V: %s solutions=%d" % (N, n, " ".join(map(str, V)), len(sols)))
        sys.stdout.flush()


if __name__ == "__main__":
    main()
