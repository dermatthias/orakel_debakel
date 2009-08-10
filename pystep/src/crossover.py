"""
crossover
=========
All crossover related operations. In the context of strongly-typed Genetic
Programming, this operator is heavily modified to produce offsprings that 
are compliant with multiple rules and constraints set by the user.
In the present version, only a strongly-typed version of Koza 1 point 
crossover is supported. 

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
import crossutil
import treeutil
import buildtree
from copy import deepcopy
#from types import *
import evalfitness
import sys
from collections import deque
import timeit
import settings

psyco.profile()

    
    

def Koza1PointCrossover(maxdepth,p1,p2,p1_mp,p2_mp,p1_depth,p2_depth):
    """
    Function:  Koza1PointCrossover
    ==============================
    create 2 offsprings from 2 parents using a modified version of Koza-1-point
    crossover. This version try to produce offsprings compliant with the 
    constraints and rules used to build an individual. If it does not manage,
    it produce a report showing if the offsprings produced are compatible.
 
    @param maxdepth: maximum depth of the mutated offspring
    @param p1: parent tree 1  e.g. a=buildtree.buildTree().AddHalfNode((0,2,'root'),0,2,7)  
    @param p2: parent tree 2  e.g. a=buildtree.buildTree().AddHalfNode((0,2,'root'),0,2,7)  
    @param p1_mp: parent tree index mapping e.g a_map=crossutil.get_indices_mapping_from_tree(a)
    @param p2_mp: parent tree index mapping e.g a_map=crossutil.get_indices_mapping_from_tree(a)
    @param p1_depth: parent tree depth e.g. a_depth=crossutil.get_depth_from_indices_mapping(a_map) 
    @param p2_depth: parent tree depth e.g. a_depth=crossutil.get_depth_from_indices_mapping(a_map)
    
    @return: a tuple containing 3 elements
        - The first one is a list of 1 and 0 indicating if the first and second offspring are rule 
        compliant. 
        [1,1,1,1] frag2_leaf_compatible_p1 and frag1_leaf_compatible_p2 and frag2_branch_compatible_p1 and frag1_branch_compatible_p2
        [1,0,1,1] frag2_leaf_compatible_p1 and not frag1_leaf_compatible_p2 and frag2_branch_compatible_p1 and frag1_branch_compatible_p2
        [1,1,0,1] frag2_leaf_compatible_p1 and frag1_leaf_compatible_p2 and not frag2_branch_compatible_p1 and frag1_branch_compatible_p2
        and so on... This information can be use to decide if we want to introduce non-compliant offsprings into the population.
        - The second one is the first offspring
        - The third one is the second offspring
 
    """ 
    p1_map=deepcopy(p1_mp)
    p2_map=deepcopy(p2_mp)
    # get a random depth for parent1
    p1_cross_depth=random.randint(1, p1_depth-1)
    # get a random depth in p2 such that the resulting
    # offspring lenght is <= offspring maxdepth
    fragment_p1_depth= p1_depth-1-p1_cross_depth
    if p2_depth > (maxdepth-fragment_p1_depth):
            if maxdepth-fragment_p1_depth>0:
                p2_cross_depth=random.randint(1,(maxdepth-fragment_p1_depth))
            else:
                p2_cross_depth=1
    else:    
        p2_cross_depth=random.randint(1, p2_depth-1)
    mychoice1=crossutil.UnpackIndicesFromList(\
            crossutil.GetPackedListIndicesAtDepth(p1_map,p1_cross_depth))
    p1_point=random.choice(mychoice1)
    #print crossutil.index_lst_to_index_str2(p1_point)
    mychoice2=crossutil.UnpackIndicesFromList(\
            crossutil.GetPackedListIndicesAtDepth(p2_map,p2_cross_depth))
    p2_point=random.choice(mychoice2)
    #print crossutil.index_lst_to_index_str2(p2_point)
    parent1_clone=deepcopy(p1)
    parent2_clone=deepcopy(p2)
    exec("fragment_p1=parent1_clone%s"%crossutil.IndexLstToIndexStr2(p1_point))
    exec("fragment_p2=parent2_clone%s"%crossutil.IndexLstToIndexStr2(p2_point))
    # Having selected a sub tree, we need to check structural integrity and compatibility
    #print fragment_p1
    #print fragment_p2
    # first we want to know if the sub-tree is located under a specific ADF defining branch
    
    # first we need to extract the top node of each subtree
    if isinstance(fragment_p1, list):
        firstnode_p1= fragment_p1[0]
        #print list(treeutil.BFS_Search(fragment_p1))
    if isinstance(fragment_p1, tuple):
        firstnode_p1=fragment_p1
    if isinstance(fragment_p2, list):
        firstnode_p2=fragment_p2[0]
        #print list(treeutil.BFS_Search(fragment_p2))
    if isinstance(fragment_p2, tuple):
        firstnode_p2=fragment_p2
    
    # get the parent node of each sub tree (context of each parent)
    subtree1_parent_s = crossutil.IndexLstToIndexStr2(p1_point)
    if firstnode_p1[0]!=2:
        subtree1_parent_s= subtree1_parent_s[:-3]
    
    subtree2_parent_s = crossutil.IndexLstToIndexStr2(p2_point)
    if firstnode_p2[0]!=2:
        subtree2_parent_s= subtree2_parent_s[:-3]
    
    exec("subtree1_parent=parent1_clone%s"%subtree1_parent_s)
    #print subtree1_parent[0]
    exec("subtree2_parent=parent2_clone%s"%subtree2_parent_s)
    #print subtree2_parent[0]
    
    # get the context from grammar rules for each parent
    # print buildtree.buildTree().treeSets
    context_p1= settings.treeRules[subtree1_parent[0][2]]
    context_p2= settings.treeRules[subtree2_parent[0][2]]
    
    # check that the subtree are compatible with their new parents
    frag1_leaf_compatible_p2=True
    frag2_leaf_compatible_p1=True
    frag1_branch_compatible_p2=True
    frag2_branch_compatible_p1=True
    # extract all terminal nodes of the fragment subtrees in flat lists
    frag1, frag2 =[], []
    #print fragment_p1
    #print list(treeutil.LeafNodes_Search(fragment_p1))
    if list(treeutil.LeafNodes_Search(fragment_p1)):
        if isinstance(list(treeutil.LeafNodes_Search(fragment_p1))[0], tuple):
            frag1=list(treeutil.LeafNodes_Search(fragment_p1))
        else:
            frag1=[tuple(fragment_p1)]
    else:
        frag1=fragment_p1
    if list(treeutil.LeafNodes_Search(fragment_p2)):    
        if isinstance(list(treeutil.LeafNodes_Search(fragment_p2))[0], tuple):
            frag2=list(treeutil.LeafNodes_Search(fragment_p2))
        else:
            frag2=[tuple(fragment_p2)]
    else:
        frag2=fragment_p2
    #print frag1
    #print context_p2[1]
    #print frag2
    #print context_p1[1]
    # check if the fragments have terminal nodes incompatible with parent context
    for elem_frag2 in frag2:
            if elem_frag2 not in context_p1[p1_point[-1]-1][1]:
                frag2_leaf_compatible_p1=False
                break
    for elem_frag1 in frag1:
            if elem_frag1 not in context_p2[p2_point[-1]-1][1]:
                frag1_leaf_compatible_p2=False
                break
    # extract all branch nodes of the fragment subtrees in flat lists
    frag1, frag2 =[], []
    if isinstance(list(treeutil.BranchNodes_Search(fragment_p1))[0], tuple):
        frag1=list(treeutil.BranchNodes_Search(fragment_p1))
    else:
        frag1=[tuple(fragment_p1)]
    if isinstance(list(treeutil.BranchNodes_Search(fragment_p2))[0], tuple):
        frag2=list(treeutil.BranchNodes_Search(fragment_p2))
    else:
        frag2=[tuple(fragment_p2)]
    # if no branch node in subtree, then branch is all compatible...
    for elem_frag1 in frag1:
        if len(frag1)==1 and frag1[0][0]!=1:
            frag1_branch_compatible_p2=True
        elif elem_frag1 not in context_p2[0]:
            frag1_branch_compatible_p2=False
            break
        else:
            frag1_branch_compatible_p2=True  
    for elem_frag2 in frag2:  
        if len(frag2)==1 and frag2[0][0]!=1:
            frag2_branch_compatible_p1=True
        elif elem_frag2 not in context_p1[0]:
            frag2_branch_compatible_p1=False
            break
        else:
            frag2_branch_compatible_p1=True
            
    #print frag1
    #print context_p2[0]
    #print frag2
    #print context_p1[0]
    
    # if the automatic replacement of compatible branch operators is authorized
    # do it to make the offspring compatible wit hthe grammar rules...
    copy_fragment_p1 = deepcopy(fragment_p1)
    copy_fragment_p2 = deepcopy(fragment_p2)
    if  frag1_branch_compatible_p2==False \
    and frag1_leaf_compatible_p2==True \
    and settings.Strongly_Typed_Crossover_degree>=1:
        #print 'replace branches fragment1' 
        
        frag1=list(set(frag1))
        temp1=str(copy_fragment_p1)
        #print temp1
        for elem_frag1 in frag1:
            for elem_p2 in context_p2[p2_point[-1]-1][0]:
                for elem_crossover_mapping in settings.crossover_mapping:
                    if elem_crossover_mapping[1]==str(elem_p2[2]) and elem_crossover_mapping[0]==str(elem_frag1[2]):
                        temp1=temp1.replace(elem_crossover_mapping[0], elem_crossover_mapping[1])       
        #print temp
        exec("copy_fragment_p1 =%s"%temp1)
        #print copy_fragment_p1
           
    if  frag2_branch_compatible_p1==False \
    and frag2_leaf_compatible_p1==True \
    and settings.Strongly_Typed_Crossover_degree>=1:
        #print 'replace branches fragment2' 
        
        frag2=list(set(frag2))
        temp2=str(copy_fragment_p2)
        #print temp2
        for elem_frag2 in frag2:
            for elem_p1 in context_p1[p1_point[-1]-1][0]:
                for elem_crossover_mapping in settings.crossover_mapping:
                    if elem_crossover_mapping[1]==str(elem_p1[2]) and elem_crossover_mapping[0]==str(elem_frag2[2]):
                        temp2=temp2.replace(elem_crossover_mapping[0], elem_crossover_mapping[1])     
        #print temp
        exec("copy_fragment_p2 =%s"%temp2)
        #print copy_fragment_p2
    
    frag1_leaf_compatible_p2=True
    frag2_leaf_compatible_p1=True
    frag1_branch_compatible_p2=True
    frag2_branch_compatible_p1=True
    # extract all terminal nodes of the fragment subtrees in flat lists
    frag1, frag2 =[], []
    if list(treeutil.LeafNodes_Search(fragment_p1)):
        if isinstance(list(treeutil.LeafNodes_Search(fragment_p1))[0], tuple):
            frag1=list(treeutil.LeafNodes_Search(fragment_p1))
        else:
            frag1=[tuple(fragment_p1)]
    else:
        frag1=fragment_p1
    if list(treeutil.LeafNodes_Search(fragment_p2)):    
        if isinstance(list(treeutil.LeafNodes_Search(fragment_p2))[0], tuple):
            frag2=list(treeutil.LeafNodes_Search(fragment_p2))
        else:
            frag2=[tuple(fragment_p2)]
    else:
        frag2=fragment_p2
    #print frag1
    #print context_p2[1]
    #print frag2
    #print context_p1[1]
    # check if the fragments have terminal nodes incompatible with parent context
    for elem_frag2 in frag2:
            if elem_frag2 not in context_p1[p1_point[-1]-1][1]:
                frag2_leaf_compatible_p1=False
                break
    for elem_frag1 in frag1:
            if elem_frag1 not in context_p2[p2_point[-1]-1][1]:
                frag1_leaf_compatible_p2=False
                break
            
    #print frag2_leaf_compatible_p1
    #print frag1_leaf_compatible_p2
    #print frag1_branch_compatible_p2
    #print frag2_branch_compatible_p1
    
    # return the offspring resulting from the crossover with indicators of 
    # structural compliance of the offspring.
    # [1,1,1,1] frag2_leaf_compatible_p1 and frag1_leaf_compatible_p2 and frag2_branch_compatible_p1 and frag1_branch_compatible_p2
    # [1,0,1,1] frag2_leaf_compatible_p1 and not frag1_leaf_compatible_p2 and frag2_branch_compatible_p1 and frag1_branch_compatible_p2
    # [1,1,0,1] frag2_leaf_compatible_p1 and frag1_leaf_compatible_p2 and not frag2_branch_compatible_p1 and frag1_branch_compatible_p2
    # and so on...
    # This information can be use to decide if we want to introduce non-compliant offsprings into the population.
    
    if frag2_leaf_compatible_p1 and frag1_leaf_compatible_p2 and frag2_branch_compatible_p1 and frag1_branch_compatible_p2:
        exec("parent1_clone%s=copy_fragment_p2"%crossutil.IndexLstToIndexStr2(p1_point))
        exec("parent2_clone%s=copy_fragment_p1"%crossutil.IndexLstToIndexStr2(p2_point))
        return ([1,1,1,1],parent1_clone,parent2_clone)
    elif frag2_leaf_compatible_p1 and not frag1_leaf_compatible_p2 and frag2_branch_compatible_p1 and frag1_branch_compatible_p2:
        #print "One of the Leafs from fragment1 in the offspring is not compatible with context from parent2 "
        exec("parent1_clone%s=fragment_p2"%crossutil.IndexLstToIndexStr2(p1_point))
        exec("parent2_clone%s=fragment_p1"%crossutil.IndexLstToIndexStr2(p2_point))
        return ([1,0,1,1],parent1_clone,parent2_clone)
    elif not frag2_leaf_compatible_p1 and frag1_leaf_compatible_p2 and frag2_branch_compatible_p1 and frag1_branch_compatible_p2:
        #print "One of the Leafs from fragment2 in the offspring is not compatible with context from parent1 "
        exec("parent1_clone%s=fragment_p2"%crossutil.IndexLstToIndexStr2(p1_point))
        exec("parent2_clone%s=fragment_p1"%crossutil.IndexLstToIndexStr2(p2_point))
        return ([0,1,1,1],parent1_clone,parent2_clone)
    elif not frag2_leaf_compatible_p1 and not frag1_leaf_compatible_p2 and frag2_branch_compatible_p1 and frag1_branch_compatible_p2:
        #print "Leafs from fragment2 and fragment1 in the offsprings are not compatible with context from parent1 and parent2 "
        exec("parent1_clone%s=fragment_p2"%crossutil.IndexLstToIndexStr2(p1_point))
        exec("parent2_clone%s=fragment_p1"%crossutil.IndexLstToIndexStr2(p2_point))
        return ([0,0,1,1],parent1_clone,parent2_clone)
    elif frag2_leaf_compatible_p1 and frag1_leaf_compatible_p2 and not frag2_branch_compatible_p1 and frag1_branch_compatible_p2:
        #print "One of the Branches from fragment2 in the offspring is not compatible with context from parent1 "
        exec("parent1_clone%s=fragment_p2"%crossutil.IndexLstToIndexStr2(p1_point))
        exec("parent2_clone%s=fragment_p1"%crossutil.IndexLstToIndexStr2(p2_point))
        return ([1,1,0,1],parent1_clone,parent2_clone)
    elif frag2_leaf_compatible_p1 and frag1_leaf_compatible_p2 and frag2_branch_compatible_p1 and not frag1_branch_compatible_p2:
        #print "One of the Branches from fragment1 in the offspring is not compatible with context from parent2 "
        exec("parent1_clone%s=fragment_p2"%crossutil.IndexLstToIndexStr2(p1_point))
        exec("parent2_clone%s=fragment_p1"%crossutil.IndexLstToIndexStr2(p2_point))
        return ([1,1,1,0],parent1_clone,parent2_clone)
    elif frag2_leaf_compatible_p1 and frag1_leaf_compatible_p2 and not frag2_branch_compatible_p1 and not frag1_branch_compatible_p2 :
        #print "Branches from fragment1 and Fragment2 in the offsprings are not compatible with context from parent2 and parent1 "
        exec("parent1_clone%s=fragment_p2"%crossutil.IndexLstToIndexStr2(p1_point))
        exec("parent2_clone%s=fragment_p1"%crossutil.IndexLstToIndexStr2(p2_point))
        return ([1,1,0,0],parent1_clone,parent2_clone)
    elif frag2_leaf_compatible_p1 and not frag1_leaf_compatible_p2 and not frag2_branch_compatible_p1 and not frag1_branch_compatible_p2 :
        #print "Branches from fragment1 and Fragment2 in the offsprings are not compatible with context from parent2 and parent1 "
        exec("parent1_clone%s=fragment_p2"%crossutil.IndexLstToIndexStr2(p1_point))
        exec("parent2_clone%s=fragment_p1"%crossutil.IndexLstToIndexStr2(p2_point))
        return ([1,0,0,0],parent1_clone,parent2_clone)
    elif not frag2_leaf_compatible_p1 and frag1_leaf_compatible_p2 and not frag2_branch_compatible_p1 and not frag1_branch_compatible_p2 :
        #print "Branches from fragment1 and Fragment2 in the offsprings are not compatible with context from parent2 and parent1 "
        exec("parent1_clone%s=fragment_p2"%crossutil.IndexLstToIndexStr2(p1_point))
        exec("parent2_clone%s=fragment_p1"%crossutil.IndexLstToIndexStr2(p2_point))
        return ([0,1,0,0],parent1_clone,parent2_clone)
    else:
        # no branch nor leaf compatible from fragment to parent nodes
        exec("parent1_clone%s=fragment_p2"%crossutil.IndexLstToIndexStr2(p1_point))
        exec("parent2_clone%s=fragment_p1"%crossutil.IndexLstToIndexStr2(p2_point))
        return ([0,0,0,0],parent1_clone,parent2_clone)
    








def Koza2PointsCrossover(maxdepth,parent1,parent2,p1_map,p2_map,p1_depth,p2_depth):
    first_p_cross=[]
    for i in xrange(10):
        cp1_copy_parent1=deepcopy(parent1)
        cp1_copy_p1_map=deepcopy(p1_map)
        cp1_copy_parent2=deepcopy(parent2)
        cp1_copy_p2_map=deepcopy(p2_map)
        first_p_cross=Koza1PointCrossover(maxdepth,cp1_copy_parent1,cp1_copy_parent2,cp1_copy_p1_map,cp1_copy_p2_map,p1_depth,p2_depth)
        if first_p_cross[0]==[1,1,1,1]:
            break
    second_p_cross=[]
    for i in xrange(10):    
        cp2_copy_parent1=deepcopy(first_p_cross[1])
        cp2_copy_p1_map=crossutil.GetIndicesMappingFromTree(cp2_copy_parent1)
        cp2_copy_p1_depth=crossutil.GetDepthFromIndicesMapping(cp2_copy_p1_map)
        cp2_copy_parent2=deepcopy(first_p_cross[2])
        cp2_copy_p2_map=crossutil.GetIndicesMappingFromTree(cp2_copy_parent2)
        cp2_copy_p2_depth=crossutil.GetDepthFromIndicesMapping(cp2_copy_p2_map)
        second_p_cross=Koza1PointCrossover(maxdepth,cp2_copy_parent1,cp2_copy_parent2,cp2_copy_p1_map,cp2_copy_p2_map,cp2_copy_p1_depth,cp2_copy_p2_depth)
        if second_p_cross[0]==[1,1,1,1]:
            break
    return second_p_cross



if __name__ == '__main__':
    
    # testing 1-point crossover capability
    # by generating 2 offsprings
    for i in xrange(10000):
        a=buildtree.buildTree().AddHalfNode((0,2,'root'),0,3,7)  
        b=buildtree.buildTree().AddHalfNode((0,2,'root'),0,3,7)
        a_map=crossutil.GetIndicesMappingFromTree(a)
        b_map=crossutil.GetIndicesMappingFromTree(b)
        a_depth=crossutil.GetDepthFromIndicesMapping(a_map)
        b_depth=crossutil.GetDepthFromIndicesMapping(b_map)
    #r=Koza1PointCrossover(10,a,b,a_map,b_map,a_depth,b_depth)
    #print r
    #r2=Koza2PointsCrossover(10,a,b,a_map,b_map,a_depth,b_depth)
    #print r2
        #print a
        #print b
        r2=Koza1PointCrossover(15,a,b,a_map,b_map,a_depth,b_depth)
    #if r2[1][1][0]!=(2, 2, 'adf1'):
        print r2
        #if r2[0][0]==1 and r2[0][1]==1:
        #    print evalfitness.FinalFitness_tutorial8(evalfitness.EvalTreeForOneListInputSet_tutorial8(r2[2]))
        #if r2[0][2]==1 and r2[0][3]==1:
        #    print evalfitness.FinalFitness_tutorial8(evalfitness.EvalTreeForOneListInputSet_tutorial8(r2[1]))
        
        if r2[0]==[1,1,1,1]:
            print evalfitness.FinalFitness_tutorial8(evalfitness.EvalTreeForOneListInputSet_tutorial8(r2[1]))   
            print evalfitness.FinalFitness_tutorial8(evalfitness.EvalTreeForOneListInputSet_tutorial8(r2[2]))  
    #t1 = timeit.Timer('crossover.Koza1PointCrossover2(10,a,b,a_map,b_map,a_depth,b_depth)',  'from __main__ import a,b,a_map,b_map,a_depth,b_depth ;import crossover')
    
    #print t.timeit(100)
    #print t1.repeat(1,100)