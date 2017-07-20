class Stack(list):
    #pop은 list의 pop을 그대로 사용하기 때문에 적어주지 않는다.

    #push = list.append
    def push(self, data):
        super().append(data)

    def empty(self):
        if not self:
            return True
        else:
            return False
    
    def peek(self):
        return self[-1]


if __name__ == "__main__":
    s = Stack()
    for i in range(1,6):
        s.push(i)

    print(s)

    while not s.empty():
        data = s.pop()
        print(data)

