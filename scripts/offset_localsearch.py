import numpy as np, itertools, random, sys, time
k = 7  # |B| for n = 8
C = np.array(list(itertools.product(range(-2, 3), repeat=k)), dtype=np.int64)   # 78125 x 7
T = C.sum(axis=1)
nonzero = np.any(C != 0, axis=1)
def first_hole(B):
    B = np.array(sorted(B), dtype=np.int64)
    if len(set(B.tolist())) < k or B[0] <= 0: return None
    V = C @ B
    # condition (i): no nonzero c with |sum c| <= 2 and value 0
    if np.any((V == 0) & nonzero & (np.abs(T) <= 2)): return None
    lim = int(2 * B.sum()) + 1
    forb = np.zeros(2 * lim + 10, dtype=bool)
    # s = 1: M in {V : T in [-1, 3]} ; s = 2: 2M in {V : T in [0,4]}; s = 3: 3M in {V: T in [1,5]} ...
    Ms = np.arange(0, lim + 1)
    bad = np.zeros(lim + 1, dtype=bool)
    for s in range(1, 2 * (k + 1) + 1):
        sel = (T >= s - 2) & (T <= s + 2)
        vals = V[sel]
        vals = vals[(vals > 0) & (vals % s == 0)] // s
        vals = vals[vals <= lim]
        bad[vals] = True
    for M in range(int(B.max()) + 1, lim + 1):
        if not bad[M]: return M
    return lim + 1
B0 = [24, 27, 31, 45, 81, 188, 502]
print('start', B0, first_hole(B0), flush=True)
random.seed(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
best = (first_hole(B0), B0)
cur = best
t0 = time.time()
iters = int(sys.argv[2]) if len(sys.argv) > 2 else 20000
for it in range(iters):
    B = list(cur[1])
    m = random.choice([1, 1, 2, 3])
    for _ in range(m):
        i = random.randrange(k)
        B[i] = max(1, B[i] + random.choice([-1, 1]) * random.randint(1, 8))
    h = first_hole(B)
    if h is None: continue
    if h < cur[0] or (h == cur[0] and random.random() < 0.3) or random.random() < 0.002:
        cur = (h, sorted(B))
        if h < best[0]:
            best = cur
            print(f'{time.time()-t0:7.1f}s it={it} M={h} B={best[1]} A={sorted([h] + [h - b for b in best[1]])}', flush=True)
print('best', best)
