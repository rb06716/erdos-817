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
