#!/bin/bash
# n=8: profile-window search (NOT exhaustive) for M = 1361..1367, full enumeration inside windows
for M in 1361 1362 1363 1364 1365 1366 1367 1368; do
  ../../bin/g3profile 8 $M $M 0 1 0 600:700 830:900 920:970 940:1000 940:1000 940:1000 940:1000 | grep -E "SOLUTION|^N="
done
