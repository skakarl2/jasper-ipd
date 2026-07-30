"""Weighted union-find (disjoint set) with path compression."""

from typing import Hashable


class UnionFind:
    """Disjoint set forest supporting arbitrary hashable elements.

    Uses union by rank and path compression for nearly O(1) amortised
    operations (inverse-Ackermann in theory).
    """

    def __init__(self):
        self._parent: dict[Hashable, Hashable] = {}
        self._rank: dict[Hashable, int] = {}
        self._size: dict[Hashable, int] = {}
        self._components = 0

    def _ensure(self, x: Hashable) -> None:
        if x not in self._parent:
            self._parent[x] = x
            self._rank[x] = 0
            self._size[x] = 1
            self._components += 1

    def find(self, x: Hashable) -> Hashable:
        """Return the root representative of *x*'s component.

        Lazily registers *x* if it has not been seen before.
        Path compression flattens the tree on every traversal.
        """
        self._ensure(x)
        # human edit: two-pass find with explicit compression loop
        root = x
        while self._parent[root] != root:
            root = self._parent[root]
        node = x
        while node != root:
            parent = self._parent[node]
            self._parent[node] = root
            node = parent
        return root

    def union(self, x: Hashable, y: Hashable) -> bool:
        """Merge the components containing *x* and *y*.

        Returns ``True`` if a merge actually happened (they were in
        different components), ``False`` if they were already connected.
        """
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        if self._rank[rx] < self._rank[ry]:
            rx, ry = ry, rx
        self._parent[ry] = rx
        self._size[rx] += self._size[ry]
        if self._rank[rx] == self._rank[ry]:
            self._rank[rx] += 1
        self._components -= 1
        return True

    def connected(self, x: Hashable, y: Hashable) -> bool:
        """Check whether *x* and *y* belong to the same component."""
        return self.find(x) == self.find(y)

    def component_count(self) -> int:
        """Return the number of disjoint components."""
        return self._components

    def component_size(self, x: Hashable) -> int:
        """Return the size of the component containing *x*."""
        return self._size[self.find(x)]

    def groups(self) -> dict[Hashable, list[Hashable]]:
        """Return a dict mapping each root to the list of members in its component."""
        result: dict[Hashable, list[Hashable]] = {}
        for element in self._parent:
            root = self.find(element)
            result.setdefault(root, []).append(element)
        return result

    def reset(self) -> None:
        """Clear all components, restoring the structure to its initial empty state."""
        self._parent.clear()
        self._rank.clear()
        self._size.clear()
        self._components = 0

    def __len__(self) -> int:
        """Total number of tracked elements."""
        return len(self._parent)

    def __contains__(self, x: Hashable) -> bool:
        return x in self._parent

    def __repr__(self) -> str:
        return f"UnionFind(elements={len(self)}, components={self._components})"


if __name__ == "__main__":
    uf = UnionFind()

    edges = [("a", "b"), ("c", "d"), ("b", "c"), ("e", "f")]
    for u, v in edges:
        merged = uf.union(u, v)
        print(f"union({u!r}, {v!r}) -> merged={merged}  components={uf.component_count()}")

    print()
    print(f"connected('a', 'd') = {uf.connected('a', 'd')}")
    print(f"connected('a', 'e') = {uf.connected('a', 'e')}")
    print(f"component_size('a') = {uf.component_size('a')}")
    print(f"component_size('e') = {uf.component_size('e')}")
    print(f"total elements: {len(uf)}, components: {uf.component_count()}")

    print("\n--- numeric keys ---")
    uf2 = UnionFind()
    for i in range(8):
        uf2.union(i, i + 1)
    print(f"0..8 chained: size={uf2.component_size(0)}, components={uf2.component_count()}")
    uf2.union(100, 200)
    print(f"after union(100,200): components={uf2.component_count()}")
    print(repr(uf2))
