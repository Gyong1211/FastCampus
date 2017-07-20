class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

    def __del__(self):
        print('data of {} is is deleted'.format(self.data))

class Linked_list:
    def __init__(self):
        self.head = None
        self.tail = None
        self.before = None
        self.current = None
        self.num_data = 0

    def empty(self):
        if self.num_data == 0:
            return True
        else:
            return False

    def size(self):
        return self.num_data

    def append(self, data):
        new_node = Node(data)
        if self.empty():
            self.head = new_node
        else:
            self.tail.next = new_node
        self.tail = new_node
        self.num_data += 1

    def traverse(self, mode='next'):
        if self.empty():
            return None
        if mode == 'first':
            self.before = self.head
            self.current = self.head
        else:
            if self.current.next is None:
                return None
            self.before = self.current
            self.current = self.current.next
        return self.current.data

    def remove(self):
        ret_data = self.current.data

        if self.size() == 1:
            self.head = None
            self.before = None
            self.current = None
            self.tail = None
        elif self.current is self.head:
            self.head = self.current.next
            self.before = self.current.next
            self.current = self.current.next
        else:
            if self.current is self.tail:
                self.tail = self.before
            self.before.next = self.current.next
            self.current = self.before
        self.num_data -= 1
        return ret_data
    
def show_list(_list):
    data = _list.traverse(mode='first')
    if data:
        print(data, end=' ')
        data = slist.traverse()
        while data:
            print(data, end=' ')
            data = _list.traverse()
    else:
        print('There is no data')

if __name__ == "__main__":
    slist = Linked_list()
    print(slist.empty())
    slist.append(1)
    slist.append(2)
    print(slist.empty())
    print(slist.head.data)
    print(slist.tail.data)
    slist.append(2)
    print(slist.tail.data)
    print(slist.current)
    show_list(slist)
