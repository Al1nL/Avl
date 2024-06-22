#username - alinl
#id1      - complete info 
#name1    - complete info 
#id2      - complete info
#name2    - complete info  



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
		while node.is_real_node():
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
		parent = None
		while node.is_real_node():
			parent = node
			if node.key < key:
				node = node.right
			else:
				node = node.left


		if not parent.is_real_node():
			parent = new
		elif key < parent.key:
			parent.left = new
		else:
			parent.right = new

		prev_height = parent.height
		parent.height = max(parent.left.height, parent.right.height) +1

		while parent.is_real_node():
			BF = abs(parent.get_BF())
			if BF < 2 and parent.height != prev_height:
				self.rotation((parent.left.get_BF(), parent.right.get_BF()), parent)
		return -1

	def rotation(self, rotate, parent):
		match rotate:
			case (-2,-1):
				parent.right.left = parent

			case (-2,1):
				tmp = parent.right
				parent.right = parent.right.left
				parent.right.right = tmp
				parent.right.left = parent
			case (2,-1):
				tmp = parent.left
				parent.left = parent.left.right
				parent.left.left = tmp
				parent.left.right = parent
			case (2,1):
				parent.left.right = parent

		parent.left = None
		parent.right = None

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
			if node.is_real_node():
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
		""""𝑟 ← 𝑥.𝑙𝑒𝑓𝑡.𝑠𝑖𝑧𝑒 + 1
		𝑦 ← 𝑥
		while 𝑦 ≠ 𝑛𝑢𝑙𝑙
		if 𝑦 = 𝑦.𝑝𝑎𝑟𝑒𝑛𝑡.𝑟𝑖𝑔ℎ𝑡  # 𝑦 is a right son
		𝑟 ← 𝑟 + 𝑦.𝑝𝑎𝑟𝑒𝑛𝑡.𝑙𝑒𝑓𝑡.𝑠𝑖𝑧𝑒 + 1
		𝑦 ← 𝑦.𝑝𝑎𝑟𝑒𝑛𝑡
		"""

		return -1


	"""finds the i'th smallest item (according to keys) in the dictionary

	@type i: int
	@pre: 1 <= i <= self.size()
	@param i: the rank to be selected in self
	@rtype: AVLNode
	@returns: the node of rank i in self
	"""
	def select(self, i):
		"""
		1. 𝑟 → 𝑥. 𝑙𝑒𝑓𝑡. 𝑠𝑖𝑧𝑒 + 1
		2. if 𝑘 = 𝑟
		2.1 return 𝑥
		3. else if 𝑘 < 𝑟
		3.1 return Tree-Select-rec(𝑥. 𝑙𝑒𝑓𝑡, 𝑘)
		4. else return Tree-Select-rec(𝑥. 𝑟𝑖𝑔ℎ𝑡, 𝑘 – 𝑟)
		"""

		return None


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


		return None


	"""returns the root of the tree representing the dictionary

	@rtype: AVLNode
	@returns: the root, None if the dictionary is empty
	"""
	def get_root(self):
		return self.root if self.root.is_real_node() else None
