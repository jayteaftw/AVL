
class AVL():

    class Node():
        def __init__(self, val=0, left=None, right=None):
            self.bf = 0
            self.height = 0
            self.value = val
            self.left = left
            self.right = right

        #Tree Display code taken from https://stackoverflow.com/questions/34012886/print-binary-tree-level-by-level-in-python
        def _display_aux(self):
            """Returns list of strings, width, height, and horizontal coordinate of the root."""
            # No child.
            if self.right is None and self.left is None:
                line = '%s' % self.value
                width = len(line)
                height = 1
                middle = width // 2
                return [line], width, height, middle

            # Only left child.
            if self.right is None:
                lines, n, p, x = self.left._display_aux()
                s = '%s' % self.value
                u = len(s)
                first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
                second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
                shifted_lines = [line + u * ' ' for line in lines]
                return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

            # Only right child.
            if self.left is None:
                lines, n, p, x = self.right._display_aux()
                s = '%s' % self.value
                u = len(s)
                first_line = s + x * '_' + (n - x) * ' '
                second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
                shifted_lines = [u * ' ' + line for line in lines]
                return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

            # Two children.
            left, n, p, x = self.left._display_aux()
            right, m, q, y = self.right._display_aux()
            s = '%s' % self.value
            u = len(s)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s + y * '_' + (m - y) * ' '
            second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '
            if p < q:
                left += [n * ' '] * (q - p)
            elif q < p:
                right += [m * ' '] * (p - q)
            zipped_lines = zip(left, right)
            lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
            return lines, n + m + u, max(p, q) + 2, n + u // 2

    def __init__(self, value):
        self.root = self.Node(value)
        self.nodeCount = 1

    def contains(self, value):
        return self._contains(self.root,value)


    def _contains(self, node, value):
        if node == None: return False

        #Looks through right subtree
        if node.value < value:
            return self._contains(node.right, value)

        #Look through left subtree    
        if node.value > value:
            return self._contains(node.left, value)
        
        return True
    
    def insert(self, value):
        if value == None: return None

        if not self.contains(value):
            self.root = self._insert(self.root, value)
            self.nodeCount += 1
            return True
        return False
    
    def _insert(self, node, value):
        
        #Base Case
        if not node: return self.Node(value)

        #Insert into left subtree
        if  value < node.value:
            node.left = self._insert(node.left, value)
        
        #Insert into right subtree
        else:
            node.right = self._insert(node.right, value)

        #Update BF and Height values
        self._update(node)

        #Rebalnce Tree
        return self._balance(node)

    def _update(self, node):
        leftNodeHeight = node.left.height if node.left else -1
        rightNodeHeight = node.right.height if node.right else -1

        #update height
        node.height = 1 + max(leftNodeHeight, rightNodeHeight)

        #update balance factor
        node.bf = rightNodeHeight - leftNodeHeight

    def _balance(self, node):
        
        #left heavy subtree
        if node.bf == -2:
            #Left Left Case
            if node.left.bf <= 0:
                return self._leftLeftCase(node)
            #Left Right Case
            else:
                return self._leftRightCase(node)
        
        #Right Heavy Subtree
        if node.bf == 2:
            #Right Right Case
            if node.right.bf >= 0:
                return self._rightRightCase(node)      
            #Right Left Case
            else:
                return self._rightLeftCase(node)


        #Node either BF 0, +1, or -1 so return node
        return node

    def _leftLeftCase(self, node):
        return self._rightRotation(node)
    
    def _leftRightCase(self, node):
        node.left = self._leftRotation(node.left)
        return self._leftLeftCase(node)

    def _rightRightCase(self, node):
        return self._leftRotation(node)

    def _rightLeftCase(self, node):
        node.right = self._rightRotation(node.right)
        x = self._rightRightCase(node)
        return x

    def _rightRotation(self, node):
        set_root = False
        if self.root == node:
            set_root = True
        
        newParent = node.left
        node.left = newParent.right
        newParent.right = node
        
        self._update(node)
        self._update(newParent)

        if set_root:
            self.root = newParent

        return newParent

    def _leftRotation(self, node):
        set_root = False
        if self.root == node:
            set_root = True

        newParent = node.right
        node.right = newParent.left
        newParent.left = node

        self._update(node)
        self._update(newParent)

        if set_root:
            self.root = newParent

        return newParent

    
    def remove(self, elem):
        if (elem is None): return False

        if self.contains(elem):
            self._remove(self.root, elem)
            self.nodeCount -= 1
            return True

        return False

    def _remove(self, node, elem):

        if not node: return None

        #Elem less than node.value go left
        if elem < node.value:
            node.left = self._remove(node.left, elem)

        #Elem greater than node.value go right
        elif elem > node.value:
            node.right = self._remove(node.right, elem)

        #Elem equal to node value: remove
        else:

            #Only Right subtree or no subtree at all
            if node.left == None:
                if node == self.root:
                    self.root = node.right
                return node.right
            
            #Only Left subtree or no subtree al all
            if node.right == None:
                if node == self.root:
                    self.root = node.left
                return node.left

            #Choose to remove from left subtree
            if node.left.height > node.right.height:

                temp = self._findMax(node.left)
                node.value = temp
                node.left = self._remove(node.left, temp)

            else:
                temp = self._findMin(node.right)
                node.value = temp
                node.right = self._remove(node.right, temp)

        #Update balance and BF
        self._update(node)

        #rebalance tree
        return self._balance(node)  
        
    def _findMin(self, node):

        while node.left:
            node = node.left   
        return node.value

    def _findMax(self, node):
        
        while node.right:
            node = node.right 
        return node.value

    def display(self, node=False):
        if not node: node = self.root
        lines, *_ = node._display_aux()
        for line in lines:
            print(line)

    
        
import random
if __name__ == "__main__":
    range_of_values = 51
    amount_of_nodes = 30
    random.seed()

    if range_of_values <= amount_of_nodes:
        print("ERROR: Range of values less than amount of nodes")
        exit()

    node_values_del = []
    avl = AVL(random.choices(range(range_of_values))[0])
    avl.display()

    i = 0
    while i < amount_of_nodes:
        x = random.choices(range(range_of_values))[0]
        added = avl.insert(x)
        if added:
            message = f"Inserting {x} into the tree\n" 
            print(message)
            node_values_del.append(x)
            
            i += 1
            #print("______________________")
        
    avl.display()    
       
    
    print(node_values_del)
    for i in node_values_del:
        print(f"Removing {i}: {avl.remove(i)} \n")
        avl.display()
        print("______________________")

    avl.display()



    

            

            



    


    









    




    

