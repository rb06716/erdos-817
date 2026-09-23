# scripts/

Helper scripts. Run them from the repository root, e.g. `python3 scripts/beam.py 300 12 8 40`. The search
programs themselves are in `src/` and `verify/`. The construction scripts need NumPy
(`python3 -m pip install -r requirements.txt`); the others use only the standard library.

## Running and comparing the exhaustive searches

| script | purpose |
| --- | --- |
| `run_range.sh PROGRAM n NLO NHI JOBS OUTDIR` | run the C (`bin/g3fast2_noroom`) or Rust (`bin/g3verify`) search for `N = NLO..NHI` in `JOBS` parallel processes |
| `aggregate.py table n LOGS...` | build the canonical count table (`N, V_1..V_n, solutions`) from search logs |
| `aggregate.py compare n --c LOGS... --rust LOGS...` | compare C and Rust logs value by value (count vectors and solution lists); exit status 1 on any mismatch |
| `verify_pipeline.sh JOBS` | the full n = 7 computation, in the order it was run (C and Rust, N = 1..478) |
| `finalize.sh` | rebuild `results/n7_counts.csv`, repeat all C-vs-Rust comparisons, check the certificates, rewrite `results/SHA256SUMS` |
| `make_standalone_notebook.py` | rebuild `verify/colab_verify_standalone.ipynb` from the committed files (git HEAD) |

## Constructions (upper bounds only; never used for a lower bound)

| script | purpose |
| --- | --- |
| `holes_all.py`, `hole_dp.py` | admissible maxima ("holes") `M` for an offset set `B`, i.e. those with `{M} ∪ {M − b}` admissible |
| `beam.py W K NMAX S0` | beam search over hole chains: reproduces 8, 22, 60, 168, 474 and gives the n = 8…14 bounds |
| `offset_recursion.py`, `seeds.py` | greedy first-hole chains from the known optima, or from every seed |
| `offset_localsearch.py [seed] [iterations]` | randomized local search over n = 8 offset sets |
| `offset_analysis.py` | offset-form analysis of a given set (default: the n = 7 extremal set) |
| `conway_guy_ternary.py` | Conway–Guy-type recurrences `u_{n+1} = 3u_n − u_{n−r}` (the prior-art comparison in `docs/PRIOR_ART.md`) |

## Other

| script | purpose |
| --- | --- |
| `summary_table.py` | table of exact values and bounds, Korsky's lower bound `b_n`, ratios `g_3(n)/3^n` |
| `oeis_novelty_check.py [oeisdata]` | search the official OEIS export for every value string in this package |
| `mc_valid.py` | early Monte Carlo sizing of the n = 7 search (superseded by the exact counts) |
