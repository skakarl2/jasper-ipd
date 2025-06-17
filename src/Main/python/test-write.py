class ListNode:
    def __init__(self, value=0, next=None):
        self.value = value
        self.next = next

def has_cycle(head):
    """
    Detects if a linked list has a cycle.
    :param head: The head node of the linked list.
    :return: True if there is a cycle, False otherwise.
    """
    if not head or not head.next:
        return False

    slow = head  # Tortoise
    fast = head  # Hare

    while fast and fast.next:
        slow = slow.next          # Move slow pointer one step
        fast = fast.next.next     # Move fast pointer two steps

        if slow == fast:          # Cycle detected
            return True

    return False  # No cycle detected    # Create a linked list with a cycle
    node1 = ListNode(1)
    node2 = ListNode(2)
    node3 = ListNode(3)
    node4 = ListNode(4)
    
    node1.next = node2
    node2.next = node3
    node3.next = node4
    node4.next = node2  # Creates a cycle
    
    print(has_cycle(node1))  # Output: True
    
    # Create a linked list without a cycle
    node1.next = node2
    node2.next = node3
    node3.next = node4
    node4.next = None  # No cycle
    
    print(has_cycle(node1))  # Output: False