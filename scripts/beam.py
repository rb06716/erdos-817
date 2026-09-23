"""
beam.py W K NMAX S0 -- beam search over hole chains (upper-bound constructions for g_3(n)).

A set is written in offset form A = {M} u {M - b : b in B}. Starting from B = {s} for every seed s <= S0, each level
extends a state (M, B) to (M', B u {M}) for the K smallest holes M' of B u {M} (scripts/holes_all.py). It keeps the
W states with the smallest M and prints the best set for each n <= NMAX.
Example: python3 scripts/beam.py 300 12 8 40 prints 8, 22, 60, 168, 474, 1368 (the known optima for n <= 7, and
the n = 8 upper bound) in about a second.
"""
import sys, time
from holes_all import holes
W = int(sys.argv[1]); K = int(sys.argv[2]); NMAX = int(sys.argv[3]); S0 = int(sys.argv[4])
t0 = time.time()
# level n=2 states: (M, B) with A = {M} u {M - b}
states = []
for s in range(1, S0 + 1):
    for M in holes([s])[:K]:
        states.append((M, (s,)))
states = sorted(set(states))[:W]
print(f'n=2 best {states[0]} beam {len(states)}', flush=True)
for n in range(3, NMAX + 1):
    cand = set()
    for M, B in states:
        B2 = tuple(sorted(B + (M,)))
        hs = holes(list(B2))
        if hs is None: continue
        for M2 in hs[:K]:
            cand.add((M2, B2))
    states = sorted(cand)[:W]
    A = sorted([states[0][0]] + [states[0][0] - b for b in states[0][1]])
    print(f'n={n} best M={states[0][0]} A={A} beam={len(states)} t={time.time()-t0:.0f}s', flush=True)
