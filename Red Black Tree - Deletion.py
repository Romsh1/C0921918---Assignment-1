# Romika Chaudhary
# Assignment 5 - Red Black Tree (Deletion)
# April 12, 2024

class Node:

    def __init__(self,key=None, color=None):
        self.key = key
        self.color = color #'R' or 'B'
        self.left = None
        self.right = None
        self.parent = None

class RedBlackTree:

    def __init__(self):
        self.root = None
        self.size = 0

    def insertVal(self, key):
        self.insert(None, key)
    
    def insert(self, pointer, key):
        #case 0: root (tree is empty)
        if self.root is None:
            self.root = Node(key, 'B')
            ##self.size += 1
        else:

            if pointer is None: #None is an inital insert call
              parentNode, childNode = self.findInsertPoint(key, self.root)
            else: #recursive call case
                childNode = pointer
                parentNode = pointer.parent

            if parentNode.parent is not None:
                if key < self.root.key: #uncle of insertion point is on the right
                  uncleNode = parentNode.parent.right
                else: #uncle of insertion point is on the left
                  uncleNode = parentNode.parent.left
            
                if uncleNode is not None and uncleNode.color == 'R': #case 1: uncle is red
                    self.redUncleCase(childNode, uncleNode)
                else: #case 2 subcases: uncle is black
                    if key > self.root.key and parentNode.color == 'R' and parentNode.right is not None and  parentNode.right.color == 'R': ##case 2.1: RR_Case
                        self.RightRightCase(childNode, uncleNode)
                    elif key < self.root.key and parentNode.color == 'R' and parentNode.left is not None and parentNode.left.color == 'R': ##case 2.2: LL_Case
                        self.LeftLeftCase(childNode, uncleNode)
                    elif key > self.root.key and parentNode.color == 'R' and parentNode.left is not None and parentNode.left.color == 'R': ##case 2.3: RL_Case
                        self.RightLeftCase(childNode, uncleNode)
                    elif key < self.root.key and parentNode.color == 'R' and parentNode.right is not None and parentNode.right.color == 'R': ##case 2.3: LR_Case
                        self.LeftRightCase(childNode, uncleNode)

                if parentNode.parent.parent is not None and parentNode.parent.color == 'R' and parentNode.parent.parent.color == 'R':
                   self.insert(parentNode.parent, parentNode.parent.key)

            if pointer is None:    
               self.size += 1

            if self.root.color != 'B':
                self.root.color = 'B'
         
    
    def redUncleCase(self, childNode, uncleNode):
        parentNode = childNode.parent
        grandparentNode = parentNode.parent

        #recolouring case
        parentNode.color = 'B'
        uncleNode.color = 'B'
        grandparentNode.color = 'R'

    ###TODO: Complete the below funcitons######
    def RightRightCase(self, childNode, unclenNode):
        parentNode = childNode.parent
        grandparentNode = parentNode.parent

        grandparentNode.parent.right = parentNode
        grandparentNode.left = None
        parentNode.parent = grandparentNode.parent
        parentNode.left = grandparentNode
        grandparentNode.parent = parentNode
    
        
        grandparentNode.color = 'R'
        parentNode.color = 'B'

    def RightLeftCase(self, childNode, unclenNode):
        parentNode = childNode.parent
        grandparentNode = parentNode.parent

        grandparentNode.right = childNode
        childNode.parent = grandparentNode
        childNode.right= parentNode
        parentNode.parent = childNode

        parentNode.left = None

        self.RightRightCase(parentNode, grandparentNode.parent.left)

    def LeftLeftCase(self, childNode, uncleNode):
        parentNode = childNode.parent
        grandparentNode = parentNode.parent

        grandparentNode.parent.left = parentNode
        grandparentNode.left = None
        parentNode.parent = grandparentNode.parent
        parentNode.right = grandparentNode
        grandparentNode.parent = parentNode
    
        
        grandparentNode.color = 'R'
        parentNode.color = 'B'

    def LeftRightCase(self, childNode, uncleNode):
        parentNode = childNode.parent
        grandparentNode = parentNode.parent

        grandparentNode.left = childNode
        childNode.parent = grandparentNode
        childNode.left = parentNode
        parentNode.parent = childNode

        parentNode.right = None

        self.LeftLeftCase(parentNode, grandparentNode.parent.right)
        
    #############################################

    def findInsertPoint(self, key, node):

        precursor = None
        cursor = self.root

        while(cursor is not None):
            precursor = cursor
            if key > cursor.key:
                cursor = cursor.right
            else:
                cursor = cursor.left

        child = None
        if key > precursor.key:
            child = precursor.right = Node(key, 'R')
            precursor.right.parent = precursor
        else:
            child = precursor.left = Node(key, 'R')
            precursor.left.parent = precursor
        
        return precursor, child #return parent, child pointers
    
    def delete(self, key):

        cursor = self.root

        while(cursor.key != key):
            if key > cursor.key:
                cursor = cursor.right
            else:
                cursor = cursor.left
        
        if cursor is None:
            raise Exception(str(key) + "is not in the tree")
        
        nodeToBeDelete = cursor
        origrinalColor = nodeToBeDelete.color
        self.bstDelete(nodeToBeDelete)

        """ if nodeToBeDelete.left is None:
           x = nodeToBeDelete.right
           x.parent = nodeToBeDelete.parent
           nodeToBeDelete.parent.right = x

           nodeToBeDelete.parent = None
           nodeToBeDelete.right = None
           x.color = origrinalColor
        elif nodeToBeDelete.right is None:
           x = nodeToBeDelete.left
           x.parent = nodeToBeDelete.parent
           nodeToBeDelete.parent.left = x

           nodeToBeDelete.parent = None
           nodeToBeDelete.left = None
           x.color = origrinalColor
        else:
           print() """
        
    def bstDelete(self, nodeToBeDelete):
        parent = nodeToBeDelete.parent
        #case 1: delete a leaf node
        if nodeToBeDelete.right is None and nodeToBeDelete.left is None:
           if parent.key > nodeToBeDelete.key:
               parent.left = None
           else:
               parent.right = None
           nodeToBeDelete.parent = None
        # case 2: node to delete only has 1 child
        elif nodeToBeDelete.left is None and nodeToBeDelete.right is not None:
            print("T1")
            if nodeToBeDelete.key > parent.key:
               parent.right = nodeToBeDelete.right
            else:
                parent.left = nodeToBeDelete.right

            nodeToBeDelete.right.parent = parent

            nodeToBeDelete.parent = None
            nodeToBeDelete.right = None

        elif nodeToBeDelete.right is None and nodeToBeDelete.left is not None:
          
           if nodeToBeDelete.key > parent.key:
               parent.right = nodeToBeDelete.left
           else:
                parent.left = nodeToBeDelete.left
                
           nodeToBeDelete.left.parent = parent

           nodeToBeDelete.parent = None
           nodeToBeDelete.left = None
        else:
            successor = nodeToBeDelete.right
            while(successor.left is not None):
                successor = successor.left
            
            nodeToBeDelete.key = successor.key

            successor.parent.left = None
            successor.parent = None

   
  


#main
rbt = RedBlackTree()
rbt.insertVal(50)
rbt.insertVal(30)
rbt.insertVal(70)
rbt.insertVal(20)
rbt.insertVal(40)
rbt.insertVal(60)
rbt.insertVal(80)

rbt.delete(50)
# rbt.insertVal(12)
# rbt.insertVal(8)
# rbt.insertVal(14)

# rbt.insertVal(15)
# rbt.insertVal(16)
# rbt.insertVal(6)
# rbt.insertVal(4)
# rbt.insertVal(2)
# rbt.insertVal(3)
# rbt.insertVal(20)
# rbt.insertVal(18)
# rbt.insertVal(21)
# rbt.insertVal(1)

# rbt.delete(20)
# rbt.delete(2)


print(rbt.root.key, rbt.root.color, rbt.root.parent)
print(rbt.root.left.key, rbt.root.left.color, rbt.root.left.parent.key)
print(rbt.root.left.left.key, rbt.root.left.left.color, rbt.root.left.left.parent.key)
print(rbt.root.left.right.key, rbt.root.left.right.color, rbt.root.left.right.parent.key)
#print(rbt.root.left.left.left.key, rbt.root.left.left.left.color, rbt.root.left.left.left.parent.key)
# print(rbt.root.left.left.right.key, rbt.root.left.left.right.color, rbt.root.left.left.right.parent.key)
print(rbt.root.right.key, rbt.root.right.color, rbt.root.right.parent.key)
#print(rbt.root.right.left.key, rbt.root.right.left.color, rbt.root.right.left.parent.key)
print(rbt.root.right.right.key, rbt.root.right.right.color, rbt.root.right.right.parent.key)
# print(rbt.root.right.right.left.key, rbt.root.right.right.left.color, rbt.root.right.right.left.parent.key)
# print(rbt.root.right.right.right.key, rbt.root.right.right.right.color, rbt.root.right.right.right.parent.key)
