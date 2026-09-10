class TrieNode:
    __slots__ = ("children", "is_end")

    def __init__(self):
        self.children: dict[str, "TrieNode"] = {}
        self.is_end: bool = False


class Trie:
    """A prefix tree supporting insert, search, prefix lookup, and deletion."""

    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        """Insert a word into the trie.

        Traverses the trie character by character, creating new nodes as
        needed, and marks the final node as a word boundary.

        Args:
            word: The string to insert. Must be non-empty.

        Raises:
            ValueError: If word is empty.
        """
        if not word:
            raise ValueError("Cannot insert an empty string")
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end = True

    def search(self, word: str) -> bool:
        """Check whether an exact word exists in the trie.

        Traverses the trie character by character. Returns True only if
        every character is found and the final node is marked as a word
        boundary.

        Args:
            word: The string to search for.

        Returns:
            True if the exact word has been inserted, False otherwise.
        """
        node = self._find_node(word)
        return node is not None and node.is_end

    def starts_with(self, prefix: str) -> bool:
        """Check whether any inserted word begins with the given prefix.

        Unlike search, this does not require the prefix itself to be a
        complete inserted word — only that the path exists in the trie.

        Args:
            prefix: The prefix string to look up.

        Returns:
            True if at least one inserted word starts with prefix,
            False otherwise.
        """
        return self._find_node(prefix) is not None

    def delete(self, word: str) -> bool:
        """Remove a word from the trie.

        Walks the trie to verify the word exists, then prunes nodes
        bottom-up: any node that is not a word boundary and has no
        children is removed from its parent. Nodes shared by other
        words are left intact.

        Args:
            word: The string to delete.

        Returns:
            True if the word was found and deleted, False if it was
            not present.
        """
        path: list[tuple[TrieNode, str]] = []
        node = self.root
        for ch in word:
            if ch not in node.children:
                return False
            path.append((node, ch))
            node = node.children[ch]

        if not node.is_end:
            return False

        node.is_end = False

        for parent, ch in reversed(path):
            child = parent.children[ch]
            if not child.is_end and not child.children:
                del parent.children[ch]
            else:
                break

        return True

    def _find_node(self, prefix: str) -> TrieNode | None:
        """Return the node at the end of prefix, or None if the path doesn't exist."""
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node
