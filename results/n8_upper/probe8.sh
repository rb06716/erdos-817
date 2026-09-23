#!/bin/bash
# n=8 upper-bound probe (NOT exhaustive): band-restricted search, other elements >= 0.62*M, first hit only
for M in 1400 1380 1360 1340 1320 1300; do
  lo=$(( M * 62 / 100 ))
  timeout 900 ./g3fast2_band8.bin 8 $M $M 1 1 0 $lo || echo "M=$M timeout"
done
