# Erdős Problem #817: exact values of the Erdős–Sárközy function

[![checks](https://github.com/rb06716/erdos-817/actions/workflows/checks.yml/badge.svg)](https://github.com/rb06716/erdos-817/actions/workflows/checks.yml)
[![verify](https://github.com/rb06716/erdos-817/actions/workflows/verify.yml/badge.svg)](https://github.com/rb06716/erdos-817/actions/workflows/verify.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

For a finite set `A` of positive integers, let `H(A) = {Σ_{a∈S} a : S ⊆ A}` be its set of subset sums. The
**Erdős–Sárközy function** `g_k(n)` is the least `N` such that some `n`-element set `A ⊆ {1,…,N}` has `H(A)`
free of non-constant `k`-term arithmetic progressions. It is the subject of
[Erdős Problem #817](https://www.erdosproblems.com/817), and `g_3` is OEIS [A399720](https://oeis.org/A399720).
This repository contains exhaustive searches, verification tools and data for small values.

**Status:** v1.0.0 (2026-09-23). The results below are complete, and the decisive computation was re-run by the
repository owner on separate hardware. They have not been peer-reviewed. Changes are listed in
[CHANGELOG.md](CHANGELOG.md).

## Main result

> **g₃(7) = 474**, and `{302, 409, 447, 459, 465, 466, 474}` is the only 7-element set attaining it.

The proof is computer-assisted:
* **Upper bound:** a certificate. The 3⁷ = 2187 sums `Σ εᵢaᵢ` with `εᵢ ∈ {0,1,2}` are pairwise distinct.
  This is checked directly, in milliseconds.
* **Lower bound:** an exhaustive search of every `N ≤ 473`, run by two independently written programs (C and
  Rust). They agree on the full per-level count vectors for every `N ≤ 478`.
* **Independent re-run:** the repository owner re-ran the critical range `N = 419…478` on separate hardware
  (Google Colab). All 60 count vectors were identical to the published table
  ([`results/external_verification/`](results/external_verification/)). This used the same code, so it guards
  against hardware and environment errors, not against a logic error shared by both runs.

**Credit.** The upper bound `g₃(7) ≤ 474`, with the same set, was first posted publicly by carlomitchener on the
Erdős Problems forum (23 Sep 2026); it was found independently here. A weaker bound, `g₃(7) ≤ 477`, was
implicit in J. Bae (2002), which uses an admissible 7-set with maximum 477. What is new here is the matching
lower bound and the uniqueness. This does not solve Erdős Problem #817 itself, which asks for an asymptotic
estimate of `g_k(n)`.

## Results

| quantity | value | status | details |
| --- | --- | --- | --- |
| g₃(1), …, g₃(6) | 1, 3, 8, 22, 60, 168 | known (Korsky 2026 for n ≤ 4; M. Czech 2026 for n = 5, 6); reproduced here | [A399720](https://oeis.org/A399720) |
| **g₃(7)** | **474**, unique extremal set | **new; computer-assisted proof** | [DISCOVERY](docs/DISCOVERY.md) |
| g₃(8), …, g₃(14) | ≤ 1368, 3974, 11578, 34088, 100422, 295924, 879824 | new certified upper bounds | [DISCOVERY](docs/DISCOVERY.md) |
| g₃(8) | = 1368? | conjecture (evidence only) | [DISCOVERY](docs/DISCOVERY.md), [feasibility study](research/pruning/NOTES.md) |
| g₄(1), …, g₄(7) | 1, 3, 5, 14, 40, 79, 225 | first published here (small n elementary); two independent programs | [DISCOVERY](docs/DISCOVERY.md) |
| g₅(1), …, g₅(8) | 1, 2, 4, 6, 14, 22, 60, 92 | first published here (small n elementary); two independent programs | [DISCOVERY](docs/DISCOVERY.md) |
| n = 6 claim of Bae (2002) and Bae–Choi (2003) | they state 169, but g₃(6) = 168 | correction | [DISCOVERY](docs/DISCOVERY.md) |

## Verify it yourself

Requirements: a C compiler (gcc or clang), Rust ≥ 1.75 with cargo (for the independent verifier), and Python 3
(tested with 3.11 and 3.12). The verification tools use only the Python standard library; the construction
scripts and `make check` also need NumPy (`python3 -m pip install -r requirements.txt`).

```sh
make all        # build the programs
make check      # ~2 min: 12 consistency checks (definition vs. programs, C vs. Rust, certificates, known values)
make verify     # 5-15 min: certificates and the decisive values N = 473, 474, compared with the published table
python3 verify/verify_result.py critical   # ~1 h on 8 cores: every N from Korsky's bound b_7 = 419 up to 478
```

No local setup is needed with Google Colab: `verify/colab_verify_standalone.ipynb` runs the same checks without
GitHub access. GitHub Actions runs `make check` on every push ([`checks.yml`](.github/workflows/checks.yml)), and
`verify_result.py quick` with both the C and the Rust program whenever the programs or the published data change
([`verify.yml`](.github/workflows/verify.yml)). Details: [docs/REPRODUCE.md](docs/REPRODUCE.md).

## How it works

1. **Reformulation.** Lemma 1 (proved in [docs/METHODS.md](docs/METHODS.md); also Korsky 2026, Prop. 4.1):
   `H(A)` has no non-constant 3-term progression iff the `3ⁿ` sums `Σ εᵢaᵢ` with `εᵢ ∈ {0,1,2}` are pairwise
   distinct. Such sets are called *admissible*.
2. **Search.** For each maximum `N`, every admissible set containing `N` is enumerated, one element at a time.
   A bitset of all `{−2,…,2}`-combinations of the chosen elements makes each extension test a pair of bit
   look-ups (Lemma 2).
3. **Verification by fingerprints.** The canonical counts `V_k(N)` are the numbers of admissible `k`-subsets
   of `[1, N]` containing `N` (e.g. `V₆(473) = 6,608,257,434`). They do not depend on the search order. An
   independently written Rust program, which searches in the opposite order, reproduces all of them
   (`results/n7_counts.csv`). Any re-implementation must match them exactly.

## Repository layout

```
├── src/                    search programs (C)
│   ├── g3fast2.c           main exhaustive search (-DNOROOM: canonical counts)
│   ├── g3search.c          portable reference search
│   ├── g3profile.c         profile-window search (n = 8 constructions)
│   ├── gk_search.c         search for general k (subset-sum bitset + AP test)
│   └── g3fast.c            earlier version, kept for provenance
├── verify/                 independent programs and verification tools
│   ├── g3verify_rs/        independent implementation in Rust (opposite search order)
│   ├── gk_verify.c         independent program for general k
│   ├── bruteforce.py       definition-level brute force for small cases
│   ├── check_set.py        certificate checker for a given set
│   ├── verify_result.py    one-command verification: quick / critical / full
│   └── colab_verify*.ipynb the same checks in Google Colab
├── tests/run_checks.sh     fast consistency checks (make check)
├── scripts/                runs, comparisons, constructions, novelty check (see scripts/README.md)
├── results/                logs of every run, count tables, certificates, checksums (see results/README.md)
├── research/pruning/       feasibility study and prototypes towards g₃(8)
├── docs/                   write-up (below)
└── Makefile, requirements.txt, CITATION.cff, LICENSE, CHANGELOG.md
```

## Documentation

| document | content |
| --- | --- |
| [docs/DISCOVERY.md](docs/DISCOVERY.md) | the result stated as a theorem, evidence, novelty, verification record, secondary results |
| [docs/METHODS.md](docs/METHODS.md) | proofs of the lemmas, the search and why it is exhaustive, constructions |
| [docs/REPRODUCE.md](docs/REPRODUCE.md) | how to rebuild and re-run everything |
| [docs/LIMITATIONS.md](docs/LIMITATIONS.md) | what is and is not established |
| [docs/PRIOR_ART.md](docs/PRIOR_ART.md) | literature, databases and forum; novelty assessment |
| [docs/research_log.md](docs/research_log.md) | chronological research log |
| [docs/SUBMISSION_DRAFTS.md](docs/SUBMISSION_DRAFTS.md) | drafts for the OEIS and the Erdős Problems forum |
| [results/README.md](results/README.md) | index of result files |
| [research/pruning/NOTES.md](research/pruning/NOTES.md) | how large the g₃(8) computation is, and ideas for reducing it |

## Reporting a problem

If any command gives a different result, please open an issue with the command, its output and your platform.
For the exhaustive search the per-`N` count vectors are fingerprints: a single differing value of `N` pinpoints
the problem (see "How it can be falsified" in [docs/DISCOVERY.md](docs/DISCOVERY.md)).

## Citing

If you use the results, programs or data, please cite this repository; see [CITATION.cff](CITATION.cff) or
GitHub's "Cite this repository" button. Please also cite the original sources: P. Erdős (1991), P. Erdős and
A. Sárközy, *Discrete Math.* 102 (1992), S. Korsky, arXiv:2606.24139 (2026), and OEIS A399720.

## License

MIT; see [LICENSE](LICENSE).

## Acknowledgements and AI disclosure

This work builds on:
* S. Korsky: the reformulation and the lower bound `g₃(n) ≥ b_n`;
* S. Costa: the answer to the "in particular" question;
* M. Czech: OEIS A399720, `g₃(5)`, `g₃(6)`, and the offset form of the small extremal sets;
* J. Bae (2002) and J. Bae and S. Choi (2003): 2-fold subset-sum-distinct sets (the admissible sets); Bae (2002)
  also gives an admissible 7-set with maximum 477;
* carlomitchener: the upper bound for n = 7;
* firesh: the audit repository, whose program was used as a third-party check;
* T. Bloom: the Erdős Problems site.

The search design, programs, computations and write-up were produced by an AI agent (Claude, Anthropic), working
with the repository owner, Ryan Brown, who re-ran the verification independently.
