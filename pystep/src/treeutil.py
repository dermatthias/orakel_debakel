"""
treeutil
========
Contains all sort of utilities to search and manipulate nested lists as trees.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

@author: by Mehdi Khoury
@version: 1.00
@copyright: (c) 2009 Mehdi Khoury under the mit license
http://www.opensource.org/licenses/mit-license.html
"""

from collections import deque
import psyco
import pickle
import copy
import array
import string
#Define exceptions

# Exceptions related to tree manipulation
class TreeUtilError(Exception): pass
class NestedHeadNode(TreeUtilError): pass
class NotAList(TreeUtilError): pass
class EmptyList(TreeUtilError): pass
class EmptyDict(TreeUtilError): pass

# Exceptions related to operators and calculation of fitness
class CalculationError(Exception): pass
class WrongValues(CalculationError): pass

psyco.profile()

def listGetRootNode(myTree):
    """
    Function:  listGetRootNode
    ==========================
    get the root node of a nested list
 
    @param myTree: the nested list representing a tree
    
    @return: the root node of a nested list
 
    """ 
    if type(myTree)is not list:
        raise NotAList, "Tree should be a (nested) list."
    if not myTree:
        raise EmptyList, "Tree should not be empty."
    if type(myTree[0])is list:
        raise NestedHeadNode, "Head node should not be a list."
        exit
    return myTree[0]
    

def BFS_Search(myTree):
    """
    
    Function:  BFS_Search
    =====================
    Traverse the nodes of a tree in breadth-first order.
 
    @param myTree: the nested list representing a tree
    
    @return: an generator for a list of nodes in Breath First Search order
 
    """ 

    queue = deque(myTree)
    while queue:       
        node = queue.popleft()
        if type(node) is list:
            yield node[0]
            for elem in node[1:]:
                queue.append(elem)
        else: yield node



def walk(seq):
    """
    Function:  walk
    ===============
    Walk over a sequence of items, printing each one in turn, and
    recursively walking over sub-sequences.
 
    @param seq: the nested list representing a tree
    
    """
    print seq
    if isinstance(seq, list):
        for item in seq:
            walk(item)


def getChildrenNodes2(lst,depth):
    """
    
    Function:  getChildrenNodes2
    ============================
    Get the children nodes in a nested list for a specific depth
 
    @param lst: the nested list representing a tree
    @param depth: the nested list representing a tree
    
    @return: a flat list of children nodes for a specific depth
 
    """ 
    result=[]
    if depth>0:
        for elem in getChildrenNodes2(lst,depth-1):
            if isinstance(elem, list):
                result.extend(elem[1:])
    else:
        result =lst
    return result







def PostOrder_Search(myTree):
    """
    Function:  PostOrder_Search
    ===========================
    Traverse the nodes of a tree by getting the leafs
    first and the branches after. Finishes with the root.
    e.g. [1,[2,[3,4,[5,6,7]]],[8,[9,10,11]],[12,13,14]]
    gives : [7, 6, 5, 4, 3, 2, 11, 10, 9, 8, 14, 13, 12, 1]
 
    @param myTree: the nested list representing a tree

    @return: a flat list of nodes in PostOrder Search
    
    """
    queue = deque(myTree)
    # place the root at the end of the traversal
    node = queue.popleft()
    queue.append(node)
    # add the rest in required order
    while queue:       
        node = queue.popleft()
        if type(node) is list:
            for elem in node:
                queue.appendleft(elem)
        else: yield node
        

# 
def DFS_Search(seq):
    """
    Function:  DFS_Search
    =====================
    a recursive generator that flatten a nested list
    gives a list of all nodes in the tree in Depth First Search order
 
    @param seq: the nested list representing a tree

    @return: a flat list of nodes in Depth First Search order
    
    """
    for x in seq:
        if type(x) is list:
            for y in DFS_Search(x):
                yield y
        else:
            yield x
    

def BranchNodes_Search(myTree):
    """
    Function:  BranchNodes_Search
    =============================
    a generator to iterate through branch nodes only in BFS order.
 
    @param myTree: the nested list representing a tree

    @return: a flat list of branch nodes nodes in BFS order.
    
    """  
    queue = deque(myTree)
    node = queue.popleft()
    yield node
    while queue:       
        node = queue.popleft()
        if type(node) is list:
            yield node[0]
            for elem in node:
                queue.append(elem)
        

def LeafNodes_Search(myTree):
    """
    Function:  LeafNodes_Search
    ===========================
    a generator to iterate through leaf nodes
    only in right-to-left BFS preorder.
 
    @param myTree: the nested list representing a tree

    @return: a flat list of leaf nodes nodes in BFS preorder.
    
    """ 
    queue = deque(myTree)
    # get rid of root node
    queue.popleft()
    while queue:       
        node = queue.popleft()
        if type(node) is list:
            for elem in node[1:]:
                queue.appendleft(elem)
        else: yield node



                


def isNested(myList):
    """
    Function:  isNested
    ===================
    Check if a list is nested
 
    @param myList: the nested list representing a tree

    @return: 1 if nested , 0 if not.
    
    """ 
    for elem in myList:
        if type(elem) is list:
            return 1
        else:
            return 0




            

def list_getTail(myList):
    """
    Function:  list_getTail
    =======================
    get the tail of a 'node'
    e.g. [1,2]->[2]
    e.g. [1,[2,4],5]->[2,5]
 
    @param myList: the nested list representing a tree

    @return: the tail of the list
    
    """ 
    value =[]
    if type(myList) is list:
        for elem in myList[1:]:
            if type(elem) is not list :
                value.append(elem) 
            else:
                value.append(elem[0])           
    return value


def getSubLists(myList):
    """
    Function:  getSubLists
    ======================
    get a list of all sub lists in a nested list 
 
    @param myList: the nested list representing a tree

    @return: a list of all sub lists in a nested list 
    
    """ 
    temp = myList
    result=[]
    while temp:
        elem = temp.pop(0)   
        if type(elem) is list:
                result.append(elem)
                temp.extend(elem)
    return result


def nestedListToDict(myList):
    """
    Function:  nestedListToDict
    ===========================
    get a dictionnary from a nested list
 
    @param myList: the nested list representing a tree

    @return: a dictionary 
    
    """ 
    if not myList:
        raise EmptyList, "Tree should not be empty."
        exit
    result={}
    result[myList[0]]=list_getTail(myList)
    temp = getSubLists(myList)
    for elem in temp: result[elem[0]]=list_getTail(elem)
    return result

 
def dictFindRootNode(myDict):
    """
    Function:  dictFindRootNode
    ===========================
    find the root node of a tree
    in a dictionary (assumption is that
    a root node is a key never found in
    any of all values)
 
    @param myDict: the dictionary representing a tree

    @return: a dictionary 
    
    """ 
    result=None
    temp=[]
    for elem in myDict.itervalues():
        temp.extend(elem)
    for key in myDict.iterkeys():
        if key not in temp:
            result = key
            return result
    return result


def dictGetRootList(myDict):
    """
    Function:  dictGetRootList
    ==========================
    get the list coresponding to the root node   
 
    @param myDict: the dictionary representing a tree

    @return: the list coresponding to the root node   
    
    """ 
    result=[]
    root = dictFindRootNode(myDict)
    atom = [root]
    atom.extend(myDict[root])
    result.extend(atom)
    return result



def dictToSubLists(myDict):
    """
    Function:  dictToSubLists
    =========================
    get a list version of the dictionary
 
    @param myDict: the dictionary representing a tree

    @return: the list corresponding to the dictionary
    
    """ 
    result =[]
    for k, v in myDict.iteritems():
        atom=[k]
        atom.extend(v)
        result.append(atom)
    return result


def nestedInsert(list1,list2):
    """
    Function:  nestedInsert
    =======================
    nest a list inside another one if the
    first one has elements which are head of
    lists or sub lists in list 2
 
    @param list1: flat list 1
    @param list1: flat list 2
    
    @return: resulting nested list
    
    """ 
    temp = list1
    for i in xrange(1,len(temp)):
        for elem in list2:
            if temp[i]== elem[0]:
                temp[i]=nestedInsert(elem,list2)
    return temp
    

def dictToNestedList(myDict):
    """
    Function:  dictToNestedList
    ===========================
    finally, transform the dictionary
    into a nested list
 
    @param myDict: the dictionary representing a tree

    @return: the nested list corresponding to the dictionary
    
    """ 
    if not myDict:
        raise EmptyDict, "Dictionary should not be empty."
        exit
    root = dictGetRootList(myDict)
    sublists = dictToSubLists(myDict)
    sublists.remove(root)
    return nestedInsert(root,sublists)

    
