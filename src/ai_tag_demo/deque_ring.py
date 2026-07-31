"""Hand-written double-ended queue over a Python list (human origin).

A minimal deque supporting O(1) amortized push/pop at both ends, written by
hand as a human-origin baseline for the Edit-tool attribution fix validation.
"""


class Deque:
    def __init__(self):
        self._items = []

    def __len__(self):
        return len(self._items)

    def push_back(self, x):
        self._items.append(x)

    def push_front(self, x):
        self._items.insert(0, x)

    def pop_back(self):
        if not self._items:
            raise IndexError("pop from empty deque")
        return self._items.pop()

    def pop_front(self):
        if not self._items:
            raise IndexError("pop from empty deque")
        return self._items.pop(0)

    def peek_front(self):
        return self._items[0] if self._items else None
