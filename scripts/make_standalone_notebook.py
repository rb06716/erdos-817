#!/usr/bin/env python3
"""
make_standalone_notebook.py -- build verify/colab_verify_standalone.ipynb: a Colab notebook that contains
(compressed) copies of everything verify/verify_result.py needs, so it runs without GitHub access or tokens.
The files are taken from the committed tree (git HEAD); the notebook prints their SHA-256 so they can be
compared with the repository.

usage: python3 scripts/make_standalone_notebook.py
"""
import base64
import gzip
import hashlib
import json
import subprocess

FILES = ['Makefile', 'src/g3fast2.c', 'verify/check_set.py', 'verify/bruteforce.py', 'verify/verify_result.py',
         'results/n7_counts.csv'] + ['results/n7_scan/noroom_off%d.log' % k for k in range(4)] + \
        ['verify/g3verify_rs/Cargo.toml', 'verify/g3verify_rs/Cargo.lock', 'verify/g3verify_rs/.cargo/config.toml',
         'verify/g3verify_rs/src/main.rs']
OUT = 'verify/colab_verify_standalone.ipynb'


def git(*args):
    return subprocess.run(['git'] + list(args), capture_output=True, check=True).stdout


def md(s):
    return {"cell_type": "markdown", "metadata": {}, "source": s.strip('\n').splitlines(keepends=True)}


def code(s):
    return {"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [],
            "source": s.strip('\n').splitlines(keepends=True)}


def main():
    commit = git('rev-parse', 'HEAD').decode().strip()
    blobs = []
    for path in FILES:
        data = git('show', 'HEAD:' + path)
        b64 = base64.b64encode(gzip.compress(data, mtime=0)).decode()
        lines = [b64[i:i + 100] for i in range(0, len(b64), 100)]
        blobs.append((path, hashlib.sha256(data).hexdigest(), lines))
    embed = ['import base64, gzip, hashlib, os', "ROOT = '/content/g3verify'", 'FILES = {']
    for path, h, lines in blobs:
        embed.append('  %r: (%r, (' % (path, h))
        embed += ['    %r' % ln for ln in lines]
        embed.append('  )),')
    embed += ['}',
              'ok = True',
              'for path, (sha, parts) in FILES.items():',
              "    data = gzip.decompress(base64.b64decode(''.join(parts)))",
              '    good = hashlib.sha256(data).hexdigest() == sha',
              '    ok &= good',
              '    os.makedirs(os.path.dirname(os.path.join(ROOT, path)), exist_ok=True)',
              "    open(os.path.join(ROOT, path), 'wb').write(data)",
              "    print('%s  %s  %s' % ('ok ' if good else 'BAD', sha, path))",
              'os.chdir(ROOT)',
              "print('\\nall files written and checked' if ok else '\\nCHECKSUM MISMATCH')",
              "!nproc; lscpu | grep -E 'Model name|Vendor ID'"]
    cells = [
        md("""
# Independent verification of g₃(7) = 474 (Erdős Problem #817), self-contained

This version needs **no GitHub access and no token**. It contains compressed copies of the verification program,
the search program and the published count table, taken from commit `%s` of the repository. Cell 1 unpacks them
and prints their SHA-256, which you can compare with the files in the repository. A CPU runtime is enough.

| step | what it checks | time on a standard Colab CPU runtime |
| --- | --- | --- |
| 2. quick | certificates (from the definition), Lemma 1, g₃(5) = 60, g₃(6) = 168, exhaustive search at N = 473 and 474 | ~10–15 min |
| 3. critical | exhaustive search for **every** N = 419…478, compared with the published count table | a few hours |
| 4. full (optional) | every N = 1…478 (does not rely on Korsky's bound g₃(7) ≥ 419) | +1–2 h |
| 5. Rust (optional) | the independent Rust implementation at N = 473, 474 | ~15 min |

Each value of N is logged separately. If the runtime disconnects, run cell 1 again, then the same step; finished
values are skipped, as long as the logs are on Google Drive (step 3).
""" % commit[:12]),
        md("## 1. Unpack the programs and data"),
        code('\n'.join(embed)),
        md("## 2. Quick verification (~10–15 min)"),
        code("!python3 verify/verify_result.py quick --out /content/verify_run/quick"),
        md("""## 3. The whole critical range N = 419…478 (a few hours)
Logs go to Google Drive so they survive a disconnect. After a disconnect, run cell 1 and this cell again."""),
        code("""
from google.colab import drive
drive.mount('/content/drive')
OUT = '/content/drive/MyDrive/g3_7_verify_run'
!python3 verify/verify_result.py critical --out {OUT}/critical
"""),
        md("## 4. (optional) Every N = 1…478"),
        code("""
from google.colab import drive
drive.mount('/content/drive')
OUT = '/content/drive/MyDrive/g3_7_verify_run'
!python3 verify/verify_result.py full --out {OUT}/full
"""),
        md("## 5. (optional) The independent Rust implementation at N = 473 and 474"),
        code("""
!curl -sSf https://sh.rustup.rs | sh -s -- -y --profile minimal > /dev/null
import os; os.environ['PATH'] += ':/root/.cargo/bin'
!python3 verify/verify_result.py quick --rust --out /content/verify_run/quick
"""),
        md("""## What the result means
* **quick** confirms the upper bound (the certificate is checked directly from the definition) and that the two
  decisive values N = 473 and 474 behave as claimed, with full count vectors matching the published table.
* **critical** (with Korsky's bound) or **full** (without it) re-establishes the lower bound: no admissible 7-set
  with maximum ≤ 473.
* If you post about the result, say what you ran. The Erdős Problems forum asks that claims be verified by a human
  and that AI assistance be disclosed.
"""),
    ]
    nb = {"cells": cells,
          "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                       "language_info": {"name": "python"}, "colab": {"provenance": []}},
          "nbformat": 4, "nbformat_minor": 4}
    with open(OUT, 'w', encoding='ascii', newline='\n') as f:
        json.dump(nb, f, indent=1, ensure_ascii=True)
        f.write('\n')
    print('wrote', OUT, 'from commit', commit[:12], 'with', len(FILES), 'embedded files')


if __name__ == '__main__':
    main()
