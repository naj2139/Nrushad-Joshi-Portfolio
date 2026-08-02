# Recursion Fundamentals

A collection of beginner-friendly recursive algorithms implemented in Python to build a strong foundation in recursion.

The goal of this repository is not only to solve recursion problems, but also to understand **how recursive thinking works** by breaking each problem into smaller subproblems and tracing how recursive calls are evaluated.

## Approach

This implementation focuses on the fundamental building blocks of recursion using simple toy problems.

Each solution is designed to teach a single recursion concept and includes:

* A brief explanation of the recursion concept.
* A recursion expansion showing how recursive calls are evaluated.
* Comments explaining the base case and recursive step.

Topics covered include:

* Printing numbers
* Sum of the first *n* numbers
* Factorial
* Reverse string
* Digit sum
* Count digits
* Palindrome checking

## Example

Each solution contains a recursion expansion similar to the following.

```text
reverse_string("Hello")
= reverse_string("ello") + "H"
= (reverse_string("llo") + "e") + "H"
= ((reverse_string("lo") + "l") + "e") + "H"
= (((reverse_string("o") + "l") + "l") + "e") + "H"
= (((("o") + "l") + "l") + "e") + "H"
= "olleH"
```

This helps visualize how recursive calls are expanded and then evaluated while the call stack unwinds.

## Usage

```bash
python Recursion101.py
```

## Learning Objectives

Through these exercises, I develop an understanding of how to:

- Identify an appropriate base case.
- Reduce a problem into a smaller subproblem.
- Understand how the call stack works.
- Trace recursive execution.
- Distinguish between recursion that performs an action and recursion that returns a value.
- Apply recursion to numbers, strings, and digits.