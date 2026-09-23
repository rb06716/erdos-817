# Build all programs.  Requirements: a C compiler (make's default `cc`, i.e. gcc or clang; override with
# `make CC=...`), Rust >= 1.75 with cargo for the independent verifier, Python 3, and NumPy (requirements.txt)
# for `make check`.  g3fast2 and g3profile use the BMI2 PEXT instruction when -march=native enables it and an
# equivalent portable code path otherwise (e.g. ARM / Apple Silicon: make CFLAGS="-O3 -mcpu=native").
CFLAGS ?= -O3 -march=native

all: bin/g3fast2 bin/g3fast2_noroom bin/g3search bin/gk_search bin/gk_verify bin/g3profile bin/g3verify

bin:
	mkdir -p bin

bin/g3fast2: src/g3fast2.c | bin
	$(CC) $(CFLAGS) -o $@ $<

bin/g3fast2_noroom: src/g3fast2.c | bin
	$(CC) $(CFLAGS) -DNOROOM -o $@ $<

bin/g3search: src/g3search.c | bin
	$(CC) $(CFLAGS) -o $@ $<

bin/gk_search: src/gk_search.c | bin
	$(CC) $(CFLAGS) -o $@ $<

bin/gk_verify: verify/gk_verify.c | bin
	$(CC) $(CFLAGS) -o $@ $<

bin/g3profile: src/g3profile.c | bin
	$(CC) $(CFLAGS) -o $@ $<

bin/g3verify: verify/g3verify_rs/src/main.rs verify/g3verify_rs/Cargo.toml | bin
	cd verify/g3verify_rs && cargo build --release
	cp verify/g3verify_rs/target/release/g3verify $@

# fast consistency checks (about 2 minutes): definition vs. programs, C vs. Rust, certificates, known values
check: bin/g3fast2 bin/g3fast2_noroom bin/g3verify bin/gk_search bin/gk_verify
	bash tests/run_checks.sh

# independent-verifier entry point: certificates + the decisive values N = 473, 474 (5-15 minutes);
# use `python3 verify/verify_result.py critical` (hours) to re-run every N = 419..478
verify:
	python3 verify/verify_result.py quick

clean:
	rm -rf bin verify/g3verify_rs/target

.PHONY: all check verify clean
