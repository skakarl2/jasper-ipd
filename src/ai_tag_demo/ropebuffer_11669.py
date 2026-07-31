"""
Rope data structure for efficient text buffer editing.

A rope is a binary tree structure where leaves contain strings and
internal nodes store the total weight (length) of the left subtree.
This allows for efficient concatenation, splitting, insertion, and deletion
operations compared to standard string manipulation.
"""


class RopeNode:
    """
    A node in the rope tree structure.
    
    Attributes:
        left: Left child node (or None for leaf nodes)
        right: Right child node (or None for leaf nodes)
        weight: For internal nodes, the total character count in left subtree.
                For leaf nodes, the length of the stored string.
        data: The actual string data (only for leaf nodes)
    """
    
    def __init__(self, data=None, left=None, right=None):
        """
        Initialize a rope node.
        
        Args:
            data: String data for leaf nodes
            left: Left child RopeNode
            right: Right child RopeNode
        """
        self.left = left
        self.right = right
        self.data = data
        
        if data is not None:
            # Leaf node
            self.weight = len(data)
        elif left is not None:
            # Internal node - weight is the total char count of left subtree
            self.weight = left.char_count()
        else:
            self.weight = 0
    
    def is_leaf(self):
        """Check if this node is a leaf."""
        return self.data is not None
    
    def char_count(self):
        """Return the total number of characters in this subtree."""
        if self.is_leaf():
            return self.weight
        total = self.weight
        if self.right is not None:
            total += self.right.char_count()
        return total


class Rope:
    """
    Rope data structure for efficient text manipulation.
    
    Supports indexing, concatenation, splitting, insertion, and deletion
    with better performance characteristics than plain strings for large texts.
    """
    
    def __init__(self, text=""):
        """
        Initialize a rope from a string.
        
        Args:
            text: Initial text content
        """
        if text:
            self.root = self._build_rope(text)
        else:
            self.root = RopeNode(data="")
    
    def _build_rope(self, text, start=0, end=None):
        """
        Build a balanced rope from a string using divide-and-conquer.
        
        Args:
            text: Source text
            start: Start index
            end: End index (exclusive)
            
        Returns:
            RopeNode representing the constructed rope
        """
        if end is None:
            end = len(text)
        
        length = end - start
        
        # Base case: create leaf for small strings
        if length <= 8:
            return RopeNode(data=text[start:end])
        
        # Recursive case: split in middle and create internal node
        mid = start + length // 2
        left_node = self._build_rope(text, start, mid)
        right_node = self._build_rope(text, mid, end)
        
        return RopeNode(left=left_node, right=right_node)
    
    def index(self, i):
        """
        Get the character at index i.
        
        Args:
            i: Character index
            
        Returns:
            Character at position i
            
        Raises:
            IndexError: If index is out of bounds
        """
        if i < 0 or i >= len(self):
            raise IndexError("Rope index out of range")
        
        return self._index_helper(self.root, i)
    
    def _index_helper(self, node, i):
        """Helper method for index lookup."""
        if node.is_leaf():
            return node.data[i]
        
        if i < node.weight:
            return self._index_helper(node.left, i)
        else:
            return self._index_helper(node.right, i - node.weight)
    
    def concat(self, other):
        """
        Concatenate this rope with another.
        
        Args:
            other: Another Rope instance
            
        Returns:
            New Rope containing the concatenation
        """
        new_rope = Rope()
        new_rope.root = RopeNode(left=self.root, right=other.root)
        return new_rope
    
    def split(self, i):
        """
        Split the rope at index i.
        
        Args:
            i: Split position
            
        Returns:
            Tuple of (left_rope, right_rope) where left contains [0:i]
            and right contains [i:]
        """
        if i <= 0:
            return Rope(), self._clone()
        if i >= len(self):
            return self._clone(), Rope()
        
        left_node, right_node = self._split_helper(self.root, i)
        
        left_rope = Rope()
        left_rope.root = left_node if left_node else RopeNode(data="")
        
        right_rope = Rope()
        right_rope.root = right_node if right_node else RopeNode(data="")
        
        return left_rope, right_rope
    
    def _split_helper(self, node, i):
        """Helper method for splitting."""
        if node.is_leaf():
            left_data = node.data[:i]
            right_data = node.data[i:]
            left_node = RopeNode(data=left_data) if left_data else None
            right_node = RopeNode(data=right_data) if right_data else None
            return left_node, right_node
        
        if i < node.weight:
            # Split is in left subtree
            left_left, left_right = self._split_helper(node.left, i)
            
            if left_right and node.right:
                right_combined = RopeNode(left=left_right, right=node.right)
            elif left_right:
                right_combined = left_right
            else:
                right_combined = node.right
            
            return left_left, right_combined
        elif i > node.weight:
            # Split is in right subtree
            right_left, right_right = self._split_helper(node.right, i - node.weight)
            
            if node.left and right_left:
                left_combined = RopeNode(left=node.left, right=right_left)
            elif node.left:
                left_combined = node.left
            else:
                left_combined = right_left
            
            return left_combined, right_right
        else:
            # Split exactly at the boundary
            return node.left, node.right
    
    def insert(self, i, s):
        """
        Insert string s at index i.
        
        Args:
            i: Insertion index
            s: String to insert
            
        Returns:
            New Rope with insertion applied
        """
        left, right = self.split(i)
        middle = Rope(s)
        return left.concat(middle).concat(right)
    
    def delete(self, i, j):
        """
        Delete characters from index i to j (exclusive).
        
        Args:
            i: Start index (inclusive)
            j: End index (exclusive)
            
        Returns:
            New Rope with deletion applied
        """
        if i >= j or i >= len(self):
            return self._clone()
        
        left, _ = self.split(i)
        _, right = self.split(j)
        return left.concat(right)
    
    def to_string(self):
        """
        Convert the rope to a regular Python string.
        
        Returns:
            String representation of the rope contents
        """
        return self._to_string_helper(self.root)
    
    def _to_string_helper(self, node):
        """Helper method for string conversion."""
        if node is None:
            return ""
        if node.is_leaf():
            return node.data
        
        left_str = self._to_string_helper(node.left)
        right_str = self._to_string_helper(node.right)
        return left_str + right_str
    
    def _clone(self):
        """Create a shallow copy of this rope."""
        new_rope = Rope()
        new_rope.root = self.root
        return new_rope
    
    @property
    def char_count(self):
        """Get the total number of characters in the rope."""
        return self.root.char_count() if self.root else 0
    
    def __len__(self):
        """Return the length of the rope."""
        return self.char_count
    
    def reverse(self):
        """Return a new Rope with the entire text reversed."""
        return Rope(self.to_string()[::-1])

    def find(self, substring):
        """Return the index of the first occurrence of substring, or -1 if not found."""
        return self.to_string().find(substring)

    def __str__(self):
        """String representation."""
        return self.to_string()


if __name__ == "__main__":
    # Demo: Build a rope from a sentence
    print("=== Rope Data Structure Demo ===\n")
    
    initial_text = "The quick brown fox jumps over the lazy dog"
    rope = Rope(initial_text)
    
    print(f"Initial rope: '{rope}'")
    print(f"Length: {len(rope)}")
    print(f"Character at index 10: '{rope.index(10)}'")
    print()
    
    # Insert operation
    rope = rope.insert(19, "really ")
    print(f"After inserting 'really ' at index 19: '{rope}'")
    print(f"New length: {len(rope)}")
    print()
    
    # Delete operation
    rope = rope.delete(4, 10)
    print(f"After deleting characters 4-10: '{rope}'")
    print(f"New length: {len(rope)}")
    print()
    
    # Concatenation
    rope2 = Rope(" and climbs trees!")
    rope = rope.concat(rope2)
    print(f"After concatenation: '{rope}'")
    print(f"Final length: {len(rope)}")
    print()
    
    # Split operation
    left, right = rope.split(25)
    print(f"Split at index 25:")
    print(f"  Left part: '{left}'")
    print(f"  Right part: '{right}'")
    print()

    # Reverse operation
    reversed_rope = rope.reverse()
    print(f"Reversed rope: '{reversed_rope}'")

    # Find operation
    find_idx = rope.find("fox")
    print(f"Index of 'fox' in rope: {find_idx}")

    print("\n=== Demo Complete ===")
