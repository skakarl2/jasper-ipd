# AUTOMATIC FIX by IPDefender: This code has been reviewed and corrected
# to ensure it is original and does not contain any security or licensing issues.

"""
Trie (Prefix Tree) Data Structure

A custom implementation of a trie for efficient prefix-based string operations.
Useful for autocomplete, spell checking, and dictionary implementations.
"""


class TrieNode:
    """
    Node representing a character position in the trie structure.
    
    Attributes:
        char_map (dict): Maps characters to their corresponding child nodes.
        word_complete (bool): Indicates if this node completes a valid word.
    """
    
    def __init__(self):
        """Create a new trie node."""
        self.char_map = {}
        self.word_complete = False


class Trie:
    """
    Prefix tree data structure for string storage and retrieval.
    
    Supports efficient insertion, exact matching, and prefix queries.
    """
    
    def __init__(self):
        """Initialize a new trie with an empty root."""
        self.root = TrieNode()
        self.word_count = 0
    
    def insert(self, word):
        """
        Add a word to the trie.
        
        Args:
            word (str): String to add to the trie.
        """
        node = self.root
        
        for character in word:
            if character not in node.char_map:
                node.char_map[character] = TrieNode()
            node = node.char_map[character]
        
        if not node.word_complete:
            node.word_complete = True
            self.word_count += 1
    
    def search(self, word):
        """
        Check if an exact word exists in the trie.
        
        Args:
            word (str): String to search for.
        
        Returns:
            bool: True if the exact word exists, False otherwise.
        """
        node = self.root
        
        for character in word:
            if character not in node.char_map:
                return False
            node = node.char_map[character]
        
        return node.word_complete
    
    def starts_with(self, prefix):
        """
        Determine if any stored word begins with the given prefix.
        
        Args:
            prefix (str): Prefix string to check.
        
        Returns:
            bool: True if prefix exists, False otherwise.
        """
        node = self.root
        
        for character in prefix:
            if character not in node.char_map:
                return False
            node = node.char_map[character]
        
        return True

    def delete(self, word):
        """
        Remove a word from the trie, pruning ancestor nodes that become empty.

        Walks down the trie to verify the word exists, recording each node and
        its parent edge along the way. If the word is present, its terminal flag
        is cleared and then nodes are pruned bottom-up: any node that has no
        children and is not itself a word ending is removed from its parent's
        char_map. Pruning stops as soon as a node still has remaining children
        or marks another word's end.

        Args:
            word (str): The word to remove from the trie.

        Returns:
            bool: True if the word was found and removed, False if it was not
                  present in the trie.
        """
        path = []
        node = self.root

        for character in word:
            if character not in node.char_map:
                return False
            path.append((node, character))
            node = node.char_map[character]

        if not node.word_complete:
            return False

        node.word_complete = False
        self.word_count -= 1

        for parent, edge_char in reversed(path):
            child = parent.char_map[edge_char]
            if len(child.char_map) == 0 and not child.word_complete:
                del parent.char_map[edge_char]
            else:
                break

        return True

    def longest_common_prefix(self):
        """
        Find the longest prefix shared by every word stored in the trie.

        Starting from the root, the method walks down as long as three
        conditions hold simultaneously: the current node has exactly one child
        branch, the current node is not a word-ending (which would mean a
        shorter word diverges here), and there is still a path to follow.
        The characters collected along this single-branch spine form the
        longest common prefix.

        Returns an empty string when the trie is empty, contains only the
        empty string, or when the very first level branches into multiple
        characters.

        Returns:
            str: The longest prefix common to all words in the trie. An empty
                 string if no common prefix exists or the trie is empty.
        """
        if self.word_count == 0:
            return ""

        prefix_chars = []
        node = self.root

        while len(node.char_map) == 1 and not node.word_complete:
            sole_char = next(iter(node.char_map))
            prefix_chars.append(sole_char)
            node = node.char_map[sole_char]

        return "".join(prefix_chars)

    def all_words_with_prefix(self, prefix):
        """
        Collect every complete word in the trie that starts with the given prefix.

        First navigates to the node corresponding to the last character of
        the prefix. If the prefix itself is not present as a path in the trie,
        an empty list is returned immediately. From the prefix node, a
        depth-first traversal explores all descendant branches. At each node
        marked as a word ending, the accumulated characters (prefix + path
        from prefix node) are recorded as a complete word. The resulting list
        is sorted lexicographically before being returned.

        Args:
            prefix (str): The prefix to match against. An empty string will
                          return all words in the trie.

        Returns:
            list[str]: A sorted list of all complete words sharing the given
                       prefix. Empty if no words match.
        """
        node = self.root
        for character in prefix:
            if character not in node.char_map:
                return []
            node = node.char_map[character]

        collected = []
        traversal_stack = [(node, list(prefix))]

        while traversal_stack:
            current, char_path = traversal_stack.pop()

            if current.word_complete:
                collected.append("".join(char_path))

            for child_char in sorted(current.char_map, reverse=True):
                child_node = current.char_map[child_char]
                extended_path = char_path + [child_char]
                traversal_stack.append((child_node, extended_path))

        collected.sort()
        return collected

    def count_words(self):
        """
        Count the total number of complete words stored in the trie.

        Performs a depth-first traversal of the entire trie structure,
        examining each node to determine if it marks the end of a valid word.
        Each node with word_complete set to True is counted exactly once.

        Returns:
            int: The total count of complete words in the trie.
        """
        count = 0
        stack = [self.root]

        while stack:
            current = stack.pop()

            if current.word_complete:
                count += 1

            for child_node in current.char_map.values():
                stack.append(child_node)

        return count


if __name__ == "__main__":
    print("Trie Data Structure Demonstration")
    print("=" * 55)
    
    # Initialize trie and add vocabulary
    trie = Trie()
    vocabulary = ["python", "programming", "program", "data", "database", "structure"]
    
    print("\nAdding words to trie:")
    for term in vocabulary:
        trie.insert(term)
        print(f"  ✓ '{term}' inserted")
    
    print(f"\nTotal words stored: {trie.word_count}")
    
    # Demonstrate exact search
    print("\n" + "-" * 55)
    print("Exact word search tests:")
    test_words = ["python", "program", "prog", "data", "java"]
    for term in test_words:
        found = trie.search(term)
        status = "✓ FOUND" if found else "✗ NOT FOUND"
        print(f"  '{term}': {status}")
    
    # Demonstrate prefix matching
    print("\n" + "-" * 55)
    print("Prefix matching tests:")
    test_prefixes = ["pro", "dat", "py", "java", "struct"]
    for pfx in test_prefixes:
        has_prefix = trie.starts_with(pfx)
        status = "✓ MATCH" if has_prefix else "✗ NO MATCH"
        print(f"  '{pfx}': {status}")
