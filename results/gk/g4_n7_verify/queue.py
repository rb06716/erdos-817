#!/usr/bin/env python3
"""Work queue for the remaining gk_verify values of N (k = 4, n = 7).

Replaces the sequential N = 1..200 loop part-way through, so that cores freed by the other loops are used.
Runs the given N values longest-first, one gk_verify process per N (output: gk_verify_q<N>.log), and
never starts a process while 4 or more gk_verify processes are running.  Writes lo_done.flag at the end.

usage: queue.py N1 N2 ...    (run from this directory)"""
import os
import subprocess
import sys
import time

MAXPROC = 4
BIN = '../../../bin/gk_verify'


def running_gk_verify():
    r = subprocess.run(['pgrep', '-xc', 'gk_verify'], capture_output=True, text=True)
    return int(r.stdout.strip() or 0)


todo = sorted((int(x) for x in sys.argv[1:]), reverse=True)
active = {}
while todo or active:
    for N, p in list(active.items()):
        if p.poll() is not None:
            print('N=%d finished rc=%d %s' % (N, p.returncode, time.strftime('%H:%M:%S')), flush=True)
            del active[N]
    if todo and running_gk_verify() < MAXPROC:
        time.sleep(2)                       # re-check: other loops start their next N within milliseconds
        if running_gk_verify() < MAXPROC:
            N = todo.pop(0)
            out = open('gk_verify_q%d.log' % N, 'w')
            active[N] = subprocess.Popen([BIN, '4', '7', str(N), str(N)], stdout=out)
            print('N=%d started %s' % (N, time.strftime('%H:%M:%S')), flush=True)
            continue
    time.sleep(10)
open('lo_done.flag', 'w').write('finished (queue)\n')
print('all done', time.strftime('%H:%M:%S'), flush=True)
