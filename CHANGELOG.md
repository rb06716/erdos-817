# Changelog

Notable changes to the results, programs and documentation. The detailed history, including every correction, is in
[docs/research_log.md](docs/research_log.md).

## Unreleased

* `docs/HOW_THIS_WAS_PRODUCED.md`: how the work was produced by an AI agent from one prompt (timeline, every human
  intervention, mistakes and corrections, verification status, credit); `docs/ORIGINAL_PROMPT.md`: the prompt,
  verbatim. README section and CITATION.cff abstract updated to match.

## v1.0.0 — 2026-09-23

First public version. Archived on Zenodo: https://doi.org/10.5281/zenodo.22925446 (all versions:
https://doi.org/10.5281/zenodo.22925445).

**Results**
* `g₃(7) = 474`, with `{302, 409, 447, 459, 465, 466, 474}` the unique extremal set. The upper bound is a
  certificate; the lower bound and uniqueness come from exhaustive searches by two independent programs (C and
  Rust), which agree on the canonical counts for every N ≤ 478 (`results/n7_counts.csv`).
* Certified upper bounds `g₃(8..14) ≤ 1368, 3974, 11578, 34088, 100422, 295924, 879824` (hole chains); conjecture
  `g₃(8) = 1368`.
* `g₄(1..7) = 1, 3, 5, 14, 40, 79, 225` and `g₅(1..8) = 1, 2, 4, 6, 14, 22, 60, 92` (two independent programs).
* Correction: the minimal 6-set claimed by Bae (2002) and Bae–Choi (2003) has maximum 169, but `g₃(6) = 168`.

**Verification**
* `verify/verify_result.py` (quick / critical / full, optionally with the Rust verifier), Colab notebooks,
  `make check` (12 consistency checks) and GitHub Actions.
* The critical range N = 419…478 was re-run by the repository owner on Google Colab: all 60 count vectors
  identical to the published table.

**Credit** (see [docs/PRIOR_ART.md](docs/PRIOR_ART.md))
* The upper bound `g₃(7) ≤ 474`, with the same set, was first posted by carlomitchener (Erdős Problems forum,
  23 Sep 2026); `g₃(7) ≤ 477` was implicit in Bae (2002).
* The offset form of the small optima was first noted by M. Czech (forum, 9 Sep 2026).
