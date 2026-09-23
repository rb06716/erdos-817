import numpy as np, sys
def first_hole(B, verbose=False):
    """B: offsets (positive, distinct). Returns (M, ok): smallest M > max B such that {M} u {M-b} is admissible,
    or (None, False) if B violates condition (i).  DP over (t = sum c, value = sum c b)."""
    B = sorted(B)
    m = len(B)
    S = sum(B)
    W = 2 * S                     # values in [-W, W]
    off = W
    tmin, tmax = -2 * m, 2 * m
    E = np.zeros((tmax - tmin + 1, 2 * W + 1), dtype=bool)   # E[t - tmin][v + off]
    E[0 - tmin][off] = True
    cur_sum = 0
    for b in B:
        # condition (i) incremental test for new element b: c*b notin U_{t' in [c-2, c+2]} E_t'  for c in {1,2}
        for c in (1, 2):
            v = c * b
            if v <= W:
                for tp in range(c - 2, c + 3):
                    if tmin <= tp <= tmax and E[tp - tmin][v + off]:
                        return None, False
        newE = np.zeros_like(E)
        for j in range(-2, 3):
            sh = j * b
            # newE[t + j][v + sh] |= E[t][v]
            for t in range(tmin, tmax + 1):
                t2 = t + j
                if t2 < tmin or t2 > tmax: continue
                src = E[t - tmin]
                if sh >= 0:
                    newE[t2 - tmin][sh:] |= src[:len(src) - sh] if sh > 0 else src
                else:
                    newE[t2 - tmin][:sh] |= src[-sh:]
        E = newE
        cur_sum += b
    # forbidden maxima: sM in U_{t in [s-2, s+2]} E_t for s >= 1
    lim = W + 1
    bad = np.zeros(lim + 1, dtype=bool)
    for s in range(1, 2 * m + 3):
        U = np.zeros(2 * W + 1, dtype=bool)
        for t in range(s - 2, s + 3):
            if tmin <= t <= tmax: U |= E[t - tmin]
        vals = np.nonzero(U[off + 1:])[0] + 1          # positive values
        vals = vals[vals % s == 0] // s
        vals = vals[vals <= lim]
        bad[vals] = True
    for M in range(B[-1] + 1, lim + 1):
        if not bad[M]: return M, True
    return lim + 1, True

if __name__ == '__main__':
    tests = [([1,3,8], 22), ([1,3,8,22], 60), ([4,6,9,23,61], 168), ([8,9,15,27,65,172], 474),
             ([24,27,31,45,81,188,502], 1380), ([8,9,15,27,65,172,474], 1368)]
    for B, exp in tests:
        print(B, first_hole(B), 'expected', exp)
