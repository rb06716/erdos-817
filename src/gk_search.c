/*
 * gk_search.c -- exhaustive search for the Erdos-Sarkozy functions g_k(n) (Erdos Problem #817), k >= 3:
 *     g_k(n) = least N such that some n-element A subset of {1..N} has H(A) (the SET of subset sums)
 *              free of nonconstant k-term arithmetic progressions.
 *
 * Works directly from the definition (no reformulation): H is kept as a bitset,
 * H(A u {x}) = H(A) | (H(A) << x), and a k-AP u, u+d, ..., u+(k-1)d (d >= 1) exists in H iff
 * H & (H >> d) & (H >> 2d) & ... & (H >> (k-1)d) != 0 for some d.
 * Property "H(A) is k-AP-free" is hereditary (H(B) is a subset of H(A) for B subset of A), so a DFS that
 * adds elements one at a time and prunes as soon as a k-AP appears is complete.
 *
 * For each N in [Nlo, Nhi]: the maximum N is placed first, then b_1 < ... < b_{n-1} < N in increasing
 * order (no room pruning).  Prints every good n-set with maximum N and the counts
 * V_j(N) = #{good j-subsets of [1..N] containing N}, j = 1..n.
 *
 * usage: gk_search k n Nlo Nhi [stop_at_first]
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>

typedef uint64_t u64;
#define MAXN 12
#define MAXW 2048

static int K, n, N, W;
static u64 Hs[MAXN + 1][MAXW];
static int hw[MAXN + 1];                 /* number of meaningful words at each level */
static int elem[MAXN + 1];
static long long cnt[MAXN + 2];
static int stop_first, found;

/* dst = src | (src << x), for the first nw words (result may need one more word range) */
static void add_elem(u64 *dst, const u64 *src, int nw_src, int x, int nw_dst) {
    int ws = x >> 6, bs = x & 63;
    for (int i = 0; i < nw_dst; i++) {
        u64 v = (i < nw_src) ? src[i] : 0;
        int j = i - ws;
        if (j >= 0 && j < nw_src) {
            v |= src[j] << bs;
            if (bs && j - 1 >= 0) v |= src[j - 1] >> (64 - bs);
        } else if (bs && j == nw_src && j - 1 >= 0) {
            v |= src[j - 1] >> (64 - bs);
        }
        dst[i] = v;
    }
}

/* does bitset S (positions 0..maxpos) contain a nonconstant K-term AP? */
static int has_kap(const u64 *S, int nw, int maxpos) {
    static u64 acc[MAXW];
    for (int d = 1; (K - 1) * d <= maxpos; d++) {
        /* acc = S & (S >> d) & ... & (S >> (K-1)d) ; only need positions u with u + (K-1)d <= maxpos */
        int lim = maxpos - (K - 1) * d;          /* u in [0, lim] */
        int nwl = (lim >> 6) + 1;
        for (int i = 0; i < nwl; i++) acc[i] = S[i];
        for (int m = 1; m < K; m++) {
            int s = m * d, ws = s >> 6, bs = s & 63;
            for (int i = 0; i < nwl; i++) {
                u64 v = 0;
                int j = i + ws;
                if (j < nw) {
                    v = S[j] >> bs;
                    if (bs && j + 1 < nw) v |= S[j + 1] << (64 - bs);
                }
                acc[i] &= v;
            }
        }
        int rem = (lim & 63) + 1;
        if (rem < 64) acc[nwl - 1] &= (((u64)1) << rem) - 1;
        for (int i = 0; i < nwl; i++) if (acc[i]) return 1;
    }
    return 0;
}

static void dfs(int L, int last, int sum) {
    if (found && stop_first) return;
    if (L == n) return;
    for (int x = last + 1; x < N; x++) {
        int nsum = sum + x;
        int nw = (nsum >> 6) + 1;
        add_elem(Hs[L + 1], Hs[L], hw[L], x, nw);
        hw[L + 1] = nw;
        if (has_kap(Hs[L + 1], nw, nsum)) continue;
        cnt[L + 1]++;
        elem[L] = x;
        if (L + 1 == n) {
            found = 1;
            printf("SOLUTION k=%d N=%d {", K, N);
            for (int i = 1; i < n; i++) printf("%d,", elem[i]);
            printf("%d}\n", N);
            fflush(stdout);
            if (stop_first) return;
        } else {
            dfs(L + 1, x, nsum);
            if (found && stop_first) return;
        }
    }
}

int main(int argc, char **argv) {
    if (argc < 5) { fprintf(stderr, "usage: %s k n Nlo Nhi [stop_first]\n", argv[0]); return 2; }
    K = atoi(argv[1]); n = atoi(argv[2]);
    int Nlo = atoi(argv[3]), Nhi = atoi(argv[4]);
    stop_first = argc > 5 ? atoi(argv[5]) : 0;
    if ((long long)n * Nhi / 64 + 2 >= MAXW) { fprintf(stderr, "too large\n"); return 2; }
    for (N = Nlo; N <= Nhi; N++) {
        clock_t t0 = clock();
        memset(cnt, 0, sizeof(cnt));
        found = 0;
        memset(Hs[0], 0, sizeof(Hs[0]));
        Hs[0][0] = 1; hw[0] = 1;
        elem[0] = N;
        /* level 1: A = {N} */
        int nw = (N >> 6) + 1;
        add_elem(Hs[1], Hs[0], 1, N, nw);
        hw[1] = nw;
        if (has_kap(Hs[1], nw, N)) { printf("N=%d k=%d n=%d V: 0\n", N, K, n); continue; }
        cnt[1] = 1;
        if (n == 1) found = 1, printf("SOLUTION k=%d N=%d {%d}\n", K, N, N);
        else dfs(1, 0, N);
        printf("N=%d k=%d n=%d V:", N, K, n);
        for (int j = 1; j <= n; j++) printf(" %lld", cnt[j]);
        printf(" time=%.2f\n", (double)(clock() - t0) / CLOCKS_PER_SEC);
        fflush(stdout);
        if (stop_first && found) break;
    }
    return 0;
}
