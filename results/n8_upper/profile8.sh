#!/bin/bash
# n=8 upper-bound search with profile windows (per mille of M) -- NOT exhaustive; first hit per M
for M in $(seq 1300 1 1421); do
  timeout 300 ../../bin/g3profile 8 $M $M 1 1 0 600:700 830:900 920:970 940:1000 940:1000 940:1000 940:1000 | grep -E "SOLUTION|^N="
  if [ ${PIPESTATUS[0]} -eq 124 ]; then echo "M=$M timeout"; fi
done
