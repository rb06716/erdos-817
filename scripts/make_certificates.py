#!/usr/bin/env python3
"""
make_certificates.py -- write the certificate files in results/certificates/: for each set, the sorted lists of
its 3^n ternary sums (sum e_i a_i, e in {0,1,2}^n) and of its 2^n subset sums, one per line, and a summary with
SHA-256 hashes in certificates.json. Everything is recomputed with exact integer arithmetic; verify/check_set.py
checks the same properties directly.

usage: python3 scripts/make_certificates.py [OUTDIR]      (default: results/certificates)
"""
import hashlib
import itertools
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETS = [  # (key in certificates.json, file stem, set, note)
    ('g3_7_extremal', 'g3_n7_N474', [302, 409, 447, 459, 465, 466, 474], None),
    ('g3_8_construction', 'g3_n8_N1380', [878, 1192, 1299, 1335, 1349, 1353, 1356, 1380],
     'earlier construction (profile-window search), superseded by g3_8_upper_bound'),
    ('g3_8_upper_bound', 'g3_n8_N1368', [894, 1196, 1303, 1341, 1353, 1359, 1360, 1368],
     'the set certifying g_3(8) <= 1368 (hole chain; unique with maximum 1368 inside the profile windows)'),
]


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'results', 'certificates')
    os.makedirs(out, exist_ok=True)
    summary = {}
    for key, stem, A, note in SETS:
        tern = [sum(e * a for e, a in zip(eps, A)) for eps in itertools.product((0, 1, 2), repeat=len(A))]
        H = sorted({sum(S) for r in range(len(A) + 1) for S in itertools.combinations(A, r)})
        Hset = set(H)
        aps = sum(1 for i, u in enumerate(H) for w in H[i + 1:] if (u + w) % 2 == 0 and (u + w) // 2 in Hset)
        sha = {}
        for kind, values in (('ternary_sums', sorted(tern)), ('subset_sums', H)):
            data = ''.join('%d\n' % v for v in values).encode()
            with open(os.path.join(out, '%s_%s.txt' % (stem, kind)), 'wb') as f:
                f.write(data)
            sha[kind] = hashlib.sha256(data).hexdigest()
        entry = {'set': A, 'n': len(A), 'max': max(A), 'num_ternary_sums': len(tern),
                 'distinct_ternary_sums': len(set(tern)), 'ternary_sum_range': [min(tern), max(tern)],
                 'num_subset_sums': len(H), 'three_term_APs_in_subset_sums': aps,
                 'sha256_ternary_sums_file': sha['ternary_sums'], 'sha256_subset_sums_file': sha['subset_sums']}
        if note:
            entry['note'] = note
        summary[key] = entry
        print('%s: n=%d max=%d  ternary sums distinct: %d/%d  3-APs in subset sums: %d'
              % (key, len(A), max(A), len(set(tern)), len(tern), aps))
    with open(os.path.join(out, 'certificates.json'), 'w') as f:
        f.write(json.dumps(summary, indent=1))
    print('wrote', out)


if __name__ == '__main__':
    main()
