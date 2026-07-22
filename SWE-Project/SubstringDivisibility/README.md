# Substring Divisibility

A C++ solution to Project Euler #43, which asks: among all pandigital permutations of the digits 0–9, find those where a specific sequence of overlapping 3-digit substrings are each divisible by a distinct prime number.

## Overview

For a 10-digit number `d1 d2 d3 ... d10` formed from a permutation of 0–9, define `d2d3d4` as its 1st substring, `d3d4d5` as its 2nd substring, and so on. This program finds every permutation satisfying:

| Substring | Divisible by |
|---|---|
| d2 d3 d4 | 2 |
| d3 d4 d5 | 3 |
| d4 d5 d6 | 5 |
| d5 d6 d7 | 7 |
| d6 d7 d8 | 11 |
| d7 d8 d9 | 13 |
| d8 d9 d10 | 17 |

The program takes any string of 4–10 unique digits, generates every valid permutation via exhaustive search, prints each one that satisfies all applicable substring rules, and reports the sum of all valid permutations found.

## Example

**Input:**
```
0123456789
```

**Output (abridged):**
```
1406357289
4106357289
4160357289
1460357289
1430952867
4130952867
Sum: 16695334890
```

## Key Implementation Details

- **Heap's algorithm** — generates every permutation of the input digits using an iterative, minimal-swap approach, avoiding the overhead of recursive permutation generation or storing all permutations in memory at once.
- **Substring divisibility check** — for each generated permutation, walks through the overlapping 3-digit windows and checks each one against its corresponding prime, short-circuiting the check as soon as any window fails.
- **Big-number-safe summation** — accumulates the sum using `unsigned long long`, since the sum of even a handful of 10-digit numbers can approach the limits of 64-bit integers.
- **General input size** — works for any digit-string length from 4 to 10, not just the full 10-digit pandigital case, adjusting which divisibility rules apply based on the input length.

## Usage

Build with the included `Makefile`:
```bash
make all
```

Run against a digit string:
```bash
./SubstringDivisibility/substringdivisibility 0123456789
```
