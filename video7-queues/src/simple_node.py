class Node():
    def __init__(self, value):
        self.value = value
        self.next = None

    def append(self, node):
        if self.next is not None:
            raise(ValueError("next node is not none"))
        self.next = node

    def __eq__(self, other):
        return self.value == other.value

    def __str__(self):
        return "value=" + str(self.value)

def test_node():
    n1 = Node(1)
    assert(n1.value == 1)
    assert(n1.next == None)
    
    n2 = Node(2)
    n1.append(n2)
    assert(n1.next is not None)
    
    n3 = Node(3)
    assert(n2.next is None)
    n2.append(n3)
    assert(n2.next is not None)

    node = n1
    count = 1
    while node.next is not None:
        node = node.next
        count += 1

    assert(node == n3)
    assert(count == 3)
