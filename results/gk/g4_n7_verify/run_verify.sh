#!/bin/bash
# Independent re-verification of g_4(7) with verify/gk_verify.c (decreasing order, pairwise AP test):
# full enumeration (canonical counts V_1..V_7) for every N in [1, X]; process k handles N = 1 + k + P*j.
X=$1; P=${2:-4}
for ((k = 0; k < P; k++)); do
  ( for ((N = 1 + k; N <= X; N += P)); do ../../../bin/gk_verify 4 7 $N $N; done > gk_verify_k$k.log ) &
done
wait
echo finished > done.flag
