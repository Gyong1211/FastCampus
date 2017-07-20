class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

    def __del__(self):
        print('data of {} is is deleted'.format(self.data))

class D_linked_list:
    dummy = Node('dummy')

    def __init__(self):
        self.head = self.dummy
        self.tail = self.dummy
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
        self.tail.next = new_node
        self.tail = new_node
        self.num_data += 1

    def traverse(self):
        if self.empty():
            return None
        if self.current is None:
            self.before = self.head
            self.current = self.head.next
            return self.current.data
        if self.current.next is None:
            self.before = None
            self.current = None
            return None
        self.before = self.current
        self.current = self.current.next
        return self.current.data

    def remove(self):
        ret_data = self.current.data
        if self.current is self.tail:
            self.tail = self.before
        self.before.next = self.current.next
        self.current = self.before
        self.num_data -= 1
        return ret_data
    
def show_list(dlist):
    data = dlist.traverse()
    if data:
        while data:
            print(data, end=' ')
            data = dlist.traverse()
        print('')
    else:
        print('There is no data')

if __name__ == "__main__":
    dlist = D_linked_list()
    show_list(dlist)
    dlist.append(1)
    dlist.append(2)
    dlist.append(4)
    dlist.append(2)
    dlist.append(3)
    show_list(dlist)
    dlist.traverse()
    while dlist.current:
        if dlist.current.data == 2:
            dlist.remove()
        dlist.traverse()
    show_list(dlist)
