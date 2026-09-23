"""
conway_guy_ternary.py -- Conway-Guy-type recurrences for the ternary problem (used as a prior-art proxy).

Enumerates every sequence u with u_0 = 0, u_1 = 1 and u_{n+1} = 3 u_n - u_{n-r} (r = 1..n, chosen freely at each
step) up to n = 8. For each n it prints the smallest u_n for which A = {u_n - u_i : i < n} is admissible (distinct
{0,1,2}-sums), together with the set and the choices of r. See docs/PRIOR_ART.md.
"""
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
