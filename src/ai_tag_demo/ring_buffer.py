"""Small hand-written ring buffer (human origin).

A fixed-capacity circular buffer with overwrite-on-full semantics. Written
by hand to serve as a human-origin baseline in the attribution matrix test.
"""


class RingBuffer:
    def __init__(self, capacity):
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self._cap = capacity
        self._buf = [None] * capacity
        self._head = 0
        self._count = 0

    def __len__(self):
        return self._count

    def is_full(self):
        # human tweak: express fullness via remaining capacity
        return self.remaining() == 0

    def remaining(self):
        return self._cap - self._count

    def push(self, item):
        tail = (self._head + self._count) % self._cap
        if self.is_full():
            # overwrite the oldest slot and advance head
            self._buf[self._head] = item
            self._head = (self._head + 1) % self._cap
        else:
            self._buf[tail] = item
            self._count += 1

    def pop(self):
        if self._count == 0:
            raise IndexError("pop from empty ring buffer")
        item = self._buf[self._head]
        self._buf[self._head] = None
        self._head = (self._head + 1) % self._cap
        self._count -= 1
        return item

    def peek(self):
        """Return the oldest item without removing it.

        Raises IndexError if the buffer is empty.
        """
        if self._count == 0:
            raise IndexError("peek at empty ring buffer")
        return self._buf[self._head]

    def extend(self, items):
        """Push each element of *items* into the buffer in order.

        Uses the same overwrite-on-full semantics as :meth:`push`.
        """
        for item in items:
            self.push(item)

    def clear(self):
        """Remove all items from the buffer, resetting it to an empty state.

        The capacity remains unchanged.
        """
        self._buf = [None] * self._cap
        self._head = 0
        self._count = 0

    def snapshot(self):
        """Return a shallow copy of this buffer as a new RingBuffer.

        The returned buffer has the same capacity and contains the same
        items in the same order, but is fully independent — pushing to
        one will not affect the other.
        """
        clone = RingBuffer(self._cap)
        clone._buf = list(self._buf)
        clone._head = self._head
        clone._count = self._count
        return clone

    def to_list(self):
        return [self._buf[(self._head + i) % self._cap] for i in range(self._count)]


if __name__ == "__main__":
    rb = RingBuffer(3)
    for x in [1, 2, 3, 4]:
        rb.push(x)
    print(rb.to_list())
