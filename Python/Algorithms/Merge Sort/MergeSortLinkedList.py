from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def length(self, head: Optional[ListNode]) -> int:
        # The general pattern for walking a linked list: start a pointer
        # at head, and step forward with `head = head.next` until you
        # fall off the end (head becomes None). Every linked-list
        # traversal in this file is a variation of this same loop shape --
        # only what happens *inside* the loop changes.
        length = 0
        while head:
            length += 1
            head = head.next
        return length

    def split(self, idx: int, head: ListNode):
        # left stays fixed at the very start -- this is the reference
        # we return for the first half, so it must never move.
        left = head

        # head is the pointer that actually walks forward. Stepping
        # idx - 1 times lands head on the LAST node that should belong
        # to the left half (0-indexed: idx-1 nodes ahead of the start).
        # One step further (head.next) would be the first node of the
        # right half -- which is exactly what "right" grabs below,
        # before the link gets cut.
        for _ in range(0, idx - 1):
            head = head.next

        right = head.next   # save the second half BEFORE cutting it off
        head.next = None    # cut: left half now ends cleanly here
        return left, right

    def sort(self, left: Optional[ListNode], right: Optional[ListNode]) -> Optional[ListNode]:
        # Dummy-head + moving-tail pattern for building a new list:
        #   out never moves -- it's the fixed anchor back to the start,
        #     so we can return out.next at the end (skipping the dummy).
        #   tmp moves forward one attachment at a time -- it always
        #     points at "the last node I've attached so far," which is
        #     where the NEXT node needs to be linked on.
        out = ListNode()
        tmp = out

        # left and right are already sorted (from recursion below), so
        # only their current front nodes ever need comparing -- same
        # two-pointer idea as the array merge, just moving node
        # references (left = left.next) instead of an index (l += 1).
        while left and right:
            if left.val < right.val:
                tmp.next = left    # attach the real node, no copying
                left = left.next    # advance ONLY the list we took from
            else:
                tmp.next = right
                right = right.next
            tmp = tmp.next          # advance the tail to the node just attached

        # Whichever list still has nodes left is already sorted --
        # just attach the rest of it directly, no need to walk it
        # node-by-node.
        if left:
            tmp.next = left
        if right:
            tmp.next = right

        return out.next

    def sortList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        # length(head) is an O(n) traversal by itself. Calling it three
        # separate times (once per check below) would walk the same
        # list three times before any actual splitting happens -- and
        # since sortList recurses on every half, that 3x cost compounds
        # at every level of recursion. Computing it once up front avoids
        # that redundant work.
        n = self.length(head)

        # Base case: a list of length 0 or 1 is already sorted --
        # nothing to split or merge.
        if n <= 1:
            return head

        half = n // 2
        left, right = self.split(half, head)

        left = self.sortList(left)
        right = self.sortList(right)

        return self.sort(left, right)


if __name__ == "__main__":
    # Input: 4 -> 2 -> 1 -> 3
    head = ListNode(4, ListNode(2, ListNode(1, ListNode(3))))

    sol = Solution()
    result = sol.sortList(head)

    while result:
        print(result.val, end=" -> " if result.next else "\n")
        result = result.next