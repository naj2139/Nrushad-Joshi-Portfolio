from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def insertionSortList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if not head:
            return head

        prev = head
        move = head.next

        while move:

            if prev.val > move.val:
                node = move

                # after = the real next unprocessed node in the list,
                # saved BEFORE node gets moved elsewhere. prev.next = after
                # detaches node; prev is now correctly "the node right
                # before after" (no need to move prev at all).
                after = move.next
                prev.next = after

                # Walk the sorted prefix looking for the first node whose
                # value is NOT smaller than node.val -- that's where node
                # belongs, sitting right before it. i is the "scanner"
                # moving forward; j always trails one step behind i, so
                # j is the node that will end up right before node once
                # we splice it in.
                i = head
                j = None
                while i.val < node.val:
                    j = i
                    i = i.next

                if j is not None:
                    # Found a proper insertion point in the middle (or
                    # end) of the prefix: j -> node -> i
                    #   j.next = node   links j forward to node
                    #   node.next = i   links node forward to i
                    # (i can be None here too, if node is the new largest
                    # value -- inserting at the tail works the same way)
                    j.next = node
                    node.next = i
                else:
                    # j stayed None, meaning the while loop above never
                    # ran even once -- i.val was NOT < node.val on the
                    # very first check. That means node.val is smaller
                    # than (or equal to) the current head, so node
                    # becomes the new head of the list.
                    node.next = head
                    head = node

                # --- First attempt (works, but does redundant work) ---
                # move = node.next
                #
                # move IS node (the thing we just relocated), so
                # node.next isn't "the next unprocessed node" -- it's
                # "whatever node we just linked node to" (either the old
                # head, or i from the search above). The list stays a
                # valid chain, so this doesn't produce a wrong answer,
                # but it means every shift forces a re-walk back through
                # part of the already-sorted prefix before reaching the
                # real unprocessed tail again. Those re-comparisons never
                # trigger a false swap (the prefix is sorted, so
                # prev.val > move.val is never true there) -- but they're
                # pure overhead: extra iterations of the while loop that
                # do zero useful work.

                # move = after skips straight to the real next unprocessed
                # node instead, since after was captured before node was
                # touched. That means every iteration of the outer while
                # loop does productive work -- no wasted re-scanning of
                # the sorted prefix -- which is what keeps this at the
                # true O(n^2) bound for insertion sort, instead of doing
                # extra passes on top of it.
                move = after
                continue

            prev = move
            move = move.next

        return head


if __name__ == "__main__":
    # Input: 4 -> 2 -> 1 -> 3
    head = ListNode(4, ListNode(2, ListNode(1, ListNode(3))))

    sol = Solution()
    result = sol.insertionSortList(head)

    while result:
        print(result.val, end=" -> " if result.next else "\n")
        result = result.next