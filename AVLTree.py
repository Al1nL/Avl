# username - alinl
# id1      - complete info
# name1    - complete info
# id2      - complete info
# name2    - complete info


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

    """returns whether self is not a virtual node 

    @rtype: bool
    @returns: False if self is a virtual node, True otherwise.
    """

    def is_real_node(self):
        if self.key != None:
            return True
        return False


"""
A class implementing an AVL tree.
"""


class AVLTree(object):
    """
    Constructor, you are allowed to add more fields.

    """

    def __init__(self):
        self.root = None
        self.size = 0

    """searches for a node in the dictionary corresponding to the key

    @type key: int
    @param key: a key to be searched
    @rtype: AVLNode
    @returns: node corresponding to key
    """

    def search(self, key):
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

        return -1

    """deletes node from the dictionary

    @type node: AVLNode
    @pre: node is a real pointer to a node in self
    @rtype: int
    @returns: the number of rebalancing operation due to AVL rebalancing
    """

    def delete(self, node):
        return -1

    """returns an array representing dictionary 

    @rtype: list
    @returns: a sorted list according to key of touples (key, value) representing the data structure
    """

    def avl_to_array(self):

        return None

    """returns the number of items in dictionary 

    @rtype: int
    @returns: the number of items in dictionary 
    """

    def size(self):
        sum = (1 if self.root.is_real_node() else 0)
        if self.root.left.is_real_node():
            sum += self.root.left.size
        if self.root.right.is_real_node():
            sum += self.root.right.size
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
        while curr != None:
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
    return self.root if self.root.is_real_node() else None
