# MathExpr
A C++ program that finds the shortest sequence of "multiply by 2" and "divide by 3" (integer division) operations needed to go from `1` to a given non-negative integer target, by exploring the operation space with breadth-first search.
## Overview
Starting from `1`, only two operations are allowed at each step: multiply the current value by 2, or divide it by 3 (using integer/floor division). The goal is to reach a given `target` value in as few operations as possible.
Because each operation branches into two possible next states, a naive depth-first exploration could wander down long, non-optimal paths before finding the target. BFS explores the state space level-by-level, so the first time the target is reached is guaranteed to be via the shortest possible sequence of operations. A hash set of previously-visited values prevents revisiting the same state and keeps the search from growing unbounded (in particular, avoiding the `x2`/`/3` cycle repeatedly bouncing around the same handful of values).
The program takes a single non-negative integer as a command-line argument and prints the resulting expression, starting from `1` and followed by each operation applied, in order.
## Example
**Input:**
```bash
./mathexpr 100
```
**Output:**
```
1 x 2 x 2 x 2 x 2 x 2 x 2 x 2 x 2 x 2 x 2 x 2 x 2 / 3 / 3 / 3 x 2 / 3
```
## Key Implementation Details
- **Breadth-first search over the operation space** — each state in the queue pairs a reachable value with the sequence of operations used to reach it; the queue's FIFO order guarantees the first path to reach `target` is the shortest.
- **Visited-state tracking** — an `unordered_set<int>` records every value already enqueued, so the search never re-explores a state and terminates even when operations cycle back toward earlier values.
- **Input validation** — rejects missing arguments, extra arguments, negative numbers, and any non-digit input before running the search.
- **No output on unreachable targets** — if the queue is exhausted without finding `target`, an empty operation path is returned and only the starting `1` is printed.
## Usage
Build everything with the included `Makefile`:
```bash
make all
```
Or build just this project:
```bash
make mathexpr
```
Run against a target integer:
```bash
./MathExpr/mathexpr 100
```