# Software Engineering Projects

A collection of C++ programming projects focused on algorithmic problem-solving, low-level data representation, and efficient exhaustive search — implemented without relying on high-level built-in libraries for the core logic.

## Projects

### [LargeSum](./LargeSum)
Implements arbitrary-precision integer addition from scratch, summing large non-negative integers (up to 50 digits each) that exceed the range of native integer types. Built around manual digit-by-digit arithmetic with explicit carry propagation.

**Highlights:** custom big-integer arithmetic, no arbitrary-precision libraries, edge-case handling (empty input, leading zeros, short sums).

### [SubstringDivisibility](./SubstringDivisibility)
Solves Project Euler #43 — finding permutations of digits where overlapping 3-digit substrings satisfy a chain of divisibility rules against a sequence of primes.

**Highlights:** Heap's algorithm for permutation generation, substring-based divisibility checks, efficient exhaustive search over the full permutation space.

## Getting Started

Each project folder contains its own source file, `README.md` with details, and (for LargeSum) a set of test cases. Build both projects from the repository root:

```bash
make all
```

This produces:
```
LargeSum/largesum
SubstringDivisibility/substringdivisibility
```

Run either binary directly, passing the relevant input:

```bash
./LargeSum/largesum path/to/input.txt
./SubstringDivisibility/substringdivisibility 0123456789
```

To remove built binaries:
```bash
make clean
```

## Skills Demonstrated

- Manual implementation of algorithms typically hidden behind language built-ins (big-integer arithmetic, permutation generation)
- Efficient exhaustive search techniques
- C++ fundamentals: file I/O, vectors, careful edge-case handling
- Build automation with Makefiles across a multi-project repository
