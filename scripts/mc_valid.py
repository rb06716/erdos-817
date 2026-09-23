"""
mc_valid.py -- early Monte Carlo sizing of the n = 7 search: the fraction of random k-subsets of [1..460]
(k = 3..7) that are admissible, and the implied number of admissible k-subsets. Superseded by the exact counts
in results/n7_counts.csv, and by research/pruning/mc_counts.c for n = 8.
"""
import random, itertools, math
def valid(A):
    S = {0}
    for a in A:
        T = set()
        for s in S:
            for e in (0, a, 2*a):
                T.add(s+e)
        if len(T) != 3*len(S): return False
        S = T
    return True
random.seed(0)
M = 460
for k in (3,4,5,6,7):
    trials = 200000 if k < 7 else 400000
    cnt = 0
    for _ in range(trials):
        A = random.sample(range(1, M+1), k)
        if valid(A): cnt += 1
    p = cnt/trials
    print(k, cnt, trials, p, 'est valid k-subsets of [1..%d]: %.3g' % (M, p*math.comb(M,k)))
