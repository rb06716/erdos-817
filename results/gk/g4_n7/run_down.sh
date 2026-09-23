#!/bin/bash
# Downward g_4(7) worker: N = TOP, TOP-1, ... ; skips N already completed by any worker; stops when it reaches
# an N that an upward worker has completed or is running.
TOP=$1
for ((N = TOP; N >= 201; N--)); do
  if grep -qh "^N=$N k=4" g4_n7_proc*.log g4_n7_down.log 2>/dev/null; then echo "stop: N=$N already done" >> g4_n7_down.log; break; fi
  if pgrep -f "gk_search 4 7 $N $N" > /dev/null; then echo "stop: N=$N running upward" >> g4_n7_down.log; break; fi
  ../../../bin/gk_search 4 7 $N $N 1 >> g4_n7_down.log
done
