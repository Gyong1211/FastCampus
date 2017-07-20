class Queue(list):
    #enqueue = list.append
    def enqueue(self, data):
        self.append(data)

    def dequeue(self):
        return self.pop(0)

    def empty(self):
        if not self:
            return True
        else:
            return False

    def peek(self):
        return self[0]

if __name__ == "__main__":
    q = Queue()
    for i in range(1,6):
        q.enqueue(i)

    print(q)

    while not q.empty():
        data = q.dequeue()
        print(data)
