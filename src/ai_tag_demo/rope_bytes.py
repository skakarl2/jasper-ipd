"""Rope data structure — a balanced binary tree of string chunks.

Supports efficient insert, delete, concatenation, and rebalancing
using the Fibonacci-weight heuristic described by Boehm et al.
"""

from __future__ import annotations

import math


# Precomputed Fibonacci thresholds for rebalance depth buckets.
_FIB_CACHE: list[int] = [1, 2]


def _fib_at_least(n: int) -> int:
    """Return the index of the smallest Fibonacci number >= n."""
    # Human rewrite: grow the cache first, then binary-search the boundary.
    while _FIB_CACHE[-1] < n:
        _FIB_CACHE.append(_FIB_CACHE[-2] + _FIB_CACHE[-1])
    lo, hi = 0, len(_FIB_CACHE) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if _FIB_CACHE[mid] >= n:
            hi = mid
        else:
            lo = mid + 1
    return lo


class _Node:
    """Internal rope node. Leaves hold a string; branches hold children."""

    __slots__ = ("left", "right", "text", "weight")

    def __init__(
        self,
        text: str | None = None,
        left: _Node | None = None,
        right: _Node | None = None,
    ) -> None:
        if text is not None:
            self.text: str | None = text
            self.left: _Node | None = None
            self.right: _Node | None = None
            self.weight: int = len(text)
        else:
            self.text = None
            self.left = left
            self.right = right
            self.weight = _node_len(left) if left else 0

    @property
    def is_leaf(self) -> bool:
        return self.text is not None


def _node_len(node: _Node | None) -> int:
    # human edit: explicit guard clauses
    if node is None:
        return 0
    if node.is_leaf:
        assert node.text is not None
        return len(node.text)
    right_len = _node_len(node.right)
    return node.weight + right_len


def _node_index(node: _Node, i: int) -> str:
    """Return the character at position *i* in the subtree rooted at *node*."""
    if node.is_leaf:
        return node.text[i]  # type: ignore[index]
    if i < node.weight:
        return _node_index(node.left, i)  # type: ignore[arg-type]
    return _node_index(node.right, i - node.weight)  # type: ignore[arg-type]


def _node_split(node: _Node, i: int) -> tuple[_Node | None, _Node | None]:
    """Split *node* at position *i*, returning (left, right) subtrees."""
    if node.is_leaf:
        txt = node.text  # type: ignore[assignment]
        left = _Node(txt[:i]) if i > 0 else None
        right = _Node(txt[i:]) if i < len(txt) else None  # type: ignore[arg-type]
        return left, right

    if i == node.weight:
        return node.left, node.right
    if i < node.weight:
        ll, lr = _node_split(node.left, i)  # type: ignore[arg-type]
        return ll, _concat_nodes(lr, node.right)
    rl, rr = _node_split(node.right, i - node.weight)  # type: ignore[arg-type]
    return _concat_nodes(node.left, rl), rr


def _concat_nodes(left: _Node | None, right: _Node | None) -> _Node | None:
    if left is None:
        return right
    if right is None:
        return left
    return _Node(left=left, right=right)


def _collect_leaves(node: _Node | None, out: list[str]) -> None:
    if node is None:
        return
    if node.is_leaf:
        if node.text:
            out.append(node.text)
        return
    _collect_leaves(node.left, out)
    _collect_leaves(node.right, out)


def _depth(node: _Node | None) -> int:
    if node is None or node.is_leaf:
        return 0
    return 1 + max(_depth(node.left), _depth(node.right))


def _build_balanced(leaves: list[str], lo: int, hi: int) -> _Node | None:
    """Recursively build a balanced subtree from a slice of leaves."""
    if lo > hi:
        return None
    if lo == hi:
        return _Node(leaves[lo])
    mid = (lo + hi) // 2
    return _Node(left=_build_balanced(leaves, lo, mid), right=_build_balanced(leaves, mid + 1, hi))


def _is_balanced(node: _Node | None) -> bool:
    """Check the Fibonacci-weight balance invariant.

    A rope of length *n* is balanced if its depth is at most
    floor(log_phi(n * sqrt(5))) where phi is the golden ratio.
    This is equivalent to requiring that the length meets the
    Fibonacci threshold for the node's depth.
    """
    if node is None or node.is_leaf:
        return True
    length = _node_len(node)
    if length == 0:
        return True
    depth = _depth(node)
    max_depth = int(math.log(length * math.sqrt(5)) / math.log((1 + math.sqrt(5)) / 2))
    return depth <= max_depth


class Rope:
    """A rope — a balanced binary tree of string chunks.

    Provides O(log n) insert, delete, and character lookup, with
    amortised O(n) concatenation and rebalance.
    """

    def __init__(self, text: str = "") -> None:
        self._root: _Node | None = _Node(text) if text else None

    def __len__(self) -> int:
        return _node_len(self._root)

    def __repr__(self) -> str:
        return f"Rope({self.to_string()!r})"

    def to_string(self) -> str:
        """Materialise the entire rope as a single string."""
        parts: list[str] = []
        _collect_leaves(self._root, parts)
        return "".join(parts)

    def index(self, i: int) -> str:
        """Return the character at position *i*.

        Raises IndexError when *i* is out of range.
        """
        length = len(self)
        if i < 0:
            i += length
        if i < 0 or i >= length:
            raise IndexError(f"rope index {i} out of range [0, {length})")
        return _node_index(self._root, i)  # type: ignore[arg-type]

    def insert(self, position: int, text: str) -> Rope:
        """Return a new rope with *text* inserted at *position*.

        Clamps *position* to [0, len(self)].
        """
        if not text:
            return self
        position = max(0, min(position, len(self)))
        new_node = _Node(text)
        if self._root is None:
            rope = Rope.__new__(Rope)
            rope._root = new_node
            return rope

        left, right = _node_split(self._root, position)
        combined = _concat_nodes(_concat_nodes(left, new_node), right)
        rope = Rope.__new__(Rope)
        rope._root = combined
        return rope

    def delete(self, start: int, end: int) -> Rope:
        """Return a new rope with the half-open range [start, end) removed.

        Clamps both bounds to [0, len(self)].
        """
        length = len(self)
        start = max(0, min(start, length))
        end = max(start, min(end, length))
        if start == end:
            return self
        if self._root is None:
            return self

        left, rest = _node_split(self._root, start)
        _, right = _node_split(rest, end - start) if rest else (None, None)  # type: ignore[arg-type]
        combined = _concat_nodes(left, right)
        rope = Rope.__new__(Rope)
        rope._root = combined
        return rope

    def concat(self, other: Rope) -> Rope:
        """Return a new rope that is the concatenation of *self* and *other*."""
        combined = _concat_nodes(self._root, other._root)
        rope = Rope.__new__(Rope)
        rope._root = combined
        return rope

    def rebalance(self) -> Rope:
        """Return a rebalanced copy using the Fibonacci-weight heuristic.

        Collects all leaf strings, then rebuilds the tree so that its
        depth satisfies the Fibonacci balance invariant: a rope of
        length *n* has depth at most floor(log_phi(n * sqrt(5))).
        Short-circuits if the tree is already balanced.
        """
        if self._root is None or _is_balanced(self._root):
            return self

        leaves: list[str] = []
        _collect_leaves(self._root, leaves)
        if not leaves:
            return Rope()

        target_leaf_size = max(1, int(math.sqrt(sum(len(s) for s in leaves))))
        merged: list[str] = []
        buf: list[str] = []
        buf_len = 0
        for leaf in leaves:
            buf.append(leaf)
            buf_len += len(leaf)
            if buf_len >= target_leaf_size:
                merged.append("".join(buf))
                buf.clear()
                buf_len = 0
        if buf:
            merged.append("".join(buf))

        rope = Rope.__new__(Rope)
        rope._root = _build_balanced(merged, 0, len(merged) - 1)
        return rope

    def char_count(self) -> int:
        """Return the total number of characters stored in the rope.

        Walks every leaf node and sums their text lengths, giving an
        accurate count even when the tree contains empty interior nodes.
        """
        parts: list[str] = []
        _collect_leaves(self._root, parts)
        return sum(len(s) for s in parts)

    @property
    def depth(self) -> int:
        """Return the depth of the underlying tree."""
        return _depth(self._root)

    @property
    def is_balanced(self) -> bool:
        """Check whether the tree satisfies the Fibonacci balance invariant."""
        return _is_balanced(self._root)
