# Build all programs.  Requirements: gcc (x86-64 with BMI2 for g3fast2; the portable reference g3search
# needs nothing special), Rust toolchain (cargo) for the independent verifier, Python 3 for checks.
CC ?= gcc
CFLAGS ?= -O3 -march=native

all: bin/g3fast2 bin/g3fast2_noroom bin/g3search bin/gk_search bin/g3verify

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

bin/g3verify: verify/g3verify_rs/src/main.rs verify/g3verify_rs/Cargo.toml | bin
	cd verify/g3verify_rs && cargo build --release
	cp verify/g3verify_rs/target/release/g3verify $@

clean:
	rm -rf bin verify/g3verify_rs/target

.PHONY: all clean
