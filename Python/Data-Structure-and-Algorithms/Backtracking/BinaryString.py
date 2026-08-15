from __future__ import annotations


def binary_strings(n: int) -> list[str]:
    """
    Generate all binary strings of length n.

    Args:
        n: length of each string

    Returns:
        list of all binary strings of length n (2^n total)
    """
    result: list[list[int]] = []
    path: list[int] = []

    def backtrack() -> None:
        # Base case: path is a full binary string once its length
        # reaches n (one digit chosen per position).
        if len(path) == n:
            # IMPORTANT: append a COPY (path[:]), not path itself.
            # `path` is a single mutable list reused across the entire
            # recursion. If we stored a reference to it (result.append(path)),
            # every entry in `result` would point to that same object.
            # As soon as later branches mutate `path` again (append/pop),
            # every "saved" string in `result` would silently change too,
            # and by the time recursion finishes, they'd all show path's
            # final state instead of the value at the moment it was recorded.
            # path[:] takes a snapshot, so it's unaffected by future mutation.
            result.append(path[:])
            return

        # NOTE: no outer "for _ in range(n)" loop here.
        # This single loop represents ONE decision point: "what value goes
        # at the current position?" Recursion is what advances us through
        # the n positions, one call per level of the call stack — depth 0
        # fills position 0, depth 1 fills position 1, and so on down to
        # depth n. Looping n times at a single level would re-fill the
        # SAME position n times before recursion ever reaches the next
        # one, producing (2n)^n calls full of duplicates/garbage instead
        # of the correct 2^n unique leaves.
        for val in (0, 1):
            path.append(val)  # make choice
            backtrack()         # explore deeper with this choice made
            path.pop()           # undo choice (backtrack) before trying the next value

    backtrack()
    return ["".join(str(v) for v in bits) for bits in result]


def main() -> None:
    n = 4
    result = binary_strings(n)
    print(f"binary_strings({n}) = {result}")
    print(f"count = {len(result)} (expected {pow(2, n)})")


if __name__ == "__main__":
    main()