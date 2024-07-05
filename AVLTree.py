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

    """Updates the fields of a new node to be real and attaching 2 virtual nodes
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
    """
    @rtype: int 
    @return: balance factor of node. calculated from left and right
    """
    def get_BF(self):
        left = self.left.height if self.left != None else -1
        right = self.right.height if self.right != None else -1
        return left - right

    """
    @summary: calculated new size from left and right nodes
    """
    def set_size(self):
        self.size = 1
        if self.left:
            self.size += self.left.size
        if self.right:
            self.size += self.right.size

    """
    @summary: calculated new height from left and right nodes
    """
    def set_height(self):
        m = n = -1
        if self.right:
            m = self.right.height
        if self.left:
            n = self.left.height
        self.height = max(m, n) + 1

"""
A class implementing an AVL tree.
"""

class AVLTree(object):
    """
    Constructor, you are allowed to add more fields.

    """
    def __init__(self):
        self.root = None

    """searches for a node in the dictionary corresponding to the key
        using binary search.
    @type key: int
    @param key: a key to be searched
    @rtype: AVLNode
    @returns: node corresponding to key
    @note: time complexity: O(log n)
    """
    def search(self, key):

        node = self.root
        #loop for binary search with key O(log n)
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
    @note: time complexity: O(log n)
    """
    def insert(self, key, val):
        node = self.root
        new = AVLNode(key, val)
        new.update_node_fields()

        parent = None
        # find parent for new node using binary search
        while node != None and node.is_real_node():
            parent = node
            if node.key < key:
                node = node.right
            else:
                node = node.left

        # check if new node is root or left / right child
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

        # fix tree balance factors with rotations
        return self.fix_tree(parent)

    """
    @param: node, parent: parent to update, node: node to be updated as a child of `parent`.
    @summary: Update the subtree rooted at `parent` with `node` as its child.
    """
    def update_sub_tree(self,parent, node):
        # Set `node`'s parent to `parent`.
        node.parent = parent

        # Update `node`'s height and size based on its subtree.
        node.set_height()
        node.set_size()

        if parent != None:
            # Determine whether `node` should be the left or right child of `parent`.
            if parent.key > node.key:
                parent.left = node
            else:
                parent.right = node

            # Update `parent`'s height and size after modifying its child.
            parent.set_height()
            parent.set_size()

    """
    @param: parent: The parent node of `node`, node: The node to be deleted from the AVL tree.
    @summary: Delete `node` from the AVL tree, replacing it with its appropriate child node.
    """
    def delete_node(self,parent, node):
        # Determine the replacement node based on `node`'s children.
        node_change = node.right if node.right.is_real_node() else node.left

        # Case 1: `node` is the root and has a valid replacement.
        if node is self.root and node_change.is_real_node():
            # Update `self.root` to `node_change`, adjust height and size.
            self.root = node_change
            self.root.set_height()
            self.root.set_size()
            node_change.parent = None # Remove parent reference for the new root.

        # Case 2: `node` is the root and has no children (leaf node).
        elif node is self.root:
            self.root = None

        # Case 3: `node` has a parent and is not the root.
        elif parent != None:
            # Determine if `node` is a left or right child of `parent`
            if parent.key > node.key:
                parent.left = node_change
            else:
                parent.right = node_change

            # Update `node_change`'s parent and adjust parent's height and size.
            node_change.parent = parent
            parent.set_height()
            parent.set_size()

    """
       @params: parent: The starting node from which to fix the AVL tree.
       @summary: Perform AVL tree fix starting from `parent` up to the root.
       @return: The total count of rotations performed during fixing.
       @note: time complexity: O(log n)
    """
    def fix_tree(self,parent):
        rotation_count = 0

        # Traverse up the tree until reaching the root (parent becomes None).
        while parent != None:

            prev_height = parent.height

            # Update `parent`'s height and size after adjustments.
            parent.set_height()
            parent.set_size()

            BF = abs(parent.get_BF())

            # If balance factor is within [-1, 1] and height changed, move to parent's parent
            if BF < 2 and parent.height != prev_height:
                parent = parent.parent

            # If balance factor is 2, perform rotations and update rotation count.
            elif BF == 2:
                rotation_count += self.rotation(parent)

            # Keep updating height and size of parents
            else:
                parent = parent.parent

        return rotation_count

    """
    Perform rotation operations on the AVL tree to balance it.
    @param: parent: parent of deleted / inserted node, rotate = tuple that indicates what rotation is performed
    @return: number of rotations
    """
    def rotation(self, parent, rotate=()):

        def rotate_right(node):
            """
                Perform a right rotation on the given node.

                Args:
                    node: The node around which rotation is performed.
            """

            # Set `new_parent` to `node`'s left child.
            new_parent = node.left

            # Adjust `node`'s left child to `new_parent`'s right child.
            node.left = new_parent.right

            # Update parent pointers to reflect the new structure.
            node.left.parent = node

            # Make `node` the right child of `new_parent`.
            new_parent.right = node

            # Update `new_parent`'s parent to match `node`'s current parent.
            new_parent.parent = node.parent

            # Update subtree to reflect the changes made by the rotation.
            self.update_sub_tree(new_parent, node)
            self.update_sub_tree(new_parent.parent, new_parent)

        def rotate_left(node):
            """
                Perform a left rotation on the given node.

                Args:
                    node: The node around which rotation is performed.
            """

            # Set `new_parent` to `node`'s right child.
            new_parent = node.right

            # Adjust `node`'s right child to `new_parent`'s left child.
            node.right = new_parent.left

            # Update parent pointers to reflect the new structure.
            node.right.parent = node

            # Make `node` the left child of `new_parent`.
            new_parent.left = node

            # Update `new_parent`'s parent to match `node`'s current parent.
            new_parent.parent = node.parent

            # Update subtree to reflect the changes made by the rotation.
            self.update_sub_tree(new_parent, node)
            self.update_sub_tree(new_parent.parent, new_parent)

        # If rotate parameter is not provided, determine it based on parent's balance factor
        if rotate == ():
            bf = parent.get_BF()
            if bf > 0:
                other_bf = parent.left.get_BF()
            else:
                other_bf = parent.right.get_BF()

            rotate = (bf, other_bf)

        # determine rotation count based on type
        rotation_count = 1 if rotate == (-2, -1) or rotate == (2, 1) else 2

        # Perform rotation based on the balance factors (rotate tuple)
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

        # Adjust root if necessary
        if self.root == parent:
            self.root = parent.parent

        return rotation_count


    """deletes node from the dictionary
    
    @type node: AVLNode
    @pre: node is a real pointer to a node in self
    @rtype: int
    @returns: the number of rebalancing operation due to AVL rebalancing
    @note: time complexity: O(log n)
    """
    def delete(self, node):
        parent = node.parent
        count_rotations = 0

        # Check if either left or right child of `node` is not a real node (leaf or single child).
        if not node.left.is_real_node() or not node.right.is_real_node():
            # Delete the node and adjust the tree structure.
            self.delete_node(parent, node)
            # Fix the AVL tree structure starting from `parent` and update rotation count.
            count_rotations = self.fix_tree(parent)
        else:
            # Find the successor node to replace `node`.
            successor = self.select(self.rank(node) +1)
            tmp = successor.parent

            # Delete the successor node and adjust the tree structure.
            self.delete_node(successor.parent, successor)

            # If `node` is the root, update `self.root` to point to the successor.
            if node == self.root:
                self.root = successor

            # Link `node`'s left and right children to the successor node.
            successor.left = node.left
            successor.right = node.right

            # Update parent pointers for `successor`'s new children.
            successor.left.parent = successor
            successor.right.parent = successor

            # Update subtree structure.
            self.update_sub_tree(parent, successor)

            # Determine which node to fix AVL balance starting from based on key comparison.
            # key depends on if successor was taken from right or after going up.
            if tmp.key > successor.key:
                count_rotations = self.fix_tree(tmp)
            else:
                count_rotations = self.fix_tree(successor)

        return count_rotations


    """returns an array representing dictionary 
    
    @rtype: list
    @returns: a sorted list according to key of touples (key, value) representing the data structure
    @note: time complexity: O(n)
    """
    def avl_to_array(self):
        array = []

        def to_array(node, array):
            """
                This function performs an inorder of the AVL tree and collects
                 key-value pairs into the `array`.
            """
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
    @note: time complexity: O(log n)
    """
    def rank(self, node):
        rank = node.left.size + 1
        curr = node
        while curr != None and curr.parent != None:
            if curr == curr.parent.right:
                rank += curr.parent.left.size + 1
            curr = curr.parent
        return rank

    """finds the i'th smallest item (according to keys) in the dictionary
    
    @type i: int
    @pre: 1 <= i <= self.size()
    @param i: the rank to be selected in self
    @rtype: AVLNode
    @returns: the node of rank i in self
    @note: time complexity: O(log n)
    """
    def select(self, i):

        # Recursively find the ith smallest node (by rank) in the AVL tree rooted at `node`.
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
    @note: time complexity: O(n)
    """
    def max_range(self, a, b):

        """
        Recursively find the maximum value within the range [a, b] in the subtree rooted at `node`
        in-order walk
        """
        def find_max(node, a, b, max_val):
            if node.key == a or node.key == b:
                return max(max_val, node.val)
            left_max = find_max(node.left, a, b, max_val)
            max_val = max(left_max, max_val)
            find_max(node.right, a, b, max_val)

        curr = self.root
        # go down the tree until `curr` is within the range [a, b]
        while curr.key < a or curr.key > b:
            if curr.key > b:
                curr = curr.left
            elif curr.key < a:
                curr = curr.right

        # find the maximum value within the range [a, b] starting from `curr`
        return find_max(curr, a, b, curr.val)


    """returns the root of the tree representing the dictionary
    
    @rtype: AVLNode
    @returns: the root, None if the dictionary is empty
    """
    def get_root(self):
        return self.root

