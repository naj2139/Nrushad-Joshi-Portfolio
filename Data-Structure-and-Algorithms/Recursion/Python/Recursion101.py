# Key recursion concept:
# ----------------------
# A recursive call PAUSES the current function; it does NOT terminate it.
# Once the recursive call reaches the base case and returns, execution
# resumes at the next line after the recursive call.
#
# Recursion expansion (n = 3):
#
# print_numbers(3)
# ↓
# print_numbers(2)
# ↓
# print_numbers(1)
# ↓
# print_numbers(0)
# ↑ return
# print(1)
# ↑ return
# print(2)
# ↑ return
# print(3)

def print_numbers(n: int) -> None:

    # Base case: stop when there are no numbers left to print.
    if n == 0:
        return

    # Solve the smaller subproblem first.
    print_numbers(n - 1)

    # Executes while the recursive calls unwind, printing 1 -> n.
    print(n)


# Key recursion concept:
# ----------------------
# A recursive call can RETURN a value.
# Assume the recursive call already knows how to solve the smaller problem,
# then use its returned value to solve the current problem.
#
# Recursion expansion (n = 3):
#
# sum_numbers(3)
# = 3 + sum_numbers(2)
# = 3 + (2 + sum_numbers(1))
# = 3 + (2 + (1 + sum_numbers(0)))
# = 3 + (2 + (1 + 0))
# = 3 + (2 + 1)
# = 3 + 3
# = 6

def sum_numbers(n: int) -> int:

    # Base case: the sum of the first 0 numbers is 0.
    if n == 0:
        return 0

    # Sum of the first n numbers =
    # current number + sum of the first (n - 1) numbers.
    return n + sum_numbers(n - 1)


# Key recursion concept:
# ----------------------
# Assume the recursive call already knows how to solve the smaller problem,
# then use its returned value to solve the current problem.
#
# Recursion expansion (n = 4):
#
# factorial(4)
# = 4 * factorial(3)
# = 4 * (3 * factorial(2))
# = 4 * (3 * (2 * factorial(1)))
# = 4 * (3 * (2 * 1))
# = 4 * (3 * 2)
# = 4 * 6
# = 24

def factorial(n: int) -> int:

    # Base case: factorial of 0 (and 1) is 1.
    if n <= 1:
        return 1

    # Factorial of n =
    # current number × factorial of (n - 1).
    return n * factorial(n - 1)


# Key recursion concept:
# ----------------------
# Assume the recursive call already knows how to reverse the smaller string,
# then append the current character to build the reversed result.
#
# Recursion expansion ("Hello"):
#
# reverse_string("Hello")
# = reverse_string("ello") + "H"
# = (reverse_string("llo") + "e") + "H"
# = ((reverse_string("lo") + "l") + "e") + "H"
# = (((reverse_string("o") + "l") + "l") + "e") + "H"
# = (((("o") + "l") + "l") + "e") + "H"
# = "olleH"

def reverse_string(s: str) -> str:

    # Base case: an empty or single-character string is already reversed.
    if len(s) <= 1:
        return s

    # Reverse the remaining substring, then append the current character.
    return reverse_string(s[1:]) + s[0]

# Key recursion concept:
# ----------------------
# Assume the recursive call already knows how to sum the digits of the
# remaining number, then add the current (last) digit to that result.
#
# Recursion expansion (1234):
#
# digit_sum(1234)
# = 4 + digit_sum(123)
# = 4 + (3 + digit_sum(12))
# = 4 + (3 + (2 + digit_sum(1)))
# = 4 + (3 + (2 + 1))
# = 4 + (3 + 3)
# = 4 + 6
# = 10

def digit_sum(n: int) -> int:

    # Split the number into:
    # - last_digit: current digit
    # - remainder: remaining digits
    remainder = n // 10
    last_digit = n % 10

    # Base case: only one digit remains.
    if remainder == 0:
        return last_digit

    # Sum of the digits =
    # current digit + sum of the remaining digits.
    return last_digit + digit_sum(remainder)

# Key recursion concept:
# ----------------------
# Assume the recursive call already knows how to count the digits of the
# remaining number, then count the current digit.
#
# Recursion expansion (12345):
#
# count_digits(12345)
# = 1 + count_digits(1234)
# = 1 + (1 + count_digits(123))
# = 1 + (1 + (1 + count_digits(12)))
# = 1 + (1 + (1 + (1 + count_digits(1))))
# = 1 + (1 + (1 + (1 + 1)))
# = 5

def count_digits(n: int) -> int:

    # Remove the last digit.
    remainder = n // 10

    # Base case: only one digit remains.
    if remainder == 0:
        return 1

    # Number of digits =
    # current digit + number of remaining digits.
    return 1 + count_digits(remainder)

# Key recursion concept:
# ----------------------
# Assume the recursive call already knows how to convert the remaining
# (larger place values) into binary, then append the current binary digit.
#
# Recursion expansion (13):
#
# int_to_binary(13)
# = int_to_binary(6) + "1"
# = (int_to_binary(3) + "0") + "1"
# = ((int_to_binary(1) + "1") + "0") + "1"
# = (("1") + "1") + "0" + "1"
# = "1101"

def int_to_binary(n: int) -> str:

    # Split the number into:
    # - last_digit: current binary digit (0 or 1)
    # - remainder: remaining value to convert
    last_digit = n % 2
    remainder = n // 2

    # Base case: only one binary digit remains.
    if remainder == 0:
        return str(last_digit)

    # Binary representation =
    # binary representation of the remaining value
    # followed by the current binary digit.
    return int_to_binary(remainder) + str(last_digit)

if __name__ == "__main__":

    print("print_numbers(5):")
    print_numbers(5)

    print("\nsum_numbers(5):")
    print(sum_numbers(5))

    print("\nfactorial(5):")
    print(factorial(5))

    print('\nreverse_string("Hello"):')
    print(reverse_string("Hello"))

    print("\ndigit_sum(1234):")
    print(digit_sum(1234))

    print("\ncount_digits(12345):")
    print(count_digits(12345))

    print("\nint_to_binary(13):")
    print(int_to_binary(13))