import itertools
def analyze(A):
    A = sorted(A); M = A[-1]
    B = sorted(M - a for a in A[:-1])
    F = {}  # s -> set of values sum c_b b with s-2 <= sum c <= s+2
    vals = {}
    for c in itertools.product(range(-2, 3), repeat=len(B)):
        t = sum(c); v = sum(ci * bi for ci, bi in zip(c, B))
        vals.setdefault(t, set()).add(v)
    def Fs(s):
        out = set()
        for t in range(s - 2, s + 3):
            out |= vals.get(t, set())
        return out
    # condition (i): no nonzero c with |sum c|<=2 and value 0
    bad0 = [c for c in itertools.product(range(-2,3), repeat=len(B)) if any(c) and abs(sum(c)) <= 2 and sum(ci*bi for ci,bi in zip(c,B)) == 0]
    F1 = Fs(1)
    holes = [m for m in range(max(B) + 1, 2 * sum(B) + 2) if m not in F1 and 2 * m not in Fs(2)]
    print("A =", A, " M =", M, " B =", B, " sum B =", sum(B), " 2*sumB+1 =", 2*sum(B)+1)
    print("  condition (i) violations:", len(bad0))
    print("  allowed M in (max B, 2 sum B]:", holes[:12], "... count", len(holes))
analyze([302,409,447,459,465,466,474])
analyze([107,145,159,162,164,168])
analyze([107,145,159,162,166,168])
analyze([38,52,57,59,60])
