#include <iostream>
#include <string>
#include <vector>
#include <queue>
#include <unordered_set>
#include <cctype>
#include <cstring>

using namespace std;

// Performs a breadth-first search starting from 1, applying "multiply by 2"
// and "divide by 3" (integer division) to reach `target`.
// `path` and `memo` are the accumulated operations and visited values so far
// (both empty on the initial call).
// Returns the sequence of operations for the shortest path found, or an
// empty vector if the queue is exhausted without reaching `target`.
vector<string> mathexpr(int target, vector<string> path, unordered_set<int> memo) {
    // Frontier of states to explore: each entry is (current value, path taken to reach it).
    queue<pair<int, vector<string>>> q;
    int tmp;
    vector<string> multiplyPath, dividePath;
    vector<string> result;

    // Seed the search with the starting value 1 and an empty path.
    q.push({1, {}});
    memo.insert(1);

    while (!q.empty()) {
        // Pull the next state off the front of the queue (FIFO -> BFS order).
        auto [curr, currPath] = q.front();
        q.pop();

        // Found the target: record the path that got us here and stop.
        if (curr == target) {
            result = currPath;
            break;
        }

        // Try multiplying by 2.
        tmp = curr * 2;
        if (!memo.contains(tmp)) {
            memo.insert(tmp);
            multiplyPath = currPath;
            multiplyPath.push_back(" x 2");
            q.push({tmp, multiplyPath});
        }

        // Divide by 3 (integer division).
        tmp = curr / 3;
        if (!memo.contains(tmp)) {
            memo.insert(tmp);
            dividePath = currPath;
            dividePath.push_back(" / 3");
            q.push({tmp, dividePath});
        }
    }

    return result;
}

// Returns true if `arg` consists only of decimal digit characters.
bool isAllDigits(const char *arg) {
    int length = strlen(arg);
    for (int idx = 0; idx < length; idx++) {
        if (!isdigit(static_cast<unsigned char>(arg[idx]))) {
            return false;
        }
    }
    return true;
}

int main(int argc, char **argv) {
    // No argument provided.
    if (argc == 1) {
        cerr << "No input argument\n"
             << "Usage: ./mathexpr <non-negative integer>" << endl;
        return 1;
    }

    // More than one argument provided.
    if (argc > 2) {
        cerr << "Too many input arguments\n"
             << "Usage: ./mathexpr <non-negative integer>" << endl;
        return 1;
    }

    // Reject negative numbers and anything that isn't purely digits.
    if (argv[1][0] == '-' || !isAllDigits(argv[1])) {
        cerr << "Bad input\n"
             << "Error: Argument " << argv[1] << " is not a non-negative integer." << endl;
        return 1;
    }

    // Convert validated input string to an integer target.
    int target = atoi(argv[1]);

    // Run the search starting with an empty path and empty visited set.
    vector<string> path = mathexpr(target, {}, {});

    // Print the resulting expression: starting value 1 followed by each operation.
    cout << "1";
    int pathLength = path.size();
    for (int i = 0; i < pathLength; i++) {
        cout << path[i];
    }
    cout << endl;

    return 0;
}