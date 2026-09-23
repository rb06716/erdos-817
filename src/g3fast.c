/*
 * g3fast.c -- optimized exhaustive search for g_3(n) (Erdos Problem #817, OEIS A399720).
 *
 * Same mathematics and same search tree as g3search.c (see the comments there):
 *   A admissible  <=>  no nonzero c in {-2..2}^n with sum c_i a_i = 0
 *   D_L = { sum_{i<=L} c_i a_i : c in {-2..2}^L },  adding x is legal iff x notin D_L and 2x notin D_L.
 * The maximum N is placed first; the other elements are chosen in increasing order.
 *
 * Differences from g3search.c (performance only; the visited tree and the counts are identical):
 *   - D_L is only materialised on the window of positions that can still be read later:
 *       level n-2 needs [-N, 4N]; level L needs [-N-2(n-2-L)N, 4N+2(n-2-L)N]  (intersected with the
 *       true support [-2*sum_L, 2*sum_L]).
 *   - bitsets carry zero padding so the shift loops are branch-free (auto-vectorised).
 *
 * Node counts: nodes[k] = number of admissible k-sets {N} u B (|B| = k-1) with max B <= N-(n-k+1)
 * (the DFS visits exactly these).  For k = n this is the number of admissible n-sets with max N.
 *
 * usage: g3fast n Nlo Nhi [stop_at_first=0] [step=1] [offset=0]
 *        processes N = Nlo+offset, Nlo+offset+step, ... <= Nhi
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>

#define MAXN 10
typedef uint64_t u64;

static int n, N;
static int R;                     /* position p is stored at bit index p + R (+ padding) */
static int PADW;                  /* padding words on each side */
static int TOTW;                  /* physical words per level */
static u64 *Dbuf[MAXN + 1];
static int wlo[MAXN + 1], whi[MAXN + 1];   /* word range holding data; everything else is zero */
static int needlo[MAXN + 1], needhi[MAXN + 1];  /* position ranges needed per level */
static int elem[MAXN + 1];
static long long nodes[MAXN + 2];
static long long nsol;
static int stop_first;

#define WIDX(p) ((((p) + R) >> 6) + PADW)
#define BIDX(p) (((p) + R) & 63)

static inline int getbit(const u64 *D, int p) {
    return (int)((D[WIDX(p)] >> BIDX(p)) & 1u);
}

/* dst[lo..hi] = (src | src<<a | src>>a | src<<2a | src>>2a)[lo..hi]; src is zero outside its data range */
static void expand(u64 *restrict dst, const u64 *restrict src, int a, int lo, int hi) {
    int s1 = a, s2 = 2 * a;
    int w1 = s1 >> 6, b1 = s1 & 63, w2 = s2 >> 6, b2 = s2 & 63;
    if (b1 && b2) {
        for (int i = lo; i <= hi; i++) {
            u64 v = src[i];
            v |= (src[i - w1] << b1) | (src[i - w1 - 1] >> (64 - b1));
            v |= (src[i + w1] >> b1) | (src[i + w1 + 1] << (64 - b1));
            v |= (src[i - w2] << b2) | (src[i - w2 - 1] >> (64 - b2));
            v |= (src[i + w2] >> b2) | (src[i + w2 + 1] << (64 - b2));
            dst[i] = v;
        }
    } else {
        for (int i = lo; i <= hi; i++) {
            u64 v = src[i];
            v |= b1 ? ((src[i - w1] << b1) | (src[i - w1 - 1] >> (64 - b1))) : src[i - w1];
            v |= b1 ? ((src[i + w1] >> b1) | (src[i + w1 + 1] << (64 - b1))) : src[i + w1];
            v |= b2 ? ((src[i - w2] << b2) | (src[i - w2 - 1] >> (64 - b2))) : src[i - w2];
            v |= b2 ? ((src[i + w2] >> b2) | (src[i + w2 + 1] << (64 - b2))) : src[i + w2];
            dst[i] = v;
        }
    }
}

/* bits of positions [start, start+len) of D -> out[0..], len <= 64*20 */
static inline void window(const u64 *D, int start, int len, u64 *out) {
    int w0 = WIDX(start), b = BIDX(start);
    int nw = (len + 63) >> 6;
    if (b) {
        for (int i = 0; i < nw; i++) out[i] = (D[w0 + i] >> b) | (D[w0 + i + 1] << (64 - b));
    } else {
        for (int i = 0; i < nw; i++) out[i] = D[w0 + i];
    }
    int rem = len & 63;
    if (rem) out[nw - 1] &= (((u64)1) << rem) - 1;
}

static void report(int y, int x) {
    nsol++;
    printf("SOLUTION N=%d {", N);
    for (int i = 1; i <= n - 3; i++) printf("%d,", elem[i]);
    printf("%d,%d,%d}\n", y, x, N);
    fflush(stdout);
}

static int dfs(int L, int last, long long sum) {
    const u64 *D = Dbuf[L];
    if (L == n - 2) {
        for (int y = last + 1; y <= N - 2; y++) {
            if (getbit(D, y) || getbit(D, 2 * y)) continue;
            nodes[L + 1]++;
            int len = N - 1 - y;                     /* x in [y+1, N-1] */
            u64 acc[24], tmp[24];
            int nw = (len + 63) >> 6;
            window(D, y + 1, len, acc);              /* j = 0 */
            for (int j = -2; j <= 2; j++) {
                if (j == 0) continue;
                window(D, y + 1 - j * y, len, tmp);
                for (int i = 0; i < nw; i++) acc[i] |= tmp[i];
            }
            for (int i = 0; i < nw; i++) {
                u64 fr = ~acc[i];
                if (i == nw - 1 && (len & 63)) fr &= (((u64)1) << (len & 63)) - 1;
                while (fr) {
                    int t = __builtin_ctzll(fr);
                    fr &= fr - 1;
                    int x = y + 1 + 64 * i + t;
                    if (getbit(D, 2 * x) || getbit(D, 2 * x - y) || getbit(D, 2 * x + y) ||
                        getbit(D, 2 * x - 2 * y) || getbit(D, 2 * x + 2 * y)) continue;
                    nodes[L + 2]++;
                    report(y, x);
                    if (stop_first) return 1;
                }
            }
        }
        return 0;
    }
    int remaining = n - L;
    u64 *dst = Dbuf[L + 1];
    for (int x = last + 1; x <= N - remaining; x++) {
        if (getbit(D, x) || getbit(D, 2 * x)) continue;
        nodes[L + 1]++;
        elem[L] = x;
        long long s = sum + x, span = 2 * s;
        long long plo = -span, phi = span;
        if (plo < needlo[L + 1]) plo = needlo[L + 1];
        if (phi > needhi[L + 1]) phi = needhi[L + 1];
        int lo = WIDX((int)plo), hi = WIDX((int)phi);
        /* keep the invariant: zero outside [lo,hi] */
        for (int i = wlo[L + 1]; i <= whi[L + 1] && i < lo; i++) dst[i] = 0;
        for (int i = (hi + 1 > wlo[L + 1] ? hi + 1 : wlo[L + 1]); i <= whi[L + 1]; i++) dst[i] = 0;
        wlo[L + 1] = lo; whi[L + 1] = hi;
        expand(dst, D, x, lo, hi);
        if (dfs(L + 1, x, s)) return 1;
    }
    return 0;
}

int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage: %s n Nlo Nhi [stop_first] [step] [offset]\n", argv[0]); return 2; }
    n = atoi(argv[1]);
    int Nlo = atoi(argv[2]), Nhi = atoi(argv[3]);
    stop_first = argc > 4 ? atoi(argv[4]) : 0;
    int step = argc > 5 ? atoi(argv[5]) : 1, offset = argc > 6 ? atoi(argv[6]) : 0;
    if (n < 4 || n > MAXN) { fprintf(stderr, "n in [4,%d]\n", MAXN); return 2; }
    R = 2 * n * Nhi + 128;
    PADW = (2 * Nhi) / 64 + 4;
    TOTW = (2 * R + 1) / 64 + 2 + 2 * PADW;
    for (int l = 0; l <= MAXN; l++) Dbuf[l] = (u64 *)aligned_alloc(64, sizeof(u64) * ((TOTW + 7) / 8 * 8));
    for (N = Nlo + offset; N <= Nhi; N += step) {
        clock_t t0 = clock();
        memset(nodes, 0, sizeof(nodes));
        nsol = 0;
        for (int l = 0; l <= MAXN; l++) { memset(Dbuf[l], 0, sizeof(u64) * TOTW); wlo[l] = PADW; whi[l] = TOTW - PADW - 1; }
        /* needed position ranges */
        needlo[n - 2] = -N; needhi[n - 2] = 4 * N;
        for (int L = n - 3; L >= 0; L--) { needlo[L] = needlo[L + 1] - 2 * N; needhi[L] = needhi[L + 1] + 2 * N; }
        if (needhi[0] > R || -needlo[0] > R) { fprintf(stderr, "R too small\n"); return 2; }
        Dbuf[0][WIDX(0)] |= ((u64)1) << BIDX(0);
        elem[0] = N;
        nodes[1] = 1;
        {
            long long plo = -2LL * N, phi = 2LL * N;
            if (plo < needlo[1]) plo = needlo[1];
            if (phi > needhi[1]) phi = needhi[1];
            int lo = WIDX((int)plo), hi = WIDX((int)phi);
            expand(Dbuf[1], Dbuf[0], N, lo, hi);
            wlo[1] = lo; whi[1] = hi;
            for (int i = PADW; i < lo; i++) Dbuf[1][i] = 0;
            for (int i = hi + 1; i < TOTW - PADW; i++) Dbuf[1][i] = 0;
        }
        dfs(1, 0, N);
        double el = (double)(clock() - t0) / CLOCKS_PER_SEC;
        printf("N=%d n=%d solutions=%lld nodes:", N, n, nsol);
        for (int d = 1; d <= n; d++) printf(" %lld", nodes[d]);
        printf(" time=%.2f\n", el);
        fflush(stdout);
        if (stop_first && nsol) break;
    }
    return 0;
}
