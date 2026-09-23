import numpy as np
def holes(B, limit_factor=None, kmax=None):
    """All M > max B (up to 2*sum(B)+1) such that {M} u {M-b : b in B} is admissible, assuming B satisfies
    condition (i); returns None if B violates (i)."""
    B = sorted(B); m = len(B); S = sum(B); W = 2 * S; off = W
    tmin, tmax = -2 * m, 2 * m
    E = np.zeros((tmax - tmin + 1, 2 * W + 1), dtype=bool)
    E[-tmin][off] = True
    for b in B:
        for c in (1, 2):
            v = c * b
            if v <= W:
                for tp in range(c - 2, c + 3):
                    if tmin <= tp <= tmax and E[tp - tmin][v + off]:
                        return None
        newE = np.zeros_like(E)
        for j in range(-2, 3):
            sh = j * b
            if j >= 0:
                newE[max(0, j):tmax - tmin + 1, sh:] |= E[:tmax - tmin + 1 - max(0, j), :2 * W + 1 - sh] if sh > 0 else E[:tmax - tmin + 1 - j]
            else:
                newE[:tmax - tmin + 1 + j, :sh] |= E[-j:, -sh:]
        E = newE
    lim = W + 1
    bad = np.zeros(lim + 1, dtype=bool)
    for s in range(1, 2 * m + 3):
        lo_t, hi_t = max(s - 2, tmin), min(s + 2, tmax)
        if lo_t > hi_t: continue
        U = E[lo_t - tmin:hi_t - tmin + 1].any(axis=0)
        vals = np.nonzero(U[off + 1:])[0] + 1
        vals = vals[vals % s == 0] // s
        vals = vals[vals <= lim]
        bad[vals] = True
    H = [M for M in range(B[-1] + 1, lim + 1) if not bad[M]]
    if kmax: H = H[:kmax]
    H.append(lim + 1) if not H else None
    return H
if __name__ == '__main__':
    print(holes([1, 3, 8])[:5], holes([4, 6, 9, 23, 61])[:5], holes([8, 9, 15, 27, 65, 172])[:5], holes([8,9])[:8], holes([8])[:5])
