/*
 * Project Euler #43 — Substring Divisibility
 *
 * Given a string of unique digits, this program generates every permutation
 * of those digits (using Heap's algorithm) and checks each permutation
 * against the substring-divisibility rule:
 *
 *   d2 d3 d4  must be divisible by 2
 *   d3 d4 d5  must be divisible by 3
 *   d4 d5 d6  must be divisible by 5
 *   d5 d6 d7  must be divisible by 7
 *   d6 d7 d8  must be divisible by 11
 *   d7 d8 d9  must be divisible by 13
 *   d8 d9 d10 must be divisible by 17
 *
 * Every permutation that satisfies all conditions is printed, and the
 * sum of all valid permutations is printed at the end.
 *
 * Note: this version checks each fully-formed permutation only after
 * it is generated (generate-then-test), rather than pruning invalid
 * partial permutations early.
 */

#include <iostream>
#include <string>
#include <vector>

using namespace std;

int main(int argc, char **argv) {

    ios::sync_with_stdio(false);
    cin.tie(NULL);

    if (argc < 2) {
        cerr << "Usage: " << argv[0] << " <digit_string>\n";
        return 1;
    }

    string inputDigits = argv[1];
    int digitCount = inputDigits.length();

    // The divisors checked against each 3-digit substring, in order.
    const int DIVISORS[7] = {2, 3, 5, 7, 11, 13, 17};

    // `permutation` holds the digits in their current arrangement.
    // `swapCounter` tracks Heap's algorithm's internal state: how many
    // swaps have been performed so far at each recursion "level" (index).
    vector<int> permutation(digitCount, 0);
    vector<int> swapCounter(digitCount, 0);

    unsigned long long currentValue = 0;
    unsigned long long sumOfValidPermutations = 0;

    // Heap's algorithm walks through permutations one swap at a time;
    // `level` tracks how far along that swap sequence we are.
    int level = 1;

    // Whether the permutation changed since the last check (so we know
    // whether it's worth re-checking divisibility conditions).
    bool permutationChanged = true;

    // Load the input digits into the working array.
    for (int i = 0; i < digitCount; i++) {
        permutation[i] = inputDigits[i] - '0';
    }

    // Main loop: iterate through all permutations produced by
    // Heap's algorithm, checking each one against the divisibility rule.
    while (level < digitCount) {

        if (permutationChanged) {
            // Check each 3-digit substring against its corresponding prime,
            // starting from index 3 (the substring d1 d2 d3 has no rule).
            int divisorIndex = 0;
            int substringIndex;

            for (substringIndex = 3; substringIndex < digitCount; substringIndex++) {
                int threeDigitSubstring =
                    permutation[substringIndex - 2] * 100 +
                    permutation[substringIndex - 1] * 10 +
                    permutation[substringIndex];

                if (threeDigitSubstring % DIVISORS[divisorIndex] != 0) {
                    // This substring fails; no need to check the rest.
                    break;
                }
                divisorIndex += 1;
            }

            // If we made it all the way through, every substring was valid.
            if (substringIndex == digitCount) {
                currentValue = 0;
                for (int digit : permutation) {
                    currentValue = currentValue * 10 + digit;
                    cout << digit;
                }
                sumOfValidPermutations += currentValue;
                cout << "\n";
            }
        }

        // Heap's algorithm: decide whether to swap at this level or
        // move on to the next level.
        if (swapCounter[level] < level) {
            if (level % 2 == 0) {
                // Even level: swap the first element with the current one.
                swap(permutation[0], permutation[level]);
            } else {
                // Odd level: swap using the swap counter as the index.
                swap(permutation[swapCounter[level]], permutation[level]);
            }

            swapCounter[level] += 1;

            // Reset back to level 1 to build the next permutation.
            level = 1;
            permutationChanged = true;
        } else {
            // Done swapping at this level; reset it and move up.
            swapCounter[level] = 0;
            level += 1;
            permutationChanged = false;
        }
    }

    cout << "Sum: " << sumOfValidPermutations << "\n";
    return 0;
}