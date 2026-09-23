#!/bin/bash
# stop-at-first-solution probe, N decreasing from 504 (upper bound only; not part of the exhaustive proof)
for N in $(seq 504 -1 430); do
  timeout 1200 ./g3fast2_probe.bin 7 $N $N 1
done
