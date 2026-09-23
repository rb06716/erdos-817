//! g3verify -- independent re-implementation of the exhaustive search for g_3(n)
//! (Erdos Problem #817, OEIS A399720), written separately from src/g3search.c / src/g3fast2.c.
//!
//! Admissible set: A = {a_1..a_n} positive integers such that sum_i c_i a_i != 0 for every nonzero
//! c in {-2,-1,0,1,2}^n  (equivalently the 3^n sums sum_i e_i a_i, e in {0,1,2}^n, are distinct).
//!
//! Differences from the C programs (deliberate, for independence):
//!   * search order: the maximum N first, then the remaining elements in DECREASING order;
//!   * no "room" pruning: every admissible k-subset of [1..N] that contains N is visited, so the
//!     per-depth counts V_k(N) are canonical (independent of search order);
//!   * difference sets stored as symmetric windows [-rad, rad] with rad chosen per level;
//!   * written in Rust with plain word loops (no PEXT, no windowed last level).
//!
//! Output line per N:  "N=<N> n=<n> V: V_1 V_2 ... V_n solutions=<V_n>"
//! plus one "SOLUTION" line per admissible n-set with maximum N.
//!
//! usage: g3verify n Nlo Nhi [step] [offset] [minelem_permille]
//!        (minelem_permille > 0 restricts elements other than N to >= floor(N*pm/1000); cross-checks only)

use std::env;
use std::io::Write;

struct Search {
    n: usize,
    big_n: i64,
    // bitsets: index = position + off (as bit index); off = rad of level 0 (largest radius)
    off: i64,
    #[allow(dead_code)]
    words: usize,
    levels: Vec<Vec<u64>>,
    dirty: Vec<(usize, usize)>, // word range of levels[l] that may be nonzero
    rad: Vec<i64>,      // radius needed at level L (L chosen elements)
    elems: Vec<i64>,
    counts: Vec<u64>,
    sols: Vec<Vec<i64>>,
    minelem: i64,   // all elements other than N must be >= minelem (1 = exhaustive)
}

impl Search {
    fn bit(&self, lvl: usize, p: i64) -> bool {
        let q = (p + self.off) as usize;
        (self.levels[lvl][q >> 6] >> (q & 63)) & 1 == 1
    }

    /// levels[lvl+1] = levels[lvl] + {0, +-a, +-2a}, computed exactly on [-rad, rad] (rad = self.rad[lvl+1]),
    /// clipped to the true support [-2*sum, 2*sum]; zero elsewhere.
    fn expand(&mut self, lvl: usize, a: i64, sum: i64) {
        let r = std::cmp::min(self.rad[lvl + 1], 2 * sum);
        let lo_bit = (-r + self.off) as usize;
        let hi_bit = (r + self.off) as usize;
        let lo_w = lo_bit >> 6;
        let hi_w = hi_bit >> 6;
        let (src_part, dst_part) = self.levels.split_at_mut(lvl + 1);
        let src: &[u64] = &src_part[lvl];
        let dst: &mut [u64] = &mut dst_part[0];
        // zero whatever the previous node at this level left outside the new window
        let (dlo, dhi) = self.dirty[lvl + 1];
        for i in dlo..std::cmp::min(lo_w, dhi + 1) {
            dst[i] = 0;
        }
        for i in std::cmp::max(hi_w + 1, dlo)..=dhi {
            dst[i] = 0;
        }
        self.dirty[lvl + 1] = (lo_w, hi_w);
        // arrays are padded with >= 2N/64 + 2 zero words on each side, so all slices below are in range.
        // dst[lo..=hi] = src | src<<a | src>>a | src<<2a | src>>2a, done as five branch-free slice passes.
        dst[lo_w..=hi_w].copy_from_slice(&src[lo_w..=hi_w]);
        for m in 1..=2usize {
            let sh = m * a as usize;
            let (ws, bs) = (sh >> 6, (sh & 63) as u32);
            let len = hi_w - lo_w + 1;
            let d = &mut dst[lo_w..=hi_w];
            // toward higher positions: result bit p = src bit p - sh
            let up0 = &src[lo_w - ws..lo_w - ws + len];
            if bs == 0 {
                for (dv, &s0) in d.iter_mut().zip(up0.iter()) {
                    *dv |= s0;
                }
            } else {
                let up1 = &src[lo_w - ws - 1..lo_w - ws - 1 + len];
                for ((dv, &s0), &s1) in d.iter_mut().zip(up0.iter()).zip(up1.iter()) {
                    *dv |= (s0 << bs) | (s1 >> (64 - bs));
                }
            }
            // toward lower positions: result bit p = src bit p + sh
            let dn0 = &src[lo_w + ws..lo_w + ws + len];
            if bs == 0 {
                for (dv, &s0) in d.iter_mut().zip(dn0.iter()) {
                    *dv |= s0;
                }
            } else {
                let dn1 = &src[lo_w + ws + 1..lo_w + ws + 1 + len];
                for ((dv, &s0), &s1) in d.iter_mut().zip(dn0.iter()).zip(dn1.iter()) {
                    *dv |= (s0 >> bs) | (s1 << (64 - bs));
                }
            }
        }
        // clear bits outside [lo_bit, hi_bit] in the two boundary words
        let lo_mask_bits = lo_bit & 63;
        if lo_mask_bits != 0 {
            dst[lo_w] &= !((1u64 << lo_mask_bits) - 1);
        }
        let hi_keep = (hi_bit & 63) + 1;
        if hi_keep < 64 {
            dst[hi_w] &= (1u64 << hi_keep) - 1;
        }
    }


    /// bits of levels[lvl] at positions start, start+1, ..., start+63 (one word, unaligned read)
    fn word_at(&self, lvl: usize, start: i64) -> u64 {
        let q = (start + self.off) as usize;
        let (w, b) = (q >> 6, (q & 63) as u32);
        let d = &self.levels[lvl];
        if b == 0 { d[w] } else { (d[w] >> b) | (d[w + 1] << (64 - b)) }
    }

    /// Last level without materialising D_{n-1}: the (n-1)-th element a has just been accepted
    /// (so the chosen set is elems[0..n-1] and levels[lvl] = D_{n-2}); count every x in [1, a-1]
    /// such that x and 2x avoid D_{n-1} = D_{n-2} + {0, +-a, +-2a}.
    fn last_level(&mut self, lvl: usize, a: i64) {
        let n = self.n;
        let mut base: i64 = self.minelem;
        while base <= a - 1 {
            let len = std::cmp::min(64, a - base);
            // forbidden[x - base] = 1 if x - j*a in D for some j
            let mut forb: u64 = 0;
            for j in -2i64..=2 {
                forb |= self.word_at(lvl, base - j * a);
            }
            let mut free = !forb;
            if len < 64 {
                free &= (1u64 << len) - 1;
            }
            while free != 0 {
                let t = free.trailing_zeros() as i64;
                free &= free - 1;
                let x = base + t;
                let mut ok = true;
                for j in -2i64..=2 {
                    if self.bit(lvl, 2 * x - j * a) {
                        ok = false;
                        break;
                    }
                }
                if ok {
                    self.counts[n] += 1;
                    self.elems[n - 1] = x;
                    let mut s: Vec<i64> = self.elems[..n].to_vec();
                    s.sort();
                    self.sols.push(s);
                }
            }
            base += 64;
        }
    }

    fn run(&mut self, lvl: usize, prev: i64, sum: i64) {
        // lvl = number of chosen elements; choose the next element x < prev (decreasing order).
        // Candidates are found by scanning the complement of D_lvl word by word over positions
        // [1, prev-1], from high to low; each zero bit x is then tested for 2x notin D_lvl.
        if lvl == self.n {
            return;
        }
        let lo_bit = (self.minelem + self.off) as usize;
        let hi_bit = (prev - 1 + self.off) as usize;
        if prev - 1 < self.minelem {
            return;
        }
        let lo_w = lo_bit >> 6;
        let hi_w = hi_bit >> 6;
        let mut w = hi_w as i64;
        while w >= lo_w as i64 {
            let wi = w as usize;
            let mut free = !self.levels[lvl][wi];
            if wi == hi_w {
                let keep = (hi_bit & 63) + 1;
                if keep < 64 {
                    free &= (1u64 << keep) - 1;
                }
            }
            if wi == lo_w {
                free &= !((1u64 << (lo_bit & 63)) - 1);
            }
            while free != 0 {
                let t = 63 - free.leading_zeros() as usize; // highest set bit first
                free &= !(1u64 << t);
                let x = (wi * 64 + t) as i64 - self.off;
                if self.bit(lvl, 2 * x) {
                    continue;
                }
                self.counts[lvl + 1] += 1;
                self.elems[lvl] = x;
                if lvl + 1 == self.n {
                    let mut s: Vec<i64> = self.elems[..self.n].to_vec();
                    s.sort();
                    self.sols.push(s);
                } else if lvl + 2 == self.n {
                    self.last_level(lvl, x);
                } else {
                    self.expand(lvl, x, sum + x);
                    self.run(lvl + 1, x, sum + x);
                }
            }
            w -= 1;
        }
    }
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 4 {
        eprintln!("usage: g3verify n Nlo Nhi [step=1] [offset=0] [minelem_permille=0]");
        std::process::exit(2);
    }
    let n: usize = args[1].parse().unwrap();
    let nlo: i64 = args[2].parse().unwrap();
    let nhi: i64 = args[3].parse().unwrap();
    let step: i64 = if args.len() > 4 { args[4].parse().unwrap() } else { 1 };
    let offset: i64 = if args.len() > 5 { args[5].parse().unwrap() } else { 0 };
    // optional band restriction (upper-bound / last-level cross-checks only): per mille of N
    let minelem_pm: i64 = if args.len() > 6 { args[6].parse().unwrap() } else { 0 };
    assert!(n >= 2 && n <= 12);
    let stdout = std::io::stdout();
    let mut out = stdout.lock();
    let mut big_n = nlo + offset;
    while big_n <= nhi {
        // radius needed at level L: the next element x satisfies x < N, and we must read D_L at x and 2x
        // (<= 2N); computing D_{L+1} on [-r, r] needs D_L on [-r-2N, r+2N].
        // radius needed at level L: D_L is read at x and 2x (x < N) when choosing the next element; the last
        // materialised level n-2 is also read at x - j*a and 2x - j*a (x < a < N, |j| <= 2): |pos| <= 4N+64.
        // Computing D_{L+1} on [-r, r] needs D_L on [-r-2N, r+2N].
        let mut rad = vec![0i64; n + 1];
        rad[n - 1] = 2 * big_n + 2;
        if n >= 2 {
            rad[n - 2] = 4 * big_n + 128;
        }
        for l in (0..n.saturating_sub(2)).rev() {
            rad[l] = rad[l + 1] + 2 * big_n;
        }
        rad[n] = 0;
        let pad_bits = 64 * ((2 * big_n) / 64 + 4);
        let off = rad[0] + pad_bits;
        let words = ((2 * off + 1) as usize + 63) / 64 + 4;
        let mut st = Search {
            n,
            big_n,
            off,
            words,
            levels: vec![vec![0u64; words]; n + 1],
            dirty: vec![(0usize, words - 1); n + 1],
            rad,
            elems: vec![0; n + 1],
            counts: vec![0; n + 1],
            sols: Vec::new(),
            minelem: std::cmp::max(1, big_n * minelem_pm / 1000),
        };
        // level 0: D_0 = {0}
        let q = st.off as usize;
        st.levels[0][q >> 6] |= 1u64 << (q & 63);
        // choose the maximum N (always admissible as a 1-set)
        st.counts[1] = 1;
        st.elems[0] = big_n;
        if n == 1 {
            st.sols.push(vec![big_n]);
        } else {
            st.expand(0, big_n, big_n);
            st.run(1, big_n, big_n);
        }
        let _ = st.big_n;
        for s in &st.sols {
            let strs: Vec<String> = s.iter().map(|v| v.to_string()).collect();
            writeln!(out, "SOLUTION N={} {{{}}}", big_n, strs.join(",")).unwrap();
        }
        let cs: Vec<String> = st.counts[1..=n].iter().map(|v| v.to_string()).collect();
        writeln!(out, "N={} n={} V: {} solutions={}", big_n, n, cs.join(" "), st.sols.len()).unwrap();
        out.flush().unwrap();
        big_n += step;
    }
}
