class TreeNode:
    def __init__(self):
        self.data = None
        self.left = None
        self.right = None

    def __del__(self):
        print('TreeNode of {} is deleted'.format(self.data))

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data

class BinaryTree:
    def __init__(self):
        self.root = None

    def get_root(self):
        return self.root

    def set_root(self, root):
        self.root = root

    def make_node(self):
        new_node = TreeNode()
        return new_node
    
    def get_node_data(self, cur):
        return cur.data

    def set_node_data(self, cur, data):
        cur.data = data

    def get_left_sub_tree(self, cur):
        return cur.left

    def get_right_sub_tree(self, cur):
        return cur.right

    def make_left_sub_tree(self, cur, left):
        cur.left = left

    def make_right_sub_tree(self, cur, right):
        cur.right = right

    def preorder_traverse(self, cur, func):
        if cur == None:
            return
        func(cur.data)
        self.preorder_traverse(cur.left, func)
        self.preorder_traverse(cur.right, func)

    def inorder_traverse(self, cur, func):
        if not cur:
            return
        self.inorder_traverse(cur.left, func)
        func(cur.data)
        self.inorder_traverse(cur.right, func)

    def postorder_traverse(self, cur, func):
        if not cur:
            return
        self.postorder_traverse(cur.left, func)
        self.postorder_traverse(cur.right, func)
        func(cur.data)


"""
  전위 연산      중위 연산          후위 연산
      1              4                  7
    /   \          /   \              /   \
   2     5        2     7            3     6
  / \   / \      / \   / \          / \   / \
 3   4 6   7    1   3 5   6        1   2 4   5
"""

class BinarySearchTree(BinaryTree):
    def insert(self, data):
        new_node = self.make_node()
        self.set_node_data(new_node, data)
        cur = self.get_root()
        if not cur:
            self.set_root(new_node)
            return
        while True:
            if data < self.get_node_data(cur):
                if self.get_left_sub_tree(cur):
                    cur = self.get_left_sub_tree(cur)
                else:
                    cur.make_left_sub_tree(cur, new_node)
                    break
            else:
                if self.get_right_sub_tree(cur):
                    cur = self.get_right_sub_tree(cur)
                else:
                    self.make_right_sub_tree(cur, new_node)
                    break

    def search(self, target):
        cur = self.get_root()

        while cur != None:
            if target == self.get_node_data(cur):
                return cur
            elif target < self.get_node_data(cur):
                cur = self.get_left_sub_tree(cur)
            else:
                cur = self.get_right_sub_tree(cur)

        return cur

    def remove_left_sub_tree(self, cur):
        del_node = self.get_left_sub_tree(cur)
        self.make_left_sub_tree(cur, None)
        return del_node

    def remove_right_sub_tree(self, cur):
        del_node = self.get_right_sub_tree(cur)
        self.make_right_sub_tree(cur, None)
        return del_node

    def remove_leaf(self, parent, del_node):
        if del_node == self.get_root():
            self.set_root(None)
            return del_node

        if self.get_left_sub_tree(parent) == del_node:
            self.remove_left_sub_tree(parent)
        else:
            self.remove_right_sub_tree(parent)
        return del_node

    def remove_one_child(self, parent, del_node):
        pass

    def remove_two_children(self, del_node):
        pass

    def remove(self, target):
        del_parent = self.get_root()
        del_node = self.get_root()

        while True:
            if del_node == None:
                return None

            if target == self.get_node_data(del_node):
                break
            elif target < self.get_node_data(del_node):
                del_parent = del_node
                del_node = self.get_left_sub_tree(del_node)
            else:
                del_parent = del_node
                del_node = self.get_right_sub_tree(del_node)
            
        if self.get_left_sub_tree(del_node) == None and self.get_right_sub_tree(del_node) == None:
            return self.remove_leaf(del_parent, del_node)

        elif self.get_left_sub_tree(del_node) == None or self.get_right_sub_tree(del_node) == None:
            return self.remove_one_child(del_parent, del_node)

        else:
            return self.remove_two_children(del_node)




if __name__ == "__main__":
    bt = BinaryTree()

    n1 = bt.make_node()
    bt.set_node_data(n1, 1)

    n2 = bt.make_node()
    bt.set_node_data(n2, 2)

    n3 = bt.make_node()
    bt.set_node_data(n3, 3)

    n4 = bt.make_node()
    bt.set_node_data(n4, 4)

    n5 = bt.make_node()
    bt.set_node_data(n5, 5)

    n6 = bt.make_node()
    bt.set_node_data(n6, 6)

    n7 = bt.make_node()
    bt.set_node_data(n7, 7)
    
    bt.set_root(n1)
    bt.make_left_sub_tree(bt.get_root(), n2)
    bt.make_right_sub_tree(bt.get_root(), n3)

    bt.make_left_sub_tree(n2, n4)
    bt.make_right_sub_tree(n2, n5)

    bt.make_left_sub_tree(n3, n6)
    bt.make_right_sub_tree(n3, n7)

    f = lambda x: print(x, end = ' ')
    bt.preorder_traverse(bt.get_root(), f)
    print("")
    bt.inorder_traverse(bt.get_root(), f)
    print("")
    bt.postorder_traverse(bt.get_root(), f)
    print("")
    
    n8 = bt.make_node()
    bt.set_node_data(n8, 8)
    bt.make_right_sub_tree(bt.get_root(), n8)
    bt.make_right_sub_tree(n8, n3)
    
    bt.preorder_traverse(bt.get_root(), f)
    print("")
