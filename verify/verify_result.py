#!/usr/bin/env python3
"""
verify_result.py -- one-command verification of g_3(7) = 474 for a human verifier (any machine with gcc/clang
and Python 3; also runs unchanged in Google Colab, see verify/colab_verify.ipynb).

usage:
  python3 verify/verify_result.py quick              (~5-15 min)
  python3 verify/verify_result.py critical [--jobs J] [--out DIR]   (hours: N = 419..478)
  python3 verify/verify_result.py full     [--jobs J] [--out DIR]   (hours: N = 1..478)
  add --rust to also run the independent Rust verifier at N = 473, 474 (needs cargo)

quick:    builds the programs, checks both certificates (7-set with max 474, 8-set with max 1368) directly from the
          definition, re-checks Lemma 1 numerically, reproduces g_3(5) = 60 and g_3(6) = 168 (both n = 6 extremal
          sets), and runs the exhaustive search at N = 473 (no admissible 7-set) and N = 474 (exactly the one set),
          comparing the full count vectors with the published table results/n7_counts.csv.
critical: the exhaustive search for every N = 419..478 (the range not covered by Korsky's theorem, plus 474..478
          where solutions exist), compared line by line with the published table and solution lists.
full:     every N = 1..478 (does not rely on Korsky's bound).
Runs are resumable: finished values of N (one log file per N in --out) are not recomputed.
Exit status 0 iff every check passed.
"""
import argparse
import concurrent.futures as cf
import csv
import glob
import os
import re
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TABLE = os.path.join(ROOT, 'results', 'n7_counts.csv')
LINE_C = re.compile(r'^N=(\d+) n=(\d+) solutions=(\d+) nodes: ([0-9 ]+) time=([0-9.]+)')
LINE_R = re.compile(r'^N=(\d+) n=(\d+) V: ([0-9 ]+) solutions=(\d+)')
LINE_S = re.compile(r'^SOLUTION N=(\d+) \{([0-9,]+)\}')
results = []


def report(name, ok, detail=''):
    results.append((name, ok))
    print('%-4s %s%s' % ('PASS' if ok else 'FAIL', name, ('  -- ' + detail) if detail else ''), flush=True)


def sh(cmd, **kw):
    return subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, **kw)


def cpu_flags():
    """(vendor, family, has_bmi2) from /proc/cpuinfo; (None, None, None) if unavailable (e.g. macOS)."""
    try:
        info = open('/proc/cpuinfo').read()
    except OSError:
        return None, None, None
    vendor = re.search(r'vendor_id\s*:\s*(\S+)', info)
    family = re.search(r'cpu family\s*:\s*(\d+)', info)
    flags = re.search(r'flags\s*:(.*)', info)
    return (vendor.group(1) if vendor else None, int(family.group(1)) if family else None,
            ('bmi2' in flags.group(1).split()) if flags else None)


def build(targets):
    vendor, family, bmi2 = cpu_flags()
    extra = ''
    if vendor == 'AuthenticAMD' and family == 23:
        extra = ' -DNO_PEXT'            # AMD Zen 1/2: PEXT is microcoded (slow); use the portable code path
    for cflags in ['-O3 -march=native' + extra, '-O3 -mcpu=native' + extra, '-O3' + extra]:
        r = sh(['make', '-s', 'CFLAGS=' + cflags] + targets)
        if r.returncode == 0:
            print('built %s with CFLAGS="%s" (cpu: %s family %s, bmi2=%s)' % (' '.join(targets), cflags, vendor,
                                                                              family, bmi2), flush=True)
            return True
    print(r.stdout, r.stderr)
    return False


def load_table():
    return {int(r['N']): ([int(r['V%d' % k]) for k in range(1, 8)], int(r['solutions']))
            for r in csv.DictReader(open(TABLE))}


def published_solutions():
    sols = {}
    for f in glob.glob(os.path.join(ROOT, 'results', 'n7_scan', '*.log')):
        for line in open(f):
            m = LINE_S.match(line)
            if m:
                sols.setdefault(int(m.group(1)), set()).add(m.group(2))
    return sols


def parse_log(path):
    vec, sols = None, set()
    for line in open(path):
        m = LINE_C.match(line) or None
        if m:
            vec = ([int(x) for x in m.group(4).split()], int(m.group(3)), float(m.group(5)))
        m2 = LINE_R.match(line)
        if m2:
            vec = ([int(x) for x in m2.group(3).split()], int(m2.group(4)), 0.0)
        m3 = LINE_S.match(line)
        if m3:
            sols.add(m3.group(2))
    return vec, sols


def run_one(N, out, prog='c'):
    path = os.path.join(out, '%s_%d.log' % (prog, N))
    if os.path.exists(path) and parse_log(path)[0] is not None:
        return N, path, True                  # already done (resume)
    binary = './bin/g3fast2_noroom' if prog == 'c' else './bin/g3verify'
    tmp = path + '.part'
    with open(tmp, 'w') as f:
        subprocess.run([binary, '7', str(N), str(N)], cwd=ROOT, stdout=f, check=True)
    os.replace(tmp, path)
    return N, path, False


def check_range(Ns, out, jobs, table, psols, prog='c'):
    os.makedirs(out, exist_ok=True)
    bad, t0, done = [], time.time(), 0
    with cf.ThreadPoolExecutor(max_workers=jobs) as ex:
        futs = [ex.submit(run_one, N, out, prog) for N in sorted(Ns, reverse=True)]   # largest (slowest) first
        for fu in cf.as_completed(futs):
            N, path, resumed = fu.result()
            (V, s, t), sols = parse_log(path)
            V0, s0 = table[N]
            ok = (V == V0 and s == s0 and (N < 474 or sols == psols.get(N, set())))
            done += 1
            print('  N=%d %s%s  (%d/%d, %.0f min elapsed)' % (N, 'ok' if ok else 'MISMATCH',
                  ' [resumed]' if resumed else '', done, len(Ns), (time.time() - t0) / 60), flush=True)
            if not ok:
                bad.append(N)
    return bad


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('mode', choices=['quick', 'critical', 'full'], help='what to verify (see above)')
    ap.add_argument('--jobs', type=int, default=os.cpu_count() or 1, help='parallel processes (default: all CPUs)')
    ap.add_argument('--out', default=os.path.join(ROOT, 'results', 'verify_run'),
                    help='directory for the per-N logs (default: results/verify_run, git-ignored)')
    ap.add_argument('--rust', action='store_true',
                    help='also run the independent Rust verifier at N = 473, 474 (needs cargo)')
    a = ap.parse_args()

    if not build(['bin/g3fast2', 'bin/g3fast2_noroom']):
        report('build', False, 'could not compile src/g3fast2.c')
        sys.exit(1)
    table, psols = load_table(), published_solutions()

    # 1. certificates, directly from the definition
    for s, n in [('302,409,447,459,465,466,474', 7), ('894,1196,1303,1341,1353,1359,1360,1368', 8)]:
        r = sh([sys.executable, 'verify/check_set.py', s])
        report('certificate n=%d {%s}' % (n, s), r.returncode == 0 and r.stdout.startswith('PASS'),
               r.stdout.strip()[:120])
    # 2. Lemma 1 (reformulation) against the raw definition
    r = sh([sys.executable, 'verify/bruteforce.py', '--equivalence'])
    report('Lemma 1 equivalence test', 'mismatches: 0' in r.stdout, (r.stdout.strip().splitlines() or [''])[-1])
    # 3. known values g_3(5) = 60, g_3(6) = 168 (first N with a solution; the n = 6 extremal sets)
    for n, hi, first, sets in [(5, 60, 60, None),
                               (6, 168, 168, {'107,145,159,162,164,168', '107,145,159,162,166,168'})]:
        r = sh(['./bin/g3fast2', str(n), '1', str(hi)])
        found = [(int(m.group(1)), m.group(2)) for m in map(LINE_S.match, r.stdout.splitlines()) if m]
        ok = bool(found) and min(N for N, _ in found) == first and (sets is None or
                                                                  {x for N, x in found if N == first} == sets)
        report('g_3(%d) = %d reproduced' % (n, first), ok, '%d sets at N=%d' % (sum(N == first for N, _ in found),
                                                                                 first))
    # 4. the decisive values N = 473, 474 (or the requested range)
    if a.mode == 'quick':
        Ns = [473, 474]
    elif a.mode == 'critical':
        Ns = list(range(419, 479))
    else:
        Ns = list(range(1, 479))
    print('exhaustive search, n = 7, %d values of N with %d parallel jobs -> %s' % (len(Ns), a.jobs, a.out),
          flush=True)
    bad = check_range(Ns, a.out, a.jobs, table, psols)
    report('n=7 canonical counts equal the published table for N in [%d, %d]' % (min(Ns), max(Ns)), not bad,
           'mismatches: %s' % bad if bad else '%d values' % len(Ns))
    if 474 in Ns:
        (V, s, t), sols = parse_log(os.path.join(a.out, 'c_474.log'))
        report('N=474: exactly one admissible 7-set, {302,409,447,459,465,466,474}',
               s == 1 and sols == {'302,409,447,459,465,466,474'})
    if a.mode == 'full':
        sols_found = [N for N in Ns if N <= 473 and parse_log(os.path.join(a.out, 'c_%d.log' % N))[0][1] != 0]
        report('no admissible 7-set for any N <= 473 (from this run)', not sols_found, str(sols_found or ''))
    if a.rust:
        if build(['bin/g3verify']):
            badr = check_range([473, 474], os.path.join(a.out, 'rust'), a.jobs, table, psols, prog='rust')
            report('independent Rust verifier agrees at N = 473, 474', not badr)
        else:
            report('Rust verifier build', False, 'cargo not available?')

    n_ok = sum(ok for _, ok in results)
    print('\n%d of %d checks passed.%s' % (n_ok, len(results), '' if n_ok == len(results) else '  SOME CHECKS FAILED'))
    if a.mode == 'quick' and n_ok == len(results):
        print('Note: quick mode checks the certificate and the two decisive values of N. The full claim needs '
              'every N <= 473: run "critical" (N = 419..473, with Korsky\'s bound) or "full" (all N).')
    sys.exit(0 if n_ok == len(results) else 1)


if __name__ == '__main__':
    main()
