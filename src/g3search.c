/*
 * g3search.c -- exhaustive search for the Erdos-Sarkozy function g_3(n) (Erdos Problem #817, OEIS A399720).
 *
 * A finite set A = {a_1,...,a_n} of positive integers is *admissible* when the 3^n sums
 *     sum_i e_i a_i,   e in {0,1,2}^n
 * are pairwise distinct; equivalently, when no nonzero c in {-2,...,2}^n has sum_i c_i a_i = 0.
 * (Korsky 2026, Prop. 4.1: this is exactly the condition that the subset-sum set H(A) contains no
 * nonconstant 3-term arithmetic progression.)  g_3(n) = min { max A : A admissible, |A| = n }.
 *
 * For each N in [Nlo, Nhi] this program enumerates ALL admissible n-sets with max A = N.
 *
 * Search order: the maximum N is placed first, then the remaining elements b_1 < b_2 < ... < b_{n-1} < N
 * are chosen in increasing order.  The state after L chosen elements is the bitset
 *     D_L = { sum_i c_i a_i : c in {-2,...,2}^L }            (a symmetric subset of [-R, R])
 * and a new element x keeps the set admissible iff  x notin D_L  and  2x notin D_L.
 * (Proof: a relation involving x with coefficient c_x in {+-1,+-2} reads c_x x = -(sum of the others),
 *  and the other part ranges over D_L; D_L is symmetric.)
 *
 * The last two levels are handled with windowed bit operations: for the (n-1)-th element y, the
 * admissible last elements x in (y, N) are those with  x - j*y notin D_{n-2}  and  2x - j*y notin D_{n-2}
 * for all j in {-2,...,2}  (because D_{n-1} = D_{n-2} + {0, +-y, +-2y}).
 *
 * Output: per N, the number of nodes visited at each depth and every admissible set found.
 * Node counts are deterministic and are meant to be cross-checked against an independent implementation.
 *
 * usage: g3search n Nlo Nhi [stop_at_first]
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>

#define MAXN 10
#define MAXWORDS 1024            /* bitset capacity: 65536 bits, i.e. R <= 32767 */

typedef uint64_t u64;

static int n, N, R, W;           /* W = number of words in use */
static u64 Dst[MAXN + 1][MAXWORDS];
static int dlo[MAXN + 1], dhi[MAXN + 1];   /* words outside [dlo, dhi] of Dst[L] are guaranteed zero */
static int elem[MAXN + 1];
static long long nodes[MAXN + 2];
static long long nsol;
static int stop_first;

static inline int getbit(const u64 *D, int p) {        /* p in [-R, R] */
    unsigned q = (unsigned)(p + R);
    return (int)((D[q >> 6] >> (q & 63)) & 1u);
}

/* dst = src | src<<a | src>>a | src<<2a | src>>2a  over words [lo, hi] (inclusive) */
static void expand(u64 *dst, const u64 *src, int a, int lo, int hi) {
    for (int i = lo; i <= hi; i++) dst[i] = src[i];
    for (int m = 1; m <= 2; m++) {
        int s = m * a, ws = s >> 6, bs = s & 63;
        for (int i = lo; i <= hi; i++) {
            u64 up = 0, dn = 0;
            int j = i - ws;                       /* shift toward higher positions */
            if (j >= 0) {
                up = src[j] << bs;
                if (bs && j - 1 >= 0) up |= src[j - 1] >> (64 - bs);
            }
            j = i + ws;                           /* shift toward lower positions */
            if (j < W) {
                dn = src[j] >> bs;
                if (bs && j + 1 < W) dn |= src[j + 1] << (64 - bs);
            }
            dst[i] |= up | dn;
        }
    }
}

/* extract bits [start, start+len) (positions, not indices) of D into out[] (len <= 64*16) */
static inline void window(const u64 *D, int start, int len, u64 *out) {
    unsigned q = (unsigned)(start + R);
    int w0 = (int)(q >> 6), b = (int)(q & 63);
    int nw = (len + 63) >> 6;
    for (int i = 0; i < nw; i++) {
        u64 v = D[w0 + i] >> b;
        if (b) v |= D[w0 + i + 1] << (64 - b);
        out[i] = v;
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

/* L = number of chosen elements; D = Dst[L]; last chosen element value = last */
static int dfs(int L, int last) {
    const u64 *D = Dst[L];
    if (L == n - 2) {
        /* choose y (element n-1) then x (element n), last < y < x < N */
        for (int y = last + 1; y <= N - 2; y++) {
            if (getbit(D, y) || getbit(D, 2 * y)) continue;
            nodes[L + 1]++;
            int len = N - 1 - y;                 /* x in [y+1, N-1] */
            u64 acc[20], tmp[20];
            int nw = (len + 63) >> 6;
            memset(acc, 0, sizeof(u64) * nw);
            for (int j = -2; j <= 2; j++) {      /* x - j*y in D  -> forbidden */
                window(D, y + 1 - j * y, len, tmp);
                for (int i = 0; i < nw; i++) acc[i] |= tmp[i];
            }
            for (int i = 0; i < nw; i++) {
                u64 free_ = ~acc[i];
                if (i == nw - 1 && (len & 63)) free_ &= (((u64)1) << (len & 63)) - 1;
                while (free_) {
                    int t = __builtin_ctzll(free_);
                    free_ &= free_ - 1;
                    int x = y + 1 + 64 * i + t;
                    int ok = 1;
                    for (int j = -2; j <= 2 && ok; j++)
                        if (getbit(D, 2 * x - j * y)) ok = 0;
                    if (ok) {
                        nodes[L + 2]++;
                        report(y, x);
                        if (stop_first) return 1;
                    }
                }
            }
        }
        return 0;
    }
    int remaining = n - L;                        /* elements still to choose, all < N */
    for (int x = last + 1; x <= N - remaining; x++) {
        if (getbit(D, x) || getbit(D, 2 * x)) continue;
        nodes[L + 1]++;
        elem[L] = x;
        /* active word range of the new set: |values| <= 2*sum */
        long long sum = 0;
        for (int i = 0; i < L; i++) sum += elem[i];
        sum += x;
        long long span = 2 * sum; if (span > R) span = R;
        int lo = (int)((R - span) >> 6), hi = (int)((R + span) >> 6);
        u64 *dst = Dst[L + 1];
        for (int i = dlo[L + 1]; i < lo && i <= dhi[L + 1]; i++) dst[i] = 0;
        for (int i = (hi + 1 > dlo[L + 1] ? hi + 1 : dlo[L + 1]); i <= dhi[L + 1]; i++) dst[i] = 0;
        dlo[L + 1] = lo; dhi[L + 1] = hi;
        expand(dst, D, x, lo, hi);
        if (dfs(L + 1, x)) return 1;
    }
    return 0;
}

int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage: %s n Nlo Nhi [stop_at_first]\n", argv[0]); return 2; }
    n = atoi(argv[1]);
    int Nlo = atoi(argv[2]), Nhi = atoi(argv[3]);
    stop_first = (argc > 4) ? atoi(argv[4]) : 0;
    if (n < 3 || n > MAXN) { fprintf(stderr, "n must be in [3,%d]\n", MAXN); return 2; }
    R = 2 * n * Nhi + 64;
    W = (2 * R + 1 + 63) / 64 + 2;
    if (W > MAXWORDS) { fprintf(stderr, "Nhi too large\n"); return 2; }
    for (N = Nlo; N <= Nhi; N++) {
        clock_t t0 = clock();
        memset(nodes, 0, sizeof(nodes));
        nsol = 0;
        for (int l = 0; l <= MAXN; l++) { memset(Dst[l], 0, sizeof(u64) * W); dlo[l] = 0; dhi[l] = W - 1; }
        /* D_0 = {0}; D_1 = {0, +-N, +-2N} */
        Dst[0][R >> 6] |= ((u64)1) << (R & 63);
        elem[0] = N;
        nodes[1] = 1;
        expand(Dst[1], Dst[0], N, 0, W - 1);
        dfs(1, 0);
        double el = (double)(clock() - t0) / CLOCKS_PER_SEC;
        printf("N=%d n=%d solutions=%lld nodes:", N, n, nsol);
        for (int d = 1; d <= n; d++) printf(" %lld", nodes[d]);
        printf(" time=%.2f\n", el);
        fflush(stdout);
        if (stop_first && nsol) break;
    }
    return 0;
}
