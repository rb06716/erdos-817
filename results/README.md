# Results index

Log line formats: C programs print `N=<N> n=<n> solutions=<s> nodes: V_1 … V_n time=<s>`; the Rust verifier prints
`N=<N> n=<n> V: V_1 … V_n solutions=<s>`; every admissible set found is printed as `SOLUTION N=<N> {…}`.
With `-DNOROOM` (C) and always (Rust), `V_k` = number of admissible k-subsets of [1..N] that contain N.

| path | content |
| --- | --- |
| `n7_counts.csv` | **canonical counts V_1..V_7 for n = 7, N = 1..478** (C; identical in Rust) |
| `n7_counts_c_419-478.csv` | the same for N = 419..478 only (first table produced) |
| `SHA256SUMS` | checksums of all logs/tables (regenerate with `scripts/finalize.sh`) |
| `n7_scan/` | **main C run**, `g3fast2 -DNOROOM`, N = 419..478 (4 interleaved processes) |
| `n7_c_lo/` | C run, N = 1..418 |
| `n7_verify_rust_hi/` | **independent Rust run**, N = 419..478 |
| `n7_verify_rust_lo/` | Rust run, N = 1..418 |
| `n7_band_crosscheck/` | C vs Rust, all admissible 7-sets with max N ∈ [474, 520] and other elements ≥ 0.55 N (12,010 sets) |
| `n7_reference_check/` | reference `g3search.c` vs `g3fast2` (room-pruned mode) at N = 473, 474 |
| `n7_roompruned_partial/` | first (room-pruned) scan N = 419..434, superseded by `n7_scan/` |
| `n7_probe/` | band probe that found the upper-bound set at N = 474 (not part of the proof) |
| `thirdparty_check/` | third-party `g3.c` (firesh audit repository) at n = 7, N = 200 |
| `certificates/` | sorted ternary sums / subset sums and SHA-256 of the certificate sets (n = 7, n = 8) |
| `n8_upper/` | n = 8 construction searches (band, profile windows, beam) — upper bounds only |
| `gk/` | k = 4, 5 computations (`gk_search`, `gk_verify`), including the partial g_4(7) search |
