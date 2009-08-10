"""
mutation
========
Contains strongly-typed version of the Koza-based mutation operator.

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

import psyco
import random
import settings
import crossutil
import treeutil
import buildtree
import copy
#from types import *
import evalfitness
import sys
from collections import deque
import mutation

psyco.profile()



def Mutate(maxdepth,parent,p1_map,p1_depth):
    """
    Function:  Mutate
    =================
    create a mutated individual from a parent tree using Koza styled mutation
 
    @param maxdepth: maximum depth of the mutated offspring
    @param parent: parent tree e.g. a=buildtree.buildTree().AddHalfNode((0,2,'root'),0,2,7)  
    @param p1_map: parent tree index mapping e.g a_map=crossutil.get_indices_mapping_from_tree(a)
    @param p1_depth: parent tree depth e.g. a_depth=crossutil.get_depth_from_indices_mapping(a_map)
    
    @return: a tuple containing two elements. 
        - The first one is a boolean indicating if the mutated tree is identical to the parent
            (if identical, returns True)
        - The second one is the mutated tree
 
    """ 
    # get a random depth for parent1
    if p1_depth>=1:
        p1_mutation_depth=1
    else:
        p1_mutation_depth=random.randint(1, p1_depth-1)
    # get a random depth in p2 such that the resulting
    # offspring lenght is <= offspring maxdepth
    mychoice1=crossutil.UnpackIndicesFromList(\
            crossutil.GetPackedListIndicesAtDepth(p1_map,p1_mutation_depth))
    p1_point=random.choice(mychoice1)
    parent1_clone=copy.deepcopy(parent)
    exec("fragment_p1=parent1_clone%s"%crossutil.IndexLstToIndexStr2(p1_point))
    # first we need to extract the top node of each subtree
    if isinstance(fragment_p1, list):
        firstnode_p1= fragment_p1[0]
    if isinstance(fragment_p1, tuple):
        firstnode_p1=fragment_p1
    # get the parent node of each sub tree (context of each parent)
    subtree1_parent_s = crossutil.IndexLstToIndexStr2(p1_point)
    # if the first node is not an ADF, the string version of the 
    # index of the subtree is just the index of upper node in the tree
    if firstnode_p1[0]!=2:
        subtree1_parent_s= subtree1_parent_s[:-3]
    # get the subtree using the index we just obtained
    exec("subtree1_parent=parent1_clone%s"%subtree1_parent_s)
    # get the flat list of permitted nodes for the parent tree
    # for that first get the list of permitted branch nodes...
    context_p1= settings.treeRules[subtree1_parent[0][2]]
    context=copy.deepcopy(context_p1)
    # and extend to it the list of permitted leaf nodes
    context[p1_point[-1]-1][0].extend( context[p1_point[-1]-1][1])
    if len(context[p1_point[-1]-1][0])>1 and firstnode_p1[0]==2:
            context[p1_point[-1]-1][0].remove(firstnode_p1)
    # get the context from grammar rules for each parent
    
    # min_mutation_depth for the subtree has to be extracted by looking when is the next child with a terminal
    min_mutation_depth=1
    #print context[p1_point[-1]-1][0]
    flag=random.choice(context[p1_point[-1]-1][0])
    if not settings.treeRules[subtree1_parent[0][2]][p1_point[-1]-1][1]:
        min_mutation_depth=2
    #print flag
        
    mutant_fragment=buildtree.buildTree().AddHalfNode(\
            random.choice(context[p1_point[-1]-1][0]) ,p1_mutation_depth,p1_mutation_depth+min_mutation_depth,maxdepth)
    # make sure that the mutant fragment is different from the previous fragment
    if len(mutant_fragment)==1 and isinstance(mutant_fragment[0], tuple):
        mutant_fragment=mutant_fragment[0]
    exec("parent1_clone%s=mutant_fragment"%crossutil.IndexLstToIndexStr2(p1_point))
    identical=False
    if mutant_fragment==fragment_p1:
        identical =True
    # no branch nor leaf compatible from fragment to parent nodes
    return (identical, parent1_clone)
    
    
if __name__ == '__main__':
    for i in xrange(10000):
        a=buildtree.buildTree().AddHalfNode((0,2,'root'),0,2,7)  
        a_map=crossutil.GetIndicesMappingFromTree(a)
        a_depth=crossutil.GetDepthFromIndicesMapping(a_map)
        print a
        m=mutation.Mutate(10,a,a_map,a_depth)
        print m
        m_map=crossutil.GetIndicesMappingFromTree(m[1])
        m_depth=crossutil.GetDepthFromIndicesMapping(m_map)
        print m_depth
        print evalfitness.FinalFitness_tutorial8(evalfitness.EvalTreeForOneListInputSet_tutorial8(m[1]))