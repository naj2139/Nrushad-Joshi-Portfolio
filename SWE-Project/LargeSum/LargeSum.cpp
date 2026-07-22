// Reads a file of large numbers (one per line, up to 50 digits each) and
// computes their sum using manual digit-by-digit addition with carrying,
// since the numbers are too large to fit in any built-in integer type.

#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <cstdlib>
using namespace std;

int main(int argc, char **argv) {

    ios::sync_with_stdio(false);
    cin.tie(NULL);

    if (argc < 2) {
        cerr << "Usage: " << argv[0] << " <input_file>\n";
        return 1;
    }

    // position:         loop counter used across multiple loops, walks the digit array
    // padOffset:        number of leading positions in digitSum that this line's
    //                    digits do NOT reach (i.e. where its most-significant digit lands)
    // charIndex:         current index into the current line's string, walked backwards
    // leadingZeroCount:  count of leading zero-digits in the final result (used to trim output)
    int position = 0, padOffset = 0, charIndex = 0, leadingZeroCount = 0;

    // holds the current line (one number) read from the input file
    string line;

    // Open the input file given as a command-line argument.
    fstream file(argv[1]);

    // digitSum holds one digit per position, big-endian style, sized for the largest
    // possible sum: up to 50-digit numbers, with a few extra slots (indices 0-52)
    // reserved for carry overflow when many numbers are summed together.
    vector<int> digitSum(53, 0);

    // Special case: file is empty.
    // tellg() == 0 -> read pointer is at the start.
    // peek() == eof -> no character follows, so there's nothing to read.
    // Together, these confirm a zero-byte file, so the sum is 0.
    if (file.tellg() == 0 && file.peek() == ifstream::traits_type::eof()) {
        cout << "Full sum: 0" << endl;
        cout << "First 10 digits: 0" << endl;
        exit(0);
    }

    // Read the file line by line; each line is one big number to add into digitSum.
    while (getline(file, line)) {
        charIndex = line.length() - 1;
        padOffset = 52 - charIndex;

        // Walk digitSum from the least-significant position (52) backwards to the most (0).
        for (position = 52; position >= 0; position--) {

            // Only add a digit once we've reached the part of digitSum this number's digits cover.
            if (position >= padOffset) {
                if (charIndex < 0) { exit(1); } // safety check: ran out of digits unexpectedly
                digitSum[position] += line[charIndex] - '0'; // add this digit (converted from char to int)
                charIndex -= 1; // move to the next digit to the left
            }

            // If this position overflowed past 9, carry 1 into the
            // next position to the left.
            if (digitSum[position] >= 10) {
                digitSum[position] -= 10;
                if (position > 0) { digitSum[position - 1] += 1; }
            }
        }
    }

    // Count how many leading zero digits are in the final sum,
    // so we can skip printing them.
    for (position = 0; position <= 52; position++) {
        if (digitSum[position] == 0) { leadingZeroCount++; }
        else { break; }
    }

    // Special case: every digit was zero (sum is exactly 0).
    if (leadingZeroCount == 53) {
        cout << "Full sum: 0" << endl;
        cout << "First 10 digits: 0" << endl;
        exit(0);
    }

    // Print the full sum, skipping the leading zero positions.
    cout << "Full sum: ";
    for (position = leadingZeroCount; position <= 52; position++) {
        cout << digitSum[position];
    }
    cout << endl;

    // Print the first 10 significant digits of the sum.
    cout << "First 10 digits: ";
    if (52 - leadingZeroCount < 10) {
        // The sum has fewer than 10 significant digits total.
        for (position = leadingZeroCount; position <= 52; position++) {
            cout << digitSum[position];
        }
    } else {
        // Print exactly the first 10 significant digits.
        for (position = leadingZeroCount; position <= leadingZeroCount + 9; position++) {
            cout << digitSum[position];
        }
    }
    cout << endl;
}
