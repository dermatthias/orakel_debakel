"""
buildtree
=========
Contains strongly-typed versions of Koza-based tree building methods.
The buildTree() method is the constructor for a tree and contains the
relevant functions.

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
@contact: mehdi.khoury at gmail.com



"""
import random
import settings
from collections import deque
import psyco
import timeit


# Exceptions related to tree building
class TreeBuildingError(Exception): pass
class NoTerminalSet(TreeBuildingError): pass
class NoFunctionSet(TreeBuildingError): pass
class EmptyOrderedSet(TreeBuildingError): pass


# class that contains methods to build a random tree

psyco.profile()



class buildTree():
    """
    implement tree building methods described in Koza I/II.
    The buildTree() method is the constructor for a tree and contains the
    relevant functions.
    
    """
        
    def setRandomLeafChild(self,parent,child_nb):
        """
        Function:  setRandomLeafChild
        =============================
        
        Set the a random leaf node
        
        @param parent: the parent node (generally a root node) e.g. (0,2,'root')
        @param child_nb: the child node position (0 for first, 1 for second and so on...)
        @return: the random leaf child node e.g. (3,0,'x')
        """ 
        random_leaf_child=[]
        try:
            random_leaf_child=random.choice(settings.treeRules[parent[2]][child_nb][1])
        except:
            raise NoTerminalSet, "Empty terminal set! This parent has no leaf node to choose from!"
            exit
        return random_leaf_child



    def setRandomBranchChild(self,parent,child_nb):
        """
        Function:  setRandomBranchChild
        ===============================
        
        Set the a random branch node
 
        @param parent: the parent node (generally a root node) e.g. (0,2,'root')
        @param child_nb: the child node position (0 for first, 1 for second and so on...)
        @return: the random branch child node e.g. (1,2,'*')
        """ 
        random_branch_child=[]
        try:
            random_branch_child = random.choice(settings.treeRules[parent[2]][child_nb][0])
        except:
            raise NoFunctionSet, "Empty function set! This parent has no branch node to choose from!"
            exit
        return random_branch_child



    def setRandomBranchWithTerminalSet(self,parent,child_nb):
        """
        Function:  setRandomBranchWithTerminalSet
        =========================================
        
        Set an random branch child node which has terminals
 
        @param parent: the parent node (generally a root node) e.g. (0,2,'root')
        @param child_nb: the child node position (0 for first, 1 for second and so on...)
        @return: the branch child node e.g. (1,2,'*')
        """ 
        constraints = settings.treeRules
        if not constraints[parent[2]][child_nb][0]:
            raise NoFunctionSet, "Empty function set! Root node has no function to choose from!"
            exit
        initial = constraints[parent[2]][child_nb][0]
        try:
            #filter functions (take aways those who don't have a terminal set)
            initial = [ x for x in initial if constraints[x[2]][child_nb][1] ]
            return random.choice(initial) 
        except:
            # if there are no functions with terminal set, use the other ones
            return random.choice(settings.treeRules[parent[2]][child_nb][0])


    def setRandomBranchWithFunctionSet(self,parent,child_nb):
        """
        Function:  setRandomBranchWithTerminalSet
        =========================================
        
        Set an random branch child node which has terminals
 
        @param parent: the parent node (generally a root node) e.g. (0,2,'root')
        @param child_nb: the child node position (0 for first, 1 for second and so on...)
        @return: the branch child node e.g. (1,2,'*')
        """ 
        constraints = settings.treeRules
        if not constraints[parent[2]][child_nb][0]:
            raise NoFunctionSet, "Empty function set! Root node has no function to choose from!"
            exit
        initial = constraints[parent[2]][child_nb][0]
        try:
            #filter functions (take aways those who don't have a function set)
            initial = [ x for x in initial if constraints[x[2]][child_nb][0] ]
            return random.choice(initial) 
        except:
            # if there are no functions with function set, use the other ones
            return random.choice(settings.treeRules[parent[2]][child_nb][1])
  

# The FULL method (see KOZA GP Vol I and II)
    def AddFullNode(self,parent,depth,maxdepth):
        """
        Function:  AddFullNode2
        =======================
        Build a tree using Koza Full Algorithm
 
        @param parent: the parent node (generally a root node) e.g. (0,2,'root')
        @param depth: starting depth (0 when building a tree from scratch)
        @param maxdepth: max tree depth (in principle unlimited - careful with memory limitation through :))
        @return: returns a tree built using Koza Full
        """ 
        result = [parent]
        myDepth = depth
        # stopping condition - when maximum depth is reached
        if myDepth == maxdepth:
            return parent
        # add branch upon branch until before maximum depth,
        # then, build leafs
        else:
                # if the parent node is a function, 
            
                result = [parent]
                # get the number of children of this function (arity)
                nbChildren = parent[1]
                listdepth =[]
                # for every child
                for i in xrange(nbChildren):
                    # add a new depth counter
                    listdepth.append(myDepth)
                    # if near max depth add a leaf
                    if maxdepth-listdepth[i]==1:
#                        try:
                            result.append(self.setRandomLeafChild(parent,i))
#                        except:
#                            try:
#                                result.append(self.AddFullNode(self.setRandomBranchWithTerminalSet(parent,i),listdepth[i]+1,maxdepth))
#                                listdepth[i] = listdepth[i]+1
#                            except:
#                                result.append(self.AddFullNode(self.setRandomBranchChild(parent,i),listdepth[i]+1,maxdepth))
#                                listdepth[i] = listdepth[i]+1
                    # if 2 nodes from max depth, only use functions which have a terminal set
                    elif maxdepth-listdepth[i]==2:
                        try:
                            result.append(self.AddFullNode(self.setRandomBranchWithTerminalSet(parent,i),listdepth[i]+1,maxdepth))
                            listdepth[i] = listdepth[i]+1
                        except:
                            try:
                                result.append(self.AddFullNode(self.setRandomBranchChild(parent,i),listdepth[i]+1,maxdepth))
                                listdepth[i] = listdepth[i]+1
                            except:
                                #print parent
                                #print i
                                result.append(self.setRandomLeafChild(parent,i))
                    # else add a branch
                    else:
                        try:
                            result.append(self.AddFullNode(self.setRandomBranchWithFunctionSet(parent,i),listdepth[i]+1,maxdepth))
                            listdepth[i] = listdepth[i]+1
                        except:
                            try:
                                result.append(self.AddFullNode(self.setRandomBranchChild(parent,i),listdepth[i]+1,maxdepth))
                                listdepth[i] = listdepth[i]+1
                            except:
                                result.append(self.setRandomLeafChild(parent,i))
           
        return result


# The HALF method (see KOZA GP Vol I and II)
    def AddGrowNodeMin(self,parent,depth,mindepth,maxdepth):
        """
        Function:  AddFullNode2
        =======================
        Build a tree using Koza Half Algorithm

        @param parent: the parent node (generally a root node) e.g. (0,2,'root')
        @param depth: starting depth (0 when building a tree from scratch)
        @param mindepth: min tree depth 
        @param maxdepth: max tree depth (in principle unlimited - careful with memory limitation through :))
        @return: returns a tree built using Koza Full
        """ 
        result = [parent]
        myDepth = depth
        # stopping condition - when maximum depth is reached
        if myDepth == maxdepth:
            return parent
        # add branch upon branch until before maximum depth,
        # then, build leafs
        else:
                # if the parent node is a function, 
            
                result = [parent]
                # get the number of children of this function (arity)
                nbChildren = parent[1]
                listdepth =[]
                # for every child
                for i in xrange(nbChildren):
                    # add a new depth counter
                    listdepth.append(myDepth)
                    # if near max depth add a leaf
                    if maxdepth-listdepth[i]==1:
#                        try:
                            result.append(self.setRandomLeafChild(parent,i))
#                        except:
#                            try:
#                                result.append(self.AddFullNode(self.setRandomBranchWithTerminalSet(parent,i),listdepth[i]+1,maxdepth))
#                                listdepth[i] = listdepth[i]+1
#                            except:
#                                result.append(self.AddFullNode(self.setRandomBranchChild(parent,i),listdepth[i]+1,maxdepth))
#                                listdepth[i] = listdepth[i]+1
                    # if 2 nodes from max depth, only use functions which have a terminal set
                    elif maxdepth-listdepth[i]==2 or depth-mindepth-1<=-1:
                        try:
                            result.append(self.AddGrowNodeMin(self.setRandomBranchWithTerminalSet(parent,i),listdepth[i]+1,mindepth,maxdepth))
                            #listdepth[i] = listdepth[i]+1
                        except:
                            try:
                                result.append(self.AddGrowNodeMin(self.setRandomBranchChild(parent,i),listdepth[i]+1,mindepth,maxdepth))
                                listdepth[i] = listdepth[i]+1
                            except:
                                result.append(self.setRandomLeafChild(parent,i))
                    # else in normal cases, add randomly a branch or a leave
                    else:
                        chosenType = random.randint(0, 1)
                        if chosenType:
                            result.append(self.AddGrowNodeMin(self.setRandomBranchChild(parent,i),listdepth[i]+1,mindepth,maxdepth))
                            listdepth[i] = listdepth[i]+1
                        else:
                            result.append(self.setRandomLeafChild(parent,i))
           
        return result
    


    def AddHalfNode(self,parent,depth,mindepth,maxdepth):
        """
        Function:  AddHalfNode
        ======================
        
        Build a tree using Koza Ramped Half-n-Half
 
        @param parent: the parent node (generally a root node) e.g. (0,2,'root')
        @param depth: starting depth (0 when building a tree from scratch)
        @param mindepth: min tree depth (only works with 2 in the present version)
        @param maxdepth: max tree depth (in principle unlimited - careful with memory limitation through :))
        @return: returns a tree built using Koza Ramped Half-n-Half
        """ 
        #randomDepth = random.randint(mindepth+1, maxdepth)
        randomDepth = random.randint(mindepth, maxdepth)
        prob = random.random()< 0.5
        if prob:
            return self.AddFullNode(parent,depth,randomDepth)
        else:
            return self.AddGrowNodeMin(parent,depth,mindepth,randomDepth)

if __name__ == '__main__':
    #print buildTree().setRandomLeafChild((1,2,'*'),1)
    #print buildTree().setRandomBranchChild((0,2,'root'),0)
    #print buildTree().setRandomBranchWithTerminalSet((0,2,'root'),0)
    for i in xrange(10000):
        #a=buildTree().AddFullNode((0,3,'root'),0,8)  
        #print a
        
        #b=buildTree().AddGrowNodeMin((1, 2, 'or'),1,2,10)  
        #print b
        
        c=buildTree().AddHalfNode((0,2,'root'),0,2,10)  
    
        print c


    #t = timeit.Timer("buildtree.buildTree().AddFullNode((0,1,'root'),0,8)","import buildtree")
    #print t.repeat(1,10000)

