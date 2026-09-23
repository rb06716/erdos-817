import itertools
def admissible(A):
    S = {0}
    for a in A:
        T = {s + e*a for s in S for e in (0,1,2)}
        if len(T) != 3*len(S): return False
        S = T
    return True
best = {}
def rec(u, rs):
    n = len(u) - 1
    if n >= 1:
        S = [u[n] - u[i] for i in range(n)]
        if min(S) > 0 and len(set(S)) == n and admissible(S):
            if n not in best or u[n] < best[n][0]:
                best[n] = (u[n], sorted(S), tuple(rs))
    if n == 8: return
    for r in range(1, n + 1):
        rec(u + [3*u[n] - u[n - r]], rs + [r])
for mult in (3,):
    rec([0, 1], [])
for n in sorted(best): print(n, best[n])
