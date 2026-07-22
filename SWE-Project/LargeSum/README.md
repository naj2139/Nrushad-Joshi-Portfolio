# LargeSum

A C++ program that sums an arbitrary list of very large non-negative integers — numbers far too big to fit in any native integer type — by implementing big-integer addition from scratch, without relying on any built-in arbitrary-precision library.

## Overview

Standard integer types (`int`, `long long`, etc.) top out at a fixed number of digits, and even `unsigned long long` can't represent a 50-digit number. This project solves that by representing each number as a sequence of individual digits and performing addition manually, digit-by-digit, with explicit carry propagation — the same process taught for adding numbers by hand, implemented programmatically.

The program reads any number of large integers (up to 50 digits each) from an input file, sums them all, and reports:
- The full exact sum
- The first 10 significant digits of that sum

## Example

**Input** (`input.txt`):
```
37107287533902102798797998220837590246510135740250
46376937677490009712648124896970078050417018260538
74324986199524741059474233309513058123726617309629
```

**Output:**
```
Full sum: 157809211410916853570920356427320726420653771310417
First 10 digits: 1578092114
```

## Key Implementation Details

- **Manual big-integer arithmetic** — no `BigInteger`, no arbitrary-precision library. Each number is stored as a vector of individual digits, and addition is performed with manual carry propagation across positions.
- **Fixed-width digit buffer** — a working array sized to comfortably hold the largest possible sum (up to 50-digit numbers, plus headroom for carry overflow across many summed values), avoiding dynamic resizing during the hot loop.
- **Edge case handling** — correctly handles an empty input file, a sum of exactly zero, sums with fewer than 10 significant digits, and leading zeros in the input or result.
- **Efficient I/O** — disables C++/C stdio synchronization (`ios::sync_with_stdio(false)`) for faster line-by-line file reads.

## Usage

Build with the included `Makefile`:
```bash
make all
```

Run against an input file:
```bash
./LargeSum/largesum path/to/input.txt
```

