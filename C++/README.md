# Software Engineering Projects
A collection of C++ programming projects focused on algorithmic problem-solving, low-level data representation, and efficient exhaustive search — implemented without relying on high-level built-in libraries for the core logic.
## Projects
### [LargeSum](./LargeSum)
Solves Project Euler #13 — implements arbitrary-precision integer addition from scratch, summing large non-negative integers (up to 50 digits each) that exceed the range of native integer types. Built around manual digit-by-digit arithmetic with explicit carry propagation.
**Highlights:** custom big-integer arithmetic, no arbitrary-precision libraries, edge-case handling (empty input, leading zeros, short sums).
### [SubstringDivisibility](./SubstringDivisibility)
Solves Project Euler #43 — finding permutations of digits where overlapping 3-digit substrings satisfy a chain of divisibility rules against a sequence of primes.
**Highlights:** Heap's algorithm for permutation generation, substring-based divisibility checks, efficient exhaustive search over the full permutation space.
### [Contacts](./Contacts)
Solves the HackerRank Data Structures "Contacts" problem — a trie-based lookup supporting prefix counting and whole-word search over a set of contact names.
**Highlights:** trie (prefix tree) construction, O(prefix length) prefix-count queries, shared sentinel node for end-of-word marking.
### [MathExpr](./MathExpr)
Finds the shortest sequence of "multiply by 2" / "divide by 3" (integer division) operations needed to reach a target integer starting from 1, using breadth-first search over the operation space.
**Highlights:** BFS-based shortest-path search, visited-state tracking to avoid infinite cycles, guaranteed-shortest operation sequence.
## Getting Started
Build all projects from the repository root:
```bash
make all
```
Or build a single project on its own:
```bash
make largesum
make subdiv
make contacts
make mathexpr
```
To remove built binaries:
```bash
make clean
```
## Skills Demonstrated
- Manual implementation of algorithms typically hidden behind language built-ins (big-integer arithmetic, permutation generation, trie-based prefix search)
- Efficient exhaustive search techniques
- C++ fundamentals: file I/O, vectors, careful edge-case handling