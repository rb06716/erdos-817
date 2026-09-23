"""
seeds.py [NMAX] [SMAX] -- greedy first-hole chains from every seed u_1 = s <= SMAX, up to n = NMAX. It prints each
chain and the best maximum per n. The seed s = 1 gives 0, 1, 3, 8, 22, 60, 169, 477, ...; its n = 6 set is
Bae-Choi's {109, 147, 161, 166, 168, 169}.
"""
from hole_dp import first_hole
import sys
NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 9
SMAX = int(sys.argv[2]) if len(sys.argv) > 2 else 40
best = {}
for s in range(1, SMAX + 1):
    B = [s]; seq = [0, s]
    ok = True
    for n in range(2, NMAX + 1):
        M, good = first_hole(B)
        if not good: ok = False; break
        seq.append(M)
        if n not in best or M < best[n][0]: best[n] = (M, s)
        B = sorted(B + [M])
    print('seed', s, 'u =', seq, flush=True)
print('best per n:', best)
