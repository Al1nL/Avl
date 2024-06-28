# username - alinl
# id1      - complete info
# name1    - complete info
# id2      - 324022904
# name2    - Lior Pernik \ ליאור פרניק
import TreePrint  # remove before submmision

"""A class represnting a node in an AVL tree"""


class AVLNode(object):
    """Constructor, you are allowed to add more fields.

    @type key: int or None
    @param key: key of your node
    @type value: string
    @param value: data of your node
    """

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.parent = None
        self.height = -1
        self.size = 0

    """Updates the fields of a new node to be real 
    """
    def update_node_fields(self):
        self.height = 0
        self.size = 1
        self.left = AVLNode(None, "")
        self.left.parent = self
        self.right = AVLNode(None, "")
        self.right.parent = self

    """returns whether self is not a virtual node 

    @rtype: bool
    @returns: False if self is a virtual node, True otherwise.
    """

    def is_real_node(self):
        if self.key != None:
            return True
        return False

    def get_BF(self):
        left = self.left.height if self.left != None else -1
        right = self.right.height if self.right != None else -1
        return left - right

    def get_balance_factor(self):
        left = self.left.height if self.left != None else -1
        right = self.right.height if self.right != None else -1
        return left - right

    def set_size(self):
        self.size = 1
        if self.left:
            self.size += self.left.size
        if self.right:
            self.size += self.right.size

    def set_height(self):
        m = n = -1
        if self.right:
            m = self.right.height
        if self.left:
            n = self.left.height
        self.height = max(m, n) + 1

    def get_key(self):
        return self.key
    def get_left(self):
        return self.left if self.left != None else None
    def get_right(self):
        return self.right if self.right != None else None
    def get_height(self):
        return self.height
    def get_size(self):
        return self.size
    def get_value(self):
        return self.value
    def get_parent(self):
        return self.parent

"""
A class implementing an AVL tree.
"""


class AVLTree(object):
    """
    Constructor, you are allowed to add more fields.

    """

    def __init__(self):
        self.root = None

    ## for printing the tree - delete after tests********
    def __repr__(self):
        out = ""
        for row in TreePrint.printree(self.root):  # need printree.py file
            out = out + row + "\n"
        return out

    """searches for a node in the dictionary corresponding to the key

    @type key: int
    @param key: a key to be searched
    @rtype: AVLNode
    @returns: node corresponding to key
    """

    def search(self, key):

        node = self.root
        while node != None and node.is_real_node():
            if node.key == key:
                return node
            elif node.key < key:
                node = node.right
            else:
                node = node.left

        return None

    """inserts a new node into the dictionary with corresponding key and value

    @type key: int
    @pre: key currently does not appear in the dictionary
    @param key: key of item that is to be inserted to self
    @type val: string
    @param val: the value of the item
    @rtype: int
    @returns: the number of rebalancing operation due to AVL rebalancing
    """

    def insert(self, key, val):
        node = self.root
        new = AVLNode(key, val)
        new.update_node_fields()

        parent = None
        while node != None and node.is_real_node():
            parent = node
            if node.key < key:
                node = node.right
            else:
                node = node.left

        if parent == None:
            self.root = new
            new.left.parent = self.root
            new.right.parent = self.root
            return
        elif key < parent.key:
            parent.left = new
        else:
            parent.right = new
        new.parent = parent

        return self.fix_tree(parent)

    def update_sub_tree(self,parent, node):
        node.parent = parent
        node.set_height()
        node.set_size()

        if parent != None:
            if parent.key > node.key:
                parent.left = node
            else:
                parent.right = node
            parent.set_height()
            parent.set_size()

    def delete_node(self,parent, node):
        node_change = node.right if node.right.is_real_node() else node.left
        if node is self.root and node_change.is_real_node():
            self.root = node_change
            self.root.set_height()
            self.root.set_size()
            node_change.parent = None

        elif node is self.root:
            self.root = None

        elif parent != None:
            if parent.key > node.key:
                parent.left = node_change
            else:
                parent.right = node_change
            node_change.parent = parent
            parent.set_height()
            parent.set_size()

    def fix_tree(self,parent):
        rotation_count = 0
        while parent != None:

            prev_height = parent.height
            parent.set_height()

            parent.set_size()
            BF = abs(parent.get_BF())

            if BF < 2 and parent.height != prev_height:
                parent = parent.parent
            elif BF == 2:
                rotation_count += self.rotation(parent)
            else:
                parent = parent.parent

        return rotation_count

    def rotation(self, parent, rotate=()):
        def rotate_right(node):
            new_parent = node.left
            node.left = new_parent.right
            node.left.parent = node
            new_parent.right = node
            new_parent.parent = node.parent

            self.update_sub_tree(new_parent, node)
            self.update_sub_tree(new_parent.parent, new_parent)

        def rotate_left(node):
            new_parent = node.right
            node.right = new_parent.left
            node.right.parent = node
            new_parent.left = node
            new_parent.parent = node.parent

            self.update_sub_tree(new_parent, node)
            self.update_sub_tree(new_parent.parent, new_parent)

        if (rotate == ()):
            bf = parent.get_BF()
            if bf > 0:
                other_bf = parent.left.get_BF()
            else:
                other_bf = parent.right.get_BF()

            rotate = (bf, other_bf)
            rotation_count = 1 if rotate == (-2, -1) or rotate == (2, 1) else 2

        match rotate:
            case (-2, -1) | (-2, 0):
                rotate_left(parent)

            case (-2, 1):
                rotate_right(parent.right)
                rotate_left(parent)

            case (2, -1):
                rotate_left(parent.left)
                rotate_right(parent)


            case (2, 1) | (2,0):
                rotate_right(parent)


        if self.root == parent:
            self.root = parent.parent

        return rotation_count


    """deletes node from the dictionary
    
    @type node: AVLNode
    @pre: node is a real pointer to a node in self
    @rtype: int
    @returns: the number of rebalancing operation due to AVL rebalancing
    """


    def delete(self, node):
        parent = node.parent
        count_rotations = 0
        if not node.left.is_real_node() or not node.right.is_real_node(): # case 1 and 2
            self.delete_node(parent, node)
            count_rotations = self.fix_tree(parent)
        else:
            successor = self.select(self.rank(node) +1)
            tmp = successor.parent
            self.delete_node(successor.parent, successor)
            if node == self.root:
                self.root = successor

            successor.left = node.left
            successor.right = node.right

            successor.left.parent = successor
            successor.right.parent = successor
            self.update_sub_tree(parent, successor)
            if tmp.key > successor.key:
                count_rotations = self.fix_tree(tmp)
            else:
                count_rotations = self.fix_tree(successor)

        return count_rotations


    """returns an array representing dictionary 
    
    @rtype: list
    @returns: a sorted list according to key of touples (key, value) representing the data structure
    """


    def avl_to_array(self):
        array = []

        def to_array(node, array):
            if node != None and node.is_real_node():
                to_array(node.left, array)
                array.append((node.key, node.value))
                to_array(node.right, array)

        to_array(self.root, array)
        return array


    """returns the number of items in dictionary 
    
    @rtype: int
    @returns: the number of items in dictionary 
    """


    def size(self):
        sum = 0
        if self.root != None:
            sum += self.root.size
        return sum


    """compute the rank of node in the dictionary
    
    @type node: AVLNode
    @pre: node is in self
    @param node: a node in the dictionary to compute the rank for
    @rtype: int
    @returns: the rank of node in self
    """


    def rank(self, node):
        rank = node.left.size + 1
        curr = node
        while curr != None and curr.parent != None:
            if curr == curr.parent.right:  # curr is the right son
                rank += curr.parent.left.size + 1
            curr = curr.parent
        return rank

    """finds the i'th smallest item (according to keys) in the dictionary
    
    @type i: int
    @pre: 1 <= i <= self.size()
    @param i: the rank to be selected in self
    @rtype: AVLNode
    @returns: the node of rank i in self
    """


    def select(self, i):
        def select_rec(node, i):
            rank = node.left.size + 1
            if i == rank:
                return node
            elif i < rank:
                return select_rec(node.left, i)
            else:
                return select_rec(node.right, i - rank)

        return select_rec(self.root, i)


    """finds the node with the largest value in a specified range of keys
    
    @type a: int
    @param a: the lower end of the range
    @type b: int
    @param b: the upper end of the range
    @pre: a<b
    @rtype: AVLNode
    @returns: the node with maximal (lexicographically) value having a<=key<=b, or None if no such keys exist
    """


    def max_range(self, a, b):
        def find_max(node, a, b, max_val):
            if node.key == a or node.key == b:
                return max(max_val, node.val)
            left_max = find_max(node.left, a, b, max_val)
            max_val = max(left_max, max_val)
            find_max(node.right, a, b, max_val)

        curr = self.root
        while curr.key < a or curr.key > b:
            if curr.key > b:
                curr = curr.left
            elif curr.key < a:
                curr = curr.right

        return find_max(curr, a, b, curr.val)


    """returns the root of the tree representing the dictionary
    
    @rtype: AVLNode
    @returns: the root, None if the dictionary is empty
    """


    def get_root(self):
        return self.root

