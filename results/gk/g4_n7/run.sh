#!/bin/bash
# g_4(7) search: process k (of P) handles N = START + P*j + k, one N at a time (stop at the first admissible
# set of that N).  N = 80..173 were exhausted earlier (results/gk/g4_n7_partial_N80-173.log) and N = 174, 175 by
# the low-priority run (results/gk/g4_n7_lowprio_attempt.log).
k=$1; P=$2; START=$3
for ((N = START + k; N <= 400; N += P)); do
  ../../../bin/gk_search 4 7 $N $N 1 >> g4_n7_proc$k.log
  if grep -q SOLUTION g4_n7_proc$k.log; then break; fi
done
