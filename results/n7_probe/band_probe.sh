#!/bin/bash
# Band-restricted probe (NOT exhaustive): for N = 431, 432, ..., search admissible 7-sets with max N whose
# other elements are >= floor(0.55 N); stop at the first N that has one.  Upper-bound locator only.
for N in $(seq 431 1 504); do
  lo=$(( N * 55 / 100 ))
  out=$(./g3fast2_band.bin 7 $N $N 1 1 0 $lo)
  echo "$out"
  if echo "$out" | grep -q SOLUTION; then break; fi
done
