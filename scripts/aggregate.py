#!/usr/bin/env python3
"""
aggregate.py -- collect per-N results of the exhaustive searches into one table and compare implementations.

C (src/g3fast2.c -DNOROOM) log lines:
    N=<N> n=<n> solutions=<s> nodes: V_1 ... V_n time=<t>
    SOLUTION N=<N> {a_1,...,a_n}
Rust (verify/g3verify_rs) log lines:
    N=<N> n=<n> V: V_1 ... V_n solutions=<s>
    SOLUTION N=<N> {a_1,...,a_n}

usage:
  aggregate.py table   <n> <logfiles...>                 -> CSV table on stdout (N, V_1..V_n, solutions)
  aggregate.py compare <n> --c <logs...> --rust <logs...> -> reports every N present in both, and any mismatch
"""
import re
import sys

LINE_C = re.compile(r'^N=(\d+) n=(\d+) solutions=(\d+) nodes: ([0-9 ]+) time=')
LINE_R = re.compile(r'^N=(\d+) n=(\d+) V: ([0-9 ]+) solutions=(\d+)')
LINE_S = re.compile(r'^SOLUTION N=(\d+) \{([0-9,]+)\}')


def parse(files, n):
    rows, sols = {}, {}
    for fn in files:
        for line in open(fn):
            line = line.strip()
            m = LINE_C.match(line)
            if m and int(m.group(2)) == n:
                V = tuple(int(x) for x in m.group(4).split())
                rows[int(m.group(1))] = (V, int(m.group(3)))
                continue
            m = LINE_R.match(line)
            if m and int(m.group(2)) == n:
                V = tuple(int(x) for x in m.group(3).split())
                rows[int(m.group(1))] = (V, int(m.group(4)))
                continue
            m = LINE_S.match(line)
            if m:
                A = tuple(sorted(int(x) for x in m.group(2).split(',')))
                sols.setdefault(int(m.group(1)), set()).add(A)
    return rows, sols


def main():
    mode, n = sys.argv[1], int(sys.argv[2])
    if mode == 'table':
        rows, sols = parse(sys.argv[3:], n)
        print('N,' + ','.join('V%d' % k for k in range(1, n + 1)) + ',solutions')
        for N in sorted(rows):
            V, s = rows[N]
            assert V[-1] == s, (N, V, s)
            assert len(sols.get(N, ())) == s, (N, s, sols.get(N))
            print('%d,%s,%d' % (N, ','.join(map(str, V)), s))
        return
    args = sys.argv[3:]
    ci, ri = args.index('--c'), args.index('--rust')
    cfiles = args[ci + 1:ri] if ci < ri else args[ci + 1:]
    rfiles = args[ri + 1:] if ri > ci else args[ri + 1:ci]
    crows, csols = parse(cfiles, n)
    rrows, rsols = parse(rfiles, n)
    common = sorted(set(crows) & set(rrows))
    bad = 0
    for N in common:
        if crows[N] != rrows[N] or csols.get(N, set()) != rsols.get(N, set()):
            bad += 1
            print('MISMATCH N=%d C=%s R=%s' % (N, crows[N], rrows[N]))
    print('compared %d values of N (%s..%s): %d mismatches'
          % (len(common), common[0] if common else '-', common[-1] if common else '-', bad))
    only_c = sorted(set(crows) - set(rrows))
    only_r = sorted(set(rrows) - set(crows))
    if only_c:
        print('only in C logs: %d values (%d..%d)' % (len(only_c), only_c[0], only_c[-1]))
    if only_r:
        print('only in Rust logs: %d values (%d..%d)' % (len(only_r), only_r[0], only_r[-1]))
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
