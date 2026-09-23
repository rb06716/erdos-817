#!/usr/bin/env python3
"""Compare gk_verify (full enumeration) with gk_search (stop-at-first) for k = 4, n = 7.

gk_search ran with stop-at-first, so its count vector is complete for every N without a solution (N <= 224);
those vectors must equal gk_verify's exactly.  At N = 225 gk_verify lists every admissible 7-set."""
import glob
import os
import re

here = os.path.dirname(os.path.abspath(__file__))
gk = os.path.join(here, '..')


def load(files):
    vec, sols = {}, {}
    for f in files:
        for line in open(f):
            m = re.match(r'^N=(\d+) k=4 n=7 V: ([0-9 ]+?)(?: time=.*)?$', line.strip())
            if m:
                vec[int(m.group(1))] = tuple(int(x) for x in m.group(2).split())
            m = re.match(r'SOLUTION k=4 N=(\d+) \{([0-9,]+)\}', line)
            if m:
                sols.setdefault(int(m.group(1)), set()).add(m.group(2))
    return vec, sols


s_vec, s_sols = load([os.path.join(gk, 'g4_n7_partial_N80-173.log'), os.path.join(gk, 'g4_n7_lowprio_attempt.log')]
                     + glob.glob(os.path.join(gk, 'g4_n7', 'g4_n7_*.log')))
v_vec, v_sols = load(glob.glob(os.path.join(here, 'gk_verify_*.log')))
common = sorted(N for N in s_vec if N in v_vec and N <= 224)
mism = [N for N in common if s_vec[N] != v_vec[N]]
print('gk_verify covers N =', min(v_vec) if v_vec else None, '..', max(v_vec) if v_vec else None, '(%d values)' % len(v_vec))
print('compared N = 80..224 present in both: %d values; mismatches: %s' % (len(common), mism))
missing = [N for N in range(80, 225) if N not in common]
print('not yet compared in 80..224:', missing)
print('gk_verify: N <= 224 with an admissible 7-set:', sorted(N for N in v_sols if N <= 224))
if 225 in v_vec:
    print('N = 225: V =', v_vec[225], '; all admissible 7-sets:', sorted(v_sols.get(225, [])))
