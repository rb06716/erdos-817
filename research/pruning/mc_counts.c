/* mc_counts.c -- Monte Carlo estimate of V_k(N) = #admissible k-subsets of [1..N] containing N.
   Samples uniform (k-1)-subsets of [1..N-1], adds N, tests admissibility (all 3^k ternary sums distinct).
   usage: mc_counts k N samples seed                                                          */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
static uint64_t s;
static inline uint64_t rnd(void) { s ^= s << 13; s ^= s >> 7; s ^= s << 17; return s; }
static unsigned char *seen; static int *stamp; static int cur = 0;
int main(int argc, char **argv) {
    int k = atoi(argv[1]), N = atoi(argv[2]); long samples = atol(argv[3]); s = strtoull(argv[4], 0, 10) | 1;
    int maxsum = 2 * k * N + 1;
    stamp = calloc(maxsum + 1, sizeof(int));
    long ok = 0; int a[16], T[60000];
    for (long it = 0; it < samples; it++) {
        int m = 0;
        while (m < k - 1) {                                /* distinct random elements of [1, N-1] */
            int x = 1 + rnd() % (N - 1), dup = 0;
            for (int j = 0; j < m; j++) if (a[j] == x) { dup = 1; break; }
            if (!dup) a[m++] = x;
        }
        a[k - 1] = N;
        cur++; int nt = 1, good = 1; T[0] = 0; stamp[0] = cur;
        for (int i = 0; i < k && good; i++) {             /* T <- T + {0, a_i, 2a_i}, detect collisions */
            int base = nt;
            for (int c = 1; c <= 2 && good; c++)
                for (int t = 0; t < base; t++) {
                    int v = T[t] + c * a[i];
                    if (stamp[v] == cur) { good = 0; break; }
                    stamp[v] = cur; T[nt++] = v;
                }
        }
        ok += good;
    }
    double C = 1; for (int j = 0; j < k - 1; j++) C = C * (N - 1 - j) / (j + 1);
    double p = (double)ok / samples, se = sqrt(p * (1 - p) / samples);
    printf("k=%d N=%d samples=%ld admissible=%ld p=%.3e (+-%.1e)  C(N-1,k-1)=%.3e  V_k~%.3e\n",
           k, N, samples, ok, p, se, C, p * C);
    return 0;
}
