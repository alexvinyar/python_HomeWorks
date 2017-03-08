class Node:
    def __init__(self, data = None, next=None):
        self.data = data
        self.next = next

class LinkedList:
    def __init__(self, head=None):
        self.head = head

    def empty(self):
        if self.head:
            return False
        return True

    def printList(self):
        node = self.head
        while node:
            print(node.data, end=" -> ")
            node = node.next
        print()

    def push(self, data):
        node = Node(data, next=self.head)
        self.head = node

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
        else:
            node = self.head
            while node.next:
                node = node.next
            node.next = new_node

    def find_index(self, value):
        node = self.head
        index = 0
        while node:
            if node.data == value:
                return index
            index += 1
            if node.next:
                node = node.next
            else:
                break
        return None

    def insert(self, index, value):
        new_node = Node(value)
        cur_node = self.head
        if index < 1:
            self.push(value)
        else:
            for i in range (0, index-1): 
                cur_node = cur_node.next
            new_child = cur_node.next
            cur_node.next = new_node
            new_node.next = new_child

    def size(self):
        node = self.head
        cur_size = 1
        while node.next:
            node = node.next
            cur_size += 1
        return cur_size

    def value_n_from_end(self, n):
        index = self.size() - n
        cur_node = self.head
        for i in range (0, index):
            cur_node = cur_node.next
        return cur_node


n3 = Node(9)
n2 = Node(8, next=n3)
n1 = Node(7, next=n2)


l = LinkedList(head=n1)
for i in [1,2,3,4]:
    l.push(i)

l.printList()
print(l.value_n_from_end(3).data)
