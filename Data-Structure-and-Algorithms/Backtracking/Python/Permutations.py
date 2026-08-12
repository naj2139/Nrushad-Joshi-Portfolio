from __future__ import annotations


def permutations(letters: list[str]) -> list[list[str]]:
    """
    Given an array of unique strings, return all possible permutations.

    Args:
        letters: list of unique strings

    Returns:
        list of all permutations (each permutation is a list of strings)
    """
    result: list[list[str]] = []
    path: list[str] = []

    def backtrack() -> None:
        # Base case: path is a full permutation once its length matches
        # the number of letters available.
        if len(path) == len(letters):
            # IMPORTANT: append a COPY (path[:]), not path itself.
            # `path` is a single mutable list that gets reused across the
            # entire recursion. If we stored a reference to it (result.append(path)),
            # every entry in `result` would point to that same object.
            # As soon as later branches mutate `path` again (append/pop),
            # every "saved" permutation in `result` would silently change too,
            # and by the time recursion finishes, they'd all show path's
            # final state instead of the value at the moment it was recorded.
            # path[:] takes a snapshot, so it's unaffected by future mutation.
            result.append(path[:])
            return

        for letter in letters:
            if letter in path:  # skip letters already used in this permutation
                continue

            path.append(letter)  # make choice
            backtrack()           # explore deeper with this choice made
            path.pop()             # undo choice (backtrack) before trying the next letter

    backtrack()
    return result


def main() -> None:
    letters = ["a", "b", "c"]
    result = permutations(letters)
    print(f"permutations({letters}) = {result}")
    print(f"count = {len(result)} (expected {6})")  # n!


if __name__ == "__main__":
    main()