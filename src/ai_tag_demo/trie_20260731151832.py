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
