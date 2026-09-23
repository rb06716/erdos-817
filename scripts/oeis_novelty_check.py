#!/usr/bin/env python3
"""
oeis_novelty_check.py -- reproducible part of the novelty check: search the official OEIS git export
(github.com/oeis/oeisdata) for the value strings produced in this package, and print the current A399720 entry.

usage:
  python3 scripts/oeis_novelty_check.py [path-to-oeisdata]
If no path is given, the export is sparse-cloned into ./oeisdata (needs git and ~1.6 GB of disk).
The runs recorded in docs/PRIOR_ART.md used the exports with time.txt = 2026-09-22T03:00:19-04:00 and
2026-09-23T03:00:19-04:00 (output of the second run: results/prior_art/oeis_novelty_check_2026-09-23.txt).
"""
import os
import subprocess
import sys

PATTERNS = {
    'g_3 known terms': '1,3,8,22,60,168',
    'g_3 with a(7)=474': '1,3,8,22,60,168,474',
    'n=7 extremal chain': '8,9,15,27,65,172',
    'chain continuation': '474,1368',
    'chain continuation 2': '1368,3974',
    'chain continuation 3': '3974,11578',
    'chain continuation 4': '11578,34088',
    'chain continuation 5': '34088,100422',
    'greedy chain from 1': '1,3,8,22,60,169',
    'greedy chain from 1 (b)': '1387,4041',
    'g_4': '1,3,5,14,40,79',
    'g_4 prefix': '1,3,5,14,40',
    'g_5': '1,2,4,6,14,22,60',
}


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else 'oeisdata'
    if not os.path.isdir(os.path.join(root, 'seq')):
        subprocess.check_call(['git', 'clone', '--depth', '1', '--filter=blob:none', '--sparse',
                               'https://github.com/oeis/oeisdata.git', root])
        subprocess.check_call(['git', '-C', root, 'sparse-checkout', 'set', 'seq'])
    print('export time:', open(os.path.join(root, 'time.txt')).read().strip())
    hits = {k: [] for k in PATTERNS}
    nseq = 0
    for d in sorted(os.listdir(os.path.join(root, 'seq'))):
        for f in sorted(os.listdir(os.path.join(root, 'seq', d))):
            if not f.endswith('.seq'):
                continue
            nseq += 1
            data, name = [], ''
            for line in open(os.path.join(root, 'seq', d, f), encoding='utf-8', errors='replace'):
                if line[:2] in ('%S', '%T', '%U'):
                    data.append(line[10:].strip())
                elif line[:2] == '%N':
                    name = line[10:].strip()
            s = ''.join(data).replace(' ', '')
            for k, p in PATTERNS.items():
                # match whole terms only
                if (',' + s + ',').find(',' + p + ',') >= 0:
                    hits[k].append((f[:-4], name[:90]))
    print('sequences scanned:', nseq)
    for k, p in PATTERNS.items():
        print('%-26s %-24s %s' % (k, p, hits[k] if hits[k] else 'no entry'))
    print('\n--- A399720 (current export) ---')
    for line in open(os.path.join(root, 'seq', 'A399', 'A399720.seq'), encoding='utf-8'):
        if line[:2] in ('%S', '%N', '%C', '%I'):
            print(line.rstrip()[:160])


if __name__ == '__main__':
    main()
