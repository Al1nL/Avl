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

	def get_BF(self):
		return self.left.height - self.right.height

	def set_size(self):
		self.size = 1
		if self.left:
			self.size += self.left.size
		if self.right:
			self.size += self.right.size


	def set_height(self):
		self.height = 1
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
        self.size = 0


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
		new.height = 0
		new.size = 1
		new.left = AVLNode(None, "")
		new.right = AVLNode(None, "")

		parent = None
		while node != None and node.is_real_node():
			parent = node
			if node.key < key:
				node = node.right
			else:
				node = node.left


		if parent == None:
			self.root = new
			return
		elif key < parent.key:
			parent.left = new
		else:
			parent.right = new
		new.parent = parent

		while parent != None:

			prev_height = parent.height
			parent.height = max(parent.left.height, parent.right.height) + 1

			parent.size = 1 + parent.left.size + parent.right.size
			BF = abs(parent.get_BF())

			if BF < 2 and parent.height != prev_height:
				parent = parent.parent
			elif BF == 2:
				self.rotation(parent)
			else:
				parent = parent.parent
		return

	def rotation(self, parent, rotate = ()):

		if(rotate == ()):
			bf = parent.get_BF()
			if bf >0:
				other_bf = parent.left.get_BF()
			else:
				other_bf = parent.right.get_BF()

			rotate = (bf, other_bf)

		match rotate:
			case (-2,-1):

				if parent.parent != None:
					# 3 -> 7
					parent.parent.right = parent.right
				# 7 parent = 3
				parent.right.parent = parent.parent
				# 6 parent = 7
				parent.parent = parent.right

				new_parent = parent.right
				# 6 right -> 7 left
				parent.right = parent.right.left
				# 7 left -> 6
				new_parent.left = parent


			case (-2,1):
				# tmp = parent.right
				# parent.right = parent.right.left
				# parent.right.right = tmp
				# parent.right.left = parent
				self.rotation(parent, (2,1))
				self.rotation(parent.right, (-2,-1))

			case (2,-1):
				tmp = parent.left
				parent.left = parent.left.right
				parent.left.left = tmp
				parent.left.right = parent

			case (2,1):
				# parent.left.right = parent

				# 3 -> 7
				if parent.parent != None:
					parent.parent.left = parent.left
				# 7 parent = 3
				parent.left.parent = parent.parent
				# 6 parent = 7
				parent.parent = parent.left

				new_parent = parent.left
				# 6 right -> 7 left
				parent.left = parent.left.right
				# 7 left -> 6
				new_parent.right = parent

		parent.set_size()
		parent.set_height()
		if self.root == parent:
			self.root = parent.parent
		return

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
		array = []
		def to_array(node, array):
			if node != None and node.is_real_node():
				to_array(node.left, array)
				array.append(node)
				to_array(node.right, array)

		to_array(self.root, array)
		return array


	"""returns the number of items in dictionary 

	@rtype: int
	@returns: the number of items in dictionary 
	"""
	def size(self):
		sum = (1 if self.root != None else 0)
		if self.root != None:
			if self.root.left != None:
				sum += self.root.left.size
			if self.root.right != None:
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
		""""𝑟 ← 𝑥.𝑙𝑒𝑓𝑡.𝑠𝑖𝑧𝑒 + 1
		𝑦 ← 𝑥
		while 𝑦 ≠ 𝑛𝑢𝑙𝑙
		if 𝑦 = 𝑦.𝑝𝑎𝑟𝑒𝑛𝑡.𝑟𝑖𝑔ℎ𝑡  # 𝑦 is a right son
		𝑟 ← 𝑟 + 𝑦.𝑝𝑎𝑟𝑒𝑛𝑡.𝑙𝑒𝑓𝑡.𝑠𝑖𝑧𝑒 + 1
		𝑦 ← 𝑦.𝑝𝑎𝑟𝑒𝑛𝑡
		"""

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


if __name__ == '__main__':
	tree = AVLTree()
	tree.insert(6,"hello")
	tree.insert(8,"hello")
	tree.insert(7,"hello")
	tree.insert(0,"hello")
	tree.insert(1,"hello")