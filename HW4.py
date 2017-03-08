class Stack:
    def __init__(self): 
        self.stack = []

    def push(self, item):
        self.stack.append(item)

    def pop(self):
        last = self.stack[-1]
        self.stack.pop()
        return last

    def peek(self):
        return self.stack[-1]

    def isEmpty(self):
        return not self.stack


class MyQueue:
    def __init__(self):
        self.first_stack = Stack()
        self.second_stack = Stack()
        
    def enqueue(self, item):
        self.first_stack.push(item)

        
    def dequeue(self):
        if self.second_stack.isEmpty():
            while self.first_stack.stack:
                item = self.first_stack.pop()
                self.second_stack.push(item)
        last = self.second_stack.pop()
        return last

        
    def peek(self):
        if self.second_stack.isEmpty():
            while self.first_stack.stack:
                item = self.first_stack.pop()
                self.second_stack.push(item)
        last = self.second_stack.peek()
        return last
    
    def isEmpty(self):
        empty = self.first_stack.isEmpty() and self.second_stack.isEmpty()
        return empty

q = MyQueue()
q.enqueue(5)
q.enqueue(25)
q.enqueue(30)
print(q.peek())
print(q.dequeue())
print(q.dequeue())
print(q.dequeue())
print(q.isEmpty())
q.enqueue(70)
print(q.peek())
