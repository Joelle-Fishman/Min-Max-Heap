import random
import math
import pytest

class Node(object):
    
    def __init__(self, k, d):
        self.key  = k
        self.data = d
        
    def __str__(self): 
        return "(" + str(self.key) + "," + repr(self.data) + ")"
    
class MinMaxHeap(object):
    
    def __init__(self, size):
    
        #array storing heap nodes
        self.__arr = [None] * size
        
        #amount of elements in heap
        self.__nElems = 0    
        
    #returns total number of elements in heap
    def __len__(self):
        return self.__nElems
        
    def __level(self, i):
        #level of node based off index 
        return int(math.log2(i + 1))
        
    def insert(self, k, d):
                
        #None if the heap is full
        if self.__nElems == len(self.__arr): return None 
        
        #Place new node at end of heap 
        self.__arr[self.__nElems] = Node(k, d)
        
        #Push up the node (index of new node) to fix min-max heap properly
        self.__pushUp(self.__nElems)        
        
        #Increment amount of elements by 1
        self.__nElems += 1
      
    #Push up node at index 'i' to restore heap
    def __pushUp(self, i):
        
        #Parent in refrence to index
        parent = (i - 1)//2

        #If index is not the root 
        if i != 0:
            
            #If i is on MIN level
            if self.__level(i) % 2 == 0: 
                
                #Compare key with parent's key
                if self.__arr[i].key > self.__arr[parent].key:
                    
                    #Swap with parent
                    self.__arr[i], self.__arr[parent] = self.__arr[parent], self.__arr[i]
                    
                    #pushUpMax the parent
                    self.__pushUpMax(parent)
                    
                    #Otherwise i's key is less than parent's key
                    #So pushUpMin(i)
                else:
                    self.__pushUpMin(i)
                
             #If i is on MAX level        
            else:
                
                #If i's key less than parent's key
                if self.__arr[i].key < self.__arr[parent].key:
                    
                    #swap them
                    self.__arr[i], self.__arr[parent] = self.__arr[parent], self.__arr[i]
                    
                    #pushUpMin the parent
                    self.__pushUpMin(parent)
                    
                #Otherwise i's key is greater than parent's key
                #So pushUpMax(i)                
                else:
                    self.__pushUpMax(i)
            

    def __pushUpMin(self, i):
        
        #Parent and grandParent in refrence to index
        parent = (i - 1) // 2
        grandparent = (parent - 1) // 2
        
        #If grandparent exists, and current index key < grandparent key
        if grandparent >= 0 and self.__arr[grandparent].key > self.__arr[i].key:
            
            #Swap the keys
            self.__arr[i], self.__arr[grandparent] = self.__arr[grandparent], self.__arr[i]
            
            #Continue to pushUp the grandparent 
            self.__pushUpMin(grandparent)

    def __pushUpMax(self, i):
        
        #Parent and grandParent in refrence to index
        parent = (i - 1) // 2
        grandparent = (parent - 1) // 2
        
        #If index has a grandparent, and current index key > grandparent key
        if grandparent >= 0 and self.__arr[i].key > self.__arr[grandparent].key:
            
            #Swap the keys
            self.__arr[i], self.__arr[grandparent] = self.__arr[grandparent], self.__arr[i]
            
            #Continue to pushUp the grandparent
            self.__pushUpMax(grandparent)
    
    
    def __pushDown(self, i):
        
        #if level is MIN level
        if self.__level(i)%2 == 0:
            
            #PushDown for min level on i
            self.__pushDownMin(i)
    
        #if level is MAX level
        else:
            
            #PushDown for max level on i
            self.__pushDownMax(i)
            
    #PushDown fuction for min level
    def __pushDownMin(self, i):
        
        #Index of left and right child
        leftChild = 2 * i + 1
        rightChild = leftChild + 1
        
        #Left child's left child
        left2Grand = 2 * leftChild + 1
        
        #Left child's right child
        leftRightGrand = left2Grand + 1
        
        #Right child's left child
        rightLeftGrand = 2 * rightChild + 1
        
        #Right child's right child
        right2Grand = rightLeftGrand + 1
        
        children = [leftChild, rightChild, left2Grand, leftRightGrand, \
                    rightLeftGrand, right2Grand]
        
        #Initialize smallest to index 'i'
        smallest = i
        
        
        #Loop through the list of children and grandchildren
        for c in children:
            
            #If child exists
            if c < self.__nElems and self.__arr[c]:
                
                #If the key of child/grandchild is less than key of smallest
                if self.__arr[c].key < self.__arr[smallest].key:
                   
                   #Update smallest's index to the child/granchild's index
                    smallest = c
            
        #If a child or grandChild is smallest (i isn't)
        if smallest != i:
            
            #if smallest is a grandchild (could also say if smallest in children[2:])
            if smallest != children[0] and smallest != children[1]:
            
                #swap i node with smallest node:
                self.__arr[i], self.__arr[smallest] = self.__arr[smallest], self.__arr[i]
            
                #parent index of smallest
                parentSmall = (smallest - 1) // 2
                
                #if smallest's key is greater than parents key
                if self.__arr[smallest].key > self.__arr[parentSmall].key:
                    
                    #swap smallest with smallest's parent
                    self.__arr[smallest], self.__arr[parentSmall] = self.__arr[parentSmall], self.__arr[smallest]
         
                #PushDown to fix the heap
                self.__pushDown(smallest)
           
            #If the smallest is a child (not a grandchild)
            else:   
                
                #Can swap directlty the smallest and i
                self.__arr[smallest], self.__arr[i] = self.__arr[i], self.__arr[smallest]
            
            
    def __pushDownMax(self, i):
        
        #Index of left and right child
        leftChild = 2 * i + 1
        rightChild = leftChild + 1
        
        #Left child's left child
        left2Grand = 2 * leftChild + 1
        
        #Left child's right child
        leftRightGrand = left2Grand + 1
        
        #Right child's left child
        rightLeftGrand = 2 * rightChild + 1
        
        #Right child's right child
        right2Grand = rightLeftGrand + 1
        
        #Create a list with each child/granchild's index
        children = [leftChild, rightChild, left2Grand, leftRightGrand, \
                    rightLeftGrand, right2Grand]
    
        #Initialize largest to index 'i'
        largest = i
        
        #Loop through the list of children and grandchildren
        for c in children:
            
            #If child exists
            if c < self.__nElems and self.__arr[c]:
                
                #If the key of child/grandchild is greater than key of largest
                if self.__arr[c].key > self.__arr[largest].key:
                   
                   #Update largest's index to the child/granchild's index
                    largest = c
            
        #If a child or grandChild is largest (i isn't)
        if largest != i:
            
            #if largest is a grandchild
            if largest != children[0] and largest != children[1]:
            
                #swap i node with largest node:
                self.__arr[i], self.__arr[largest] = self.__arr[largest], self.__arr[i]
            
                #parent index of largest
                parentLarge = (largest - 1) // 2
                
                #if largest's key is less than parents key
                
                if self.__arr[largest].key < self.__arr[parentLarge].key:
                    
                    #swap largest with largest's parent
                    self.__arr[largest], self.__arr[parentLarge] = self.__arr[parentLarge], self.__arr[largest]
            
        
                #PushDown to fix the heap
                self.__pushDown(largest)
            
            #If the smallest is a child (not a grandchild)
            else:
                #Can swap directlty the largest and i
                self.__arr[largest], self.__arr[i] = self.__arr[i], self.__arr[largest]
                    
        
    def findMin(self):
            
        #if heap is not empty
        if self.__nElems == 0:
            return None, None
        
        #return key/data pair of first node in array (the min)
        return self.__arr[0].key, self.__arr[0].data
        
        
    def __maxIndex(self):
        
        #If heap is empty
        if self.__nElems != 0: 
            
            
            #If theres only one child
            if self.__arr[1] and not self.__arr[2]:
            
                #maximum at index 1
                return 1
            
            #If there are two children
            if self.__arr[1] and self.__arr[2]:
                
                #If left child greater than right child
                if self.__arr[1].key > self.__arr[2].key:      
                
                    #maximum at index 1
                    return 1
                else:
                
                    #maximum at index 2               
                    return 2
                
        return 0
            
        
    def findMax(self):
        #If heap is empty
        if self.__nElems == 0:
            return None, None
        
        #Index for max node
        maximum = self.__maxIndex()
        
        #Return the key/data pair of maximum node
        return self.__arr[maximum].key, self.__arr[maximum].data
        
            
    def removeMin(self):
            
        #if heap is empty
        if self.__nElems == 0:
            return None, None
        
        #save root (min) to return later
        root = self.__arr[0]
            
        #Decrement number of elements by one
        self.__nElems -= 1
            
        #Place the last Node in the heap into the 
        #Root location, and push it down            
        self.__arr[0] = self.__arr[self.__nElems] 
            
        #Keep garbage collector happy
        self.__arr[self.__nElems] = None
        
        
        #Push down the node swapped to fix heap
        self.__pushDown(0)
        
        #Return key/data pair of min node removed
        return root.key, root.data  
        
    def removeMax(self):
            
        #if heap is empty
        if self.__nElems == 0:
            return None, None
            
        #Save max to return later
        maximum = self.__maxIndex()
        
        maxKey = self.__arr[maximum].key
        maxData = self.__arr[maximum].data
       
        #Decrement number of elements by one            
        self.__nElems -= 1
            
        #Place the last Node in the heap into the 
        #maximum location          
        self.__arr[maximum] = self.__arr[self.__nElems] 
        
        #keep garbage collector happy
        self.__arr[self.__nElems] = None  
       
        #pushDown the index of max node
        self.__pushDown(maximum)
    
        #Return the key/data pair of max node
        return maxKey, maxData 
    
    #checks if heap has properties of minMaxHeap
    def isMinMaxHeap(self):
        
        for i in range (self.__nElems):
            
            #if any node is None -- not a minMaxHeap
            if not self.__arr[i]: return False
            
            #Index of left and right child
            leftChild = 2 * i + 1
            rightChild = leftChild + 1
            
            #Left child's left child
            left2Grand = 2 * leftChild + 1
            
            #Left child's right child
            leftRightGrand = left2Grand + 1
            
            #Right child's left child
            rightLeftGrand = 2 * rightChild + 1
            
            #Right child's right child
            right2Grand = rightLeftGrand + 1
            
            #Create list of children/grandchildren based off the index
            children = [leftChild, rightChild, left2Grand, leftRightGrand, \
                        rightLeftGrand, right2Grand]
            
            #If MIN level            
            if self.__level(i) % 2 == 0:
                
                #If either the left or right child is smaller than i -- not a minMaxHeap
                if children[0] < self.__nElems and self.__arr[i].key > self.__arr[children[0]].key:
                    return False
                if children[1] < self.__nElems and self.__arr[i].key > self.__arr[children[1]].key:
                    return False
                
                #If any of grankids are smaller than i -- not a minMaxHeap
                if children[2] < self.__nElems and self.__arr[i].key > self.__arr[children[2]].key:
                    return False            
                if children[3] < self.__nElems and self.__arr[i].key > self.__arr[children[3]].key:
                    return False     
                if children[4] < self.__nElems and self.__arr[i].key > self.__arr[children[4]].key:
                    return False 
                if children[5] < self.__nElems and self.__arr[i].key > self.__arr[children[5]].key:
                    return False 
                
            #If MAX level
            else:
                #If either the left or right child is larger than i -- not a minMaxHeap
                if children[0] < self.__nElems and self.__arr[i].key < self.__arr[children[0]].key:
                    return False
                if children[1] < self.__nElems and self.__arr[i].key < self.__arr[children[1]].key:
                    return False
            
                #If any of grankids are larger than i -- not a minMaxHeap
                if children[2] < self.__nElems and self.__arr[i].key < self.__arr[children[2]].key:
                    return False            
                if children[3] < self.__nElems and self.__arr[i].key < self.__arr[children[3]].key:
                    return False        
                if children[4] < self.__nElems and self.__arr[i].key < self.__arr[children[4]].key:
                    return False 
                if children[5] < self.__nElems and self.__arr[i].key < self.__arr[children[5]].key:
                    return False   
        #if False hasn't been returned then passed all requirements, and is a minMaxHeap
        return True
                
            
def __main():
    
    h = MinMaxHeap(50)
    
    for i in range(50):
        h.insert(random.randint(0, 100), chr(ord('A') + 1 + i))
    
    print()
    print("Max of the heap")
    print(h.findMax())
    print("Min of heap")
    print(h.findMin())
    
    h.removeMax()
    print("Removed the max")
    print("The max", h.findMax())
    
    h.removeMin()
    print("Removed the min")
    print("The min", h.findMin())
    print("The max", h.findMax())
    print()
    
    
    
#if __name__ == '__main__':
#    __main()  
    
    
#Fake minMaxHeap class (stored in array):
class FakeMinMaxHeap(object):
    
    def __init__(self, size):
        
        self.__arr = []
        self.__nElems = 0
        self.__size = size
        
    def __str__(self):
        return str(self.__arr)
    
    def __len__(self):
        return self.__nElems
    
    def fakeInsert(self, k, d):
        
        #if the length of array less than size  (meaning there is room for insert)
        if len(self.__arr) < self.__size:
            
            #append the key and data to array
            self.__arr.append((k,d))
            
            #increment elements by one
            self.__nElems += 1
        
    def fakeFindMin(self):
        #check if empty
        if len(self.__arr) < 1:
            return None, None   
        
 
        #sort the array
        self.__arr.sort()
        
        #since the array is sorted, the smallest is the first index
        minimum = self.__arr[0]
        
        return minimum
    
    def fakeFindMax(self):
        #check if empty
        if len(self.__arr) < 1:
            return None, None   
        
        #sort the array
        self.__arr.sort()
        
        #since the array is sorted, the maximum is the last index
        maximum = self.__arr[-1]
        
        return maximum    

    def fakeRemoveMin(self):
        
        #check if empty
        if len(self.__arr) < 1:
            return None, None        
        
        #sort the array
        self.__arr.sort()
        
        #since the array is sorted, the smallest is the first index
        minimum = self.__arr[0]
        
        #remove the minimum 
        del self.__arr[0]
        
        #decrement amount of elements by one
        self.__nElems -= 1 
        
        return minimum
    
    def fakeRemoveMax(self):
        
        #check if empty
        if len(self.__arr) < 1:
            return None, None         
        
        #sort the array
        self.__arr.sort()
        
        #since the array is sorted, the maximum is the last index
        maximum = self.__arr[-1]        
        
        #remove the maximum 
        del self.__arr[-1] 
        
        #decrement amount of elements by one
        self.__nElems -= 1 
        
        return maximum        
    
    
#PYTESTS!!:

def test_insert():
    
    h = MinMaxHeap(100)
    f = FakeMinMaxHeap(100)
    
    for i in range(100):
        
        insert = random.randint(1,100)
        h.insert(insert, insert)
        f.fakeInsert(insert, insert)
        
        #Test that after inserts, the length of h and f will be the same
        assert len(h) == len(f)
        
        #Test that after inserts, h is a minMaxHeap
        assert h.isMinMaxHeap()
        
        
def test_findMin():
    
    h = MinMaxHeap(100)
    f = FakeMinMaxHeap(100)
    
    for i in range(100):
        
        insert = random.randint(1,100)
        h.insert(insert, insert)
        f.fakeInsert(insert, insert)
        
        #Test that after inserts, h and f have the same min
        assert h.findMin() == f.fakeFindMin()
        
def test_findMax():
    
    h = MinMaxHeap(200)
    f = FakeMinMaxHeap(200)
    
    for i in range(200):
        
        insert = random.randint(1,100)
        h.insert(insert, insert)
        f.fakeInsert(insert, insert)
        
        #Test that after inserts, h and f have the same max
        assert h.findMax() == f.fakeFindMax()   
        
def test_removeMin():
    
    h = MinMaxHeap(500)
    f = FakeMinMaxHeap(500)       
    
    for i in range(500):
        
        insert = random.randint(1,100)
        h.insert(insert, insert)
        f.fakeInsert(insert, insert)    
     
    for i in range(100):
        
        #Test that h and f are removing the same min
        assert h.removeMin() == f.fakeRemoveMin()
        
        #Test that after removing min, they have the same length
        assert len(h) == len(f)
        
        #Test that after removing the min, h is still a minMaxHeap
        assert h.isMinMaxHeap()
        
def test_removeMax():
    
    h = MinMaxHeap(1000)
    f = FakeMinMaxHeap(1000)       
    
    for i in range(1000):
        
        insert = random.randint(1,100)
        h.insert(insert, insert)
        f.fakeInsert(insert, insert)    
     
    for i in range(50):
        h.removeMax()
        f.fakeRemoveMax()
        
        #Test that after removing max, they have the same length
        assert len(h) == len(f)
        
        #Test that h and f are removing the same max
        assert h.removeMax() == f.fakeRemoveMax()
        
        #Test that after removing the max, h is still a minMaxHeap
        assert h.isMinMaxHeap()        
        
        
#Test an empty minMaxHeap   
def test_emptyMinMax():
    h = MinMaxHeap(100)
    
    assert h.isMinMaxHeap() == True
    
#Test a MinMaxHeap with only one node  
def test_oneNode():
    
    h = MinMaxHeap(100)  
    h.insert(random.randint(0, 100), 1)      
    assert h.isMinMaxHeap() == True
    
#Test an empty MinMaxHeap - find min/max
def test_emptyMinMaxfind():
    h = MinMaxHeap(100)
    
    assert h.findMin() == (None, None)
    assert h.findMax() == (None, None)
    
#Test minMaxHeap with small inserts
def test_smallInsert():
    h = MinMaxHeap(10)
    for i in range(10):
        h.insert(random.randint(1, 100), "c")
        
        assert h.isMinMaxHeap()
        
#Test small minMaxHeap with some remove min   
def test_smallRemoveMin():
    h = MinMaxHeap(10)
    for i in range(10):
        h.insert(random.randint(1, 100), "g")
    for i in range(10):
        h.removeMax()
        assert h.isMinMaxHeap()
        
#Test small minMaxHeap with some remove max          
def test_smallRemoveMax():
    h = MinMaxHeap(10)
    for i in range(10):
        h.insert(random.randint(1, 100), "b")
    for i in range(10):
        h.removeMin()
        assert h.isMinMaxHeap()   
        
#Test minMaxHeap with large inserts        
def test_largeInsert():
    h = MinMaxHeap(1000)
    for i in range(1000):
        h.insert(random.randint(1, 100), "z")
        assert h.isMinMaxHeap()

#Test large minMaxHeap with some remove min        
def test_largeRemoveMin():
    h = MinMaxHeap(1000)
    for i in range(1000):
        h.insert(random.randint(1, 100), "y")
    for i in range(1000):
        h.removeMin()
        assert h.isMinMaxHeap() 
        
#Test large minMaxHeap with some remove max        
def test_largeRemoveMax():
    h = MinMaxHeap(1000)
    for i in range(1000):
        h.insert(random.randint(1, 100), "x")
    for i in range(1000):
        h.removeMax()
        assert h.isMinMaxHeap()  
        
#Test minMaxHeap with only one node- - find/remove min        
def test_oneNodeMin():
    h = MinMaxHeap(10)
    h.insert(5,"b")
    assert h.findMin() == (5,"b")
    assert h.removeMin() == (5,"b")
    
#Test minMaxHeap with two nodes - find/remove max    
def test_TwoNodeMax():
    h = MinMaxHeap(10)
    h.insert(5,"b")
    h.insert(1,"a")
    assert h.findMax() == (5,"b")
    assert h.removeMax() == (5,"b")    
    
#Torture test #1
def test_torture1():
    h = MinMaxHeap(2000)
    f = FakeMinMaxHeap(2000)     
    
    for i in range(2000):
        do = random.randint(1,2)
        if do == 1:
            insert = (random.randint(1, 10000))
            h.insert(insert,insert)
            f.fakeInsert(insert,insert)
        else:
            h.removeMax()
            f.fakeRemoveMax()
            
            assert h.isMinMaxHeap()
            assert len(h) == len(f)
            
#Torture #2            
def test_torture2():
    h = MinMaxHeap(3000)
    f = FakeMinMaxHeap(3000) 
    
    for i in range(3000):
        do = random.randint(1,4)  
        
        if do == 1:
            insert = (random.randint(1, 10000))
            assert h.insert(insert,insert) == f.fakeInsert(insert,insert)
            assert len(h) == len(f)
            
        elif do == 2:
            
            assert h.removeMin() == f.fakeRemoveMin()
            assert len(h) == len(f)
            
        elif do == 3:
            
            assert h.removeMax() == f.fakeRemoveMax()
            assert len(h) == len(f)
        
        else:
            assert h.findMin() == f.fakeFindMin()            
            assert h.findMax() == f.fakeFindMax()            
            
        
pytest.main(["-v", "-s", "BIGHW.py"])
