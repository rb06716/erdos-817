#!/bin/bash
# Band cross-check of the LAST search level where n=7 solutions exist: for N = 474..520, all admissible 7-sets
# with max N and every other element >= floor(0.55 N), enumerated by C (g3fast2, minelem) and by Rust
# (g3verify_band, minelem per mille = 550). Solution lists must be identical.
for N in $(seq 474 520); do
  lo=$(( N * 55 / 100 ))
  ../../bin/g3fast2 7 $N $N 0 1 0 $lo | grep -E "SOLUTION|^N=" >> c_band.log
  ../../bin/g3verify_band 7 $N $N 1 0 550 | grep -E "SOLUTION|^N=" >> rust_band.log
done
echo finished >> c_band.log
