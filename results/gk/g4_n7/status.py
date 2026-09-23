#!/usr/bin/env python3
"""Coverage status of the g_4(7) search: which N are exhausted, which have admissible 7-sets."""
import re, glob, os
here = os.path.dirname(os.path.abspath(__file__))
files = [os.path.join(here, '..', 'g4_n7_partial_N80-173.log'), os.path.join(here, '..', 'g4_n7_lowprio_attempt.log'),
         os.path.join(here, '..', 'g4_n7_probe', 'probe.log')] + glob.glob(os.path.join(here, 'g4_n7_*.log'))
done, sols = {}, {}
for f in files:
    if not os.path.exists(f): continue
    for l in open(f):
        m = re.match(r'^N=(\d+) k=4 n=7 V: ([0-9 ]+)', l)
        if m: done[int(m.group(1))] = int(m.group(2).split()[-1])
        m = re.match(r'SOLUTION k=4 N=(\d+) \{([0-9,]+)\}', l)
        if m: sols.setdefault(int(m.group(1)), []).append(m.group(2))
N = 79
while N + 1 in done and done[N + 1] == 0: N += 1
best = min(sols) if sols else None
print('exhausted contiguously: 80..%d' % N)
print('N with an admissible 7-set found:', {k: v for k, v in sorted(sols.items())})
if best is not None and N + 1 == best: print('ESTABLISHED: g_4(7) = %d' % best)
else: print('bounds: %d <= g_4(7) <= %s' % (N + 1, best))
