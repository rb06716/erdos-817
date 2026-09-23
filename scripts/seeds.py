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
