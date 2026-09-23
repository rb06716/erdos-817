/*
 * gk_verify.c -- independent check of src/gk_search.c (Erdos-Sarkozy g_k(n), general k >= 3).
 *
 * Deliberately different from gk_search.c:
 *   - elements after the maximum N are added in DECREASING order;
 *   - H(A) is kept as an explicit sorted array of distinct subset sums (plus a byte-map for membership);
 *   - k-APs are detected pairwise: for every pair u < v in H, test v + (v-u), ..., u + (k-1)(v-u) in H.
 * Counts: V_j(N) = number of subsets A of [1..N] with N in A, |A| = j, H(A) free of nonconstant k-APs.
 *
 * usage: gk_verify k n Nlo Nhi
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAXN 12
#define MAXSUM 20000
#define MAXH 4096

static int K, n, N;
static unsigned char inH[MAXN + 1][MAXSUM + 1];   /* membership per level */
static int Hs[MAXN + 1][MAXH], Hn[MAXN + 1];
static int elem[MAXN + 1];
static long long V[MAXN + 1];
static long long nsol;

static int has_kap(int lvl) {
    const int *h = Hs[lvl];
    const unsigned char *m = inH[lvl];
    int cnt = Hn[lvl], top = h[cnt - 1];
    for (int i = 0; i < cnt; i++)
        for (int j = i + 1; j < cnt; j++) {
            int d = h[j] - h[i];
            if (h[i] + (long)(K - 1) * d > top) break;       /* sorted: larger j only increases d */
            int ok = 1;
            for (int t = 2; t < K; t++) if (!m[h[i] + t * d]) { ok = 0; break; }
            if (ok) return 1;
        }
    return 0;
}

/* build level lvl+1 = H(level lvl) u (H(level lvl) + x) */
static void add(int lvl, int x) {
    const int *a = Hs[lvl];
    int na = Hn[lvl];
    int *out = Hs[lvl + 1];
    unsigned char *m = inH[lvl + 1];
    /* clear previous content of this level */
    for (int i = 0; i < Hn[lvl + 1]; i++) m[Hs[lvl + 1][i]] = 0;
    /* merge two sorted lists a and a+x, dropping duplicates */
    int i = 0, j = 0, c = 0;
    while (i < na || j < na) {
        int v;
        if (j >= na || (i < na && a[i] <= a[j] + x)) v = a[i++];
        else v = a[j++] + x;
        if (c == 0 || out[c - 1] != v) out[c++] = v;
    }
    Hn[lvl + 1] = c;
    for (int t = 0; t < c; t++) m[out[t]] = 1;
}

static void dfs(int lvl, int prev) {
    for (int x = prev - 1; x >= 1; x--) {
        add(lvl, x);
        if (has_kap(lvl + 1)) continue;
        V[lvl + 1]++;
        elem[lvl] = x;
        if (lvl + 1 == n) {
            nsol++;
            printf("SOLUTION k=%d N=%d {", K, N);
            for (int t = n - 1; t >= 0; t--) printf("%d%s", elem[t], t ? "," : "}\n");
        } else dfs(lvl + 1, x);
    }
}

int main(int argc, char **argv) {
    if (argc < 5) { fprintf(stderr, "usage: %s k n Nlo Nhi\n", argv[0]); return 2; }
    K = atoi(argv[1]); n = atoi(argv[2]);
    int lo = atoi(argv[3]), hi = atoi(argv[4]);
    if ((long)n * hi > MAXSUM || (1L << n) > MAXH) { fprintf(stderr, "too large\n"); return 2; }
    for (N = lo; N <= hi; N++) {
        memset(V, 0, sizeof V); nsol = 0;
        for (int l = 0; l <= MAXN; l++) { for (int i = 0; i < Hn[l]; i++) inH[l][Hs[l][i]] = 0; Hn[l] = 0; }
        Hs[0][0] = 0; Hn[0] = 1; inH[0][0] = 1;
        add(0, N);
        elem[0] = N;
        if (!has_kap(1)) {
            V[1] = 1;
            if (n == 1) { nsol = 1; printf("SOLUTION k=%d N=%d {%d}\n", K, N, N); }
            else dfs(1, N);
        }
        printf("N=%d k=%d n=%d V:", N, K, n);
        for (int j = 1; j <= n; j++) printf(" %lld", V[j]);
        printf("\n");
        fflush(stdout);
    }
    return 0;
}
