#!/bin/bash
# n=8 upper-bound search, coarse descending scan (profile windows, per mille of M); NOT exhaustive
for M in 1420 1400 1380 1360 1340 1320; do
  timeout 900 ../../bin/g3profile 8 $M $M 1 1 0 600:700 830:900 920:970 940:1000 940:1000 940:1000 940:1000 | grep -E "SOLUTION|^N="
  if [ ${PIPESTATUS[0]} -eq 124 ]; then echo "M=$M timeout"; fi
done
