"""
evalfitness
===========
Contains methods to evaluate the fitness of a tree.

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

from treeutil import PostOrder_Search
from collections import deque
import psyco
import random
import math
import settings
import buildtree
import timeit
import settings
import fitnessutil

psyco.profile()

    
def EvalTreeForOneInputSet(myTree, input_set_ref):
        """
        Function:  EvalTreeForOneInputSet
        =================================
        Function used to evaluate a tree by pluggin in
        one set of values (one learning example)
 
        @param myTree: the nested list representing a tree
        @param input_set_ref: the set of values to plug into the tree
        @return: the fitness of the tree for this set of values
        """ 
        resultStack=deque()
        adfDict={}
        # examine every node in the tree in pre-order taversal
        # (leaves first and then branches)
        for elem in PostOrder_Search(myTree):
            # if the node is a leaf (variable, or constant),
            # add its value to the result stack
            if elem[0]==3:
                resultStack.append(settings.terminals[elem[2]][input_set_ref])
            elif elem[0]==4:
                resultStack.append(settings.terminals[elem[2]])
            # if the node is a function with n arguments, pop the result stack
            # n times. Get these popped elemnts as arguments for the function,
            # and replace the top of the stack by the result of the function
            elif elem[0]==1:
                nb= elem[1]
                name = elem[2]
                tempResult=deque()
                for i in xrange(0,nb):
                    try:
                        tempResult.append(resultStack.pop())
                    except:
                        print myTree
                        print elem
                        print resultStack
                        exit
                resultStack.extend(map(settings.functions[name],[tempResult]))
            # if the node is an ADF branch, add the top of the stack to
            # the ADF dictionary
            elif elem[0]==2:
                adfDict[elem[2]]= resultStack[-1]
            # if the node is an ADF terminal, add the corresponding ADF
            # branch value available in the dictionary to the result stack
            elif elem[0]==5:
                resultStack.append(adfDict[elem[2]])
            # if the node is a root, apply the root function to all
            # direct children and return the result.
            elif elem[0]==0:
                name = elem[2]
                tempResult=[]
                while resultStack:
                    tempResult.append(resultStack.popleft())
                resultStack.extend(map(settings.functions[name],[tempResult]))
        return resultStack[0]
    


def EvalTreeForOneListInputSet(myTree):
        """
        Function:  EvalTreeForOneInputSet
        =================================
        Function used to evaluate a tree by pluggin in
        one list of values (one list of data points)
 
        @param myTree: the nested list representing a tree
        @return: the fitness of the tree for this set of values
        """ 
        resultStack=deque()
        adfDict={}
        # examine every node in the tree in pre-order taversal
        # (leaves first and then branches)
        for elem in PostOrder_Search(myTree):
            # if the node is a leaf (variable, or constant),
            # add its value to the result stack
            if elem[0]==3:
                resultStack.append(settings.terminals[elem[2]])
                
            elif elem[0]==4:
                resultStack.append(settings.terminals[elem[2]])
            # if the node is a function with n arguments, pop the result stack
            # n times. Get these popped elemnts as arguments for the function,
            # and replace the top of the stack by the result of the function
            elif elem[0]==1:
                nb= elem[1]
                name = elem[2]
                tempResult=deque()
                for i in xrange(0,nb):
                    tempResult.append(resultStack.pop())
                resultStack.extend(map(settings.functions[name],[tempResult]))
            # if the node is an ADF branch, add the top of the stack to
            # the ADF dictionary
            elif elem[0]==2:
                adfDict[elem[2]]= resultStack[-1]
            # if the node is an ADF terminal, add the corresponding ADF
            # branch value available in the dictionary to the result stack
            elif elem[0]==5:
                resultStack.append(adfDict[elem[2]])
            # if the node is a root, apply the root function to all
            # direct children and return the result.
            elif elem[0]==0:
                name = elem[2]
                tempResult=[]
                while resultStack:
                    tempResult.append(resultStack.popleft())
                resultStack.extend(map(settings.functions[name],[tempResult]))
        return resultStack[0]

def EvalTreeForOneListInputSet_tutorial8(myTree):
        """
        Function:  EvalTreeForOneInputSet2
        ==================================
        Function used to evaluate a tree by pluggin in
        one list of values (one list of data points)
 
        @param myTree: the nested list representing a tree
        @return: the fitness of the tree for this set of values
        """ 
        resultStack=deque()
        adfDict={}
        # examine every node in the tree in pre-order taversal
        # (leaves first and then branches)
        for elem in PostOrder_Search(myTree):
            # if the node is a leaf (variable, or constant),
            # add its value to the result stack
            if elem[0]==3:
                resultStack.append(settings.terminals[elem[2]])                
            elif elem[0]==4:
                resultStack.append(settings.terminals[elem[2]])   
            # if the node is a function with n arguments, pop the result stack
            # n times. Get these popped elemnts as arguments for the function,
            # and replace the top of the stack by the result of the function
            elif elem[0]==1:
                nb= elem[1]
                name = elem[2]
                tempResult=deque()
                for i in xrange(nb):
                    tempResult.append(resultStack.pop())
                resultStack.extend(map(settings.functions[name],[tempResult]))
                
            # if the node is an ADF branch, add the top of the stack to
            # the ADF dictionary
            elif elem[0]==2:
                adfDict[elem[2]]= resultStack[-1]
            # if the node is an ADF terminal, add the corresponding ADF
            # branch value available in the dictionary to the result stack
            elif elem[0]==5:
                resultStack.append(adfDict[elem[2]])
            # if the node is a root, apply the root function to all
            # direct children and return the result.
            elif elem[0]==0:
                name = elem[2]
                tempResult=[]
                while resultStack:
                    tempResult.append(resultStack.popleft())
                resultStack.extend(map(settings.functions[name],[tempResult]))
        return resultStack[0]


def EvalTreeForOneListInputSet_tutorial9(myTree):
        """
        Function:  EvalTreeForOneInputSet2
        ==================================
        Function used to evaluate a tree by pluggin in
        one list of values (one list of data points)
 
        @param myTree: the nested list representing a tree
        @return: the fitness of the tree for this set of values
        """ 
        resultStack=deque()
        adfDict={}
        # examine every node in the tree in pre-order taversal
        # (leaves first and then branches)
        for elem in PostOrder_Search(myTree):
            # if the node is a leaf (variable, or constant),
            # add its value to the result stack
            if elem[0]==3:
                resultStack.append(settings.terminals[elem[2]])                
            elif elem[0]==4:
                resultStack.append(settings.terminals[elem[2]])   
            # if the node is a function with n arguments, pop the result stack
            # n times. Get these popped elemnts as arguments for the function,
            # and replace the top of the stack by the result of the function
            elif elem[0]==1:
                nb= elem[1]
                name = elem[2]
                tempResult=deque()
                for i in xrange(nb):
                    tempResult.append(resultStack.pop())
                resultStack.extend(map(settings.functions[name],[tempResult]))
                
            # if the node is an ADF branch, add the top of the stack to
            # the ADF dictionary
            elif elem[0]==2:
                adfDict[elem[2]]= resultStack[-1]
            # if the node is an ADF terminal, add the corresponding ADF
            # branch value available in the dictionary to the result stack
            elif elem[0]==5:
                resultStack.append(adfDict[elem[2]])
            # if the node is a root, apply the root function to all
            # direct children and return the result.
            elif elem[0]==0:
                name = elem[2]
                tempResult=[]
                while resultStack:
                    tempResult.append(resultStack.popleft())
                resultStack.extend(map(settings.functions[name],[tempResult]))
        return resultStack[0]


def EvalTreeForAllInputSets(myTree, input_sets):
        """
        Function:  EvalTreeForAllInputSets
        ==================================
        Function used to evaluate a tree by pluggin in
        several sets of values
 
        @param myTree: the nested list representing a tree
        @param input_sets: the set of values to plug into the tree
        @return: the fitnesses of the tree over several sets of values
        """ 
        results=[]
        val=len(input_sets)
        for elem in xrange(val):
            results.append(EvalTreeForOneInputSet(myTree, elem))
        return results
    # compute global fitness of an individual across all different examples



def FinalFitness(intermediate_outputs):
        """
        Function:  FinalFitness
        =======================
        Compute global fitness of an individual. Intended when wanting to refine
        the fitness score.
 
        @param intermediate_outputs: the fitnesses of the tree over several sets of
        values
        @return: global fitness
        """ 
        final_output=0
        # each element represents one different sample or set of input data
        # the size of each represents the number of examples
        #each sub-element represents the value(s) obtained at the top of a three for one input
        #In this particular case, we simply add the difference of all results with an ideal solution
        
        # the ideal solution is : [adf1 = x+y adf2 = add1*(y-x)]
        # build a corresponding list of two-elements sub lists
        # then evaluate the sum of the difference with our built models
        goal_function=[]
        for nb in xrange(settings.nb_eval):
        #for nb in xrange(settings.nb_ex):
        
            ideal_results=settings.ideal_results[nb]
            obtained_results=intermediate_outputs[nb]
            
            
            for el in obtained_results:
                try:
                    if math.isinf(el):
                        return el
                except:
                    return float('inf')
            # sum the absolute values of the differences over one example
            diff= sum( [math.fabs(ideal_results[x]-obtained_results[x]) for x in xrange(len(ideal_results))])
            final_output= final_output+diff
        return final_output

def FinalFitness2(intermediate_outputs):
        """
        Function:  FinalFitness2
        ========================
        Compute global fitness of an individual. Intended when wanting to refine
        the fitness score.
 
        @param intermediate_outputs: the fitnesses of the tree over several sets of
        values
        @return: global fitness
        """ 
        final_output=0
        # each element represents one different sample or set of input data
        # the size of each represents the number of examples
        #each sub-element represents the value(s) obtained at the top of a three for one input
        #In this particular case, we simply add the difference of all results with an ideal solution
        
        # the ideal solution is : [adf1 = x+y adf2 = add1*(y-x)]
        # build a corresponding list of two-elements sub lists
        # then evaluate the sum of the difference with our built models
        ideal_results=settings.ideal_results
        obtained_results=intermediate_outputs
        for res in xrange(len(settings.ideal_results)):
            for el in obtained_results[res]:
                try:
                    if math.isinf(el):
                        return el
                except:
                    return float('inf')
            # sum the absolute values of the differences over one example
            diff= sum( [math.fabs(ideal_results[res][x]-obtained_results[res][x]) for x in xrange(settings.nb_ex)])
            final_output= final_output+diff
        return final_output

def FinalFitness3(intermediate_outputs):
        """
        Function:  FinalFitness3
        ========================
        Compute global fitness of an individual. Intended when wanting to refine
        the fitness score.
 
        @param intermediate_outputs: the fitnesses of the tree over several sets of
        values
        @return: global fitness
        """ 
        final_output=0
        # each element represents one different sample or set of input data
        # the size of each represents the number of examples
        #each sub-element represents the value(s) obtained at the top of a three for one input
        #In this particular case, we simply add the difference of all results with an ideal solution
        
        # the ideal solution is : [adf1 = x+y adf2 = add1*(y-x)]
        # build a corresponding list of two-elements sub lists
        # then evaluate the sum of the difference with our built models
        goal_function=[]
        for nb in xrange(settings.nb_eval):
        #for nb in xrange(settings.nb_ex):
        
            ideal_results=settings.ideal_results[nb]
            obtained_results=intermediate_outputs[nb]
            #print ideal_results
            #print obtained_results
            for el in obtained_results:
                try:
                    if math.isinf(el):
                        return el
                except:
                    return float('inf')
            # sum the absolute values of the differences over one example
            # here we use a very very puzzling python list comprehension... This deserve a bit of explanation.
            # In general, the expression "T if C is true, or F if C is false" can be written as (F, T)[bool(C)].
            # This single line could be replaced by a simpler but slower expression of the type:
            #z=[]
            #for i in range(10):
            #    if  C:
            #        z.append(T)
            #    else:
            #        z.append(F)
            # In our case, if the first element of obtained_resultsis is True (the result of the if statement)
            # then use the result produce by the second branch, otherwise use the result produced by the third 
            # branch.
            # As far as we are concerned, list comprehension are faster + compact + more memory efficient.
            # so for this crucial fitness calculation bit, I chose this solution...
            # May the deities of the Python programming pantheon forgive me (Sorry Guido...).
            diff= sum( [(math.fabs(ideal_results[x]-obtained_results[1]) ,math.fabs(ideal_results[x]-obtained_results[2]) )[obtained_results[0]] for x in xrange(len(ideal_results))])
            final_output= final_output+diff
        return final_output


def FinalFitness4(intermediate_outputs):
        """
        Function:  FinalFitness3
        ========================
        Compute global fitness of an individual. Intended when wanting to refine
        the fitness score.
 
        @param intermediate_outputs: the fitnesses of the tree over several sets of
        values
        @return: global fitness
        """ 
        final_output=0
        # each element represents one different sample or set of input data
        # the size of each represents the number of examples
        #each sub-element represents the value(s) obtained at the top of a three for one input
        #In this particular case, we simply add the difference of all results with an ideal solution
        
        # the ideal solution is : [adf1 = x+y adf2 = add1*(y-x)]
        # build a corresponding list of two-elements sub lists
        # then evaluate the sum of the difference with our built models
        goal_function=[]
       
        for nb in xrange(len(intermediate_outputs)):
            for el in intermediate_outputs[nb]:
                for el2 in el:
                    try:
                        if isinstance(el2, bool):
                            pass
                        elif math.isinf(el2):
                            return el2
                    except:
                        return float('inf')
        # sum the absolute values of the differences over one example
        # here we use a very very puzzling python list comprehension... This deserve a bit of explanation.
        # In general, the expression "T if C is true, or F if C is false" can be written as (F, T)[bool(C)].
        # This single line could be replaced by a simpler but slower expression of the type:
        #z=[]
        #for i in range(10):
        #    if  C:
        #        z.append(T)
        #    else:
        #        z.append(F)
        # In our case, if the first element of obtained_resultsis is True (the result of the if statement)
        # then use the result produce by the second branch, otherwise use the result produced by the third 
        # branch.
        # As far as we are concerned, list comprehension are faster + compact + more memory efficient.
        # so for this crucial fitness calculation bit, I chose this solution...
        # May the deities of the Python programming pantheon forgive me (Sorry Guido...).
        final_output= sum([(math.fabs(settings.ideal_results[x][y]-intermediate_outputs[2][x][y]),math.fabs(settings.ideal_results[x][y]-intermediate_outputs[1][x][y])) [intermediate_outputs[0][x][y]] for x in xrange(len(intermediate_outputs[1])) for y in xrange(len(intermediate_outputs[1][x]))])
        
        return final_output


def FinalFitness_tutorial8(intermediate_outputs):
        """
        Function:  FinalFitness3
        ========================
        Compute global fitness of an individual. Intended when wanting to refine
        the fitness score.
 
        @param intermediate_outputs: the fitnesses of the tree over several sets of
        values
        @return: global fitness
        """ 
        final_output=0
        goal_function=[]
        
        #for i in xrange( len(settings.ideal_results)):
        #    for j in xrange( len(settings.ideal_results[i])):
        #        print settings.ideal_results[i][j]
        #print settings.inputdata
        #print intermediate_outputs[0]
        #print intermediate_outputs[1]
        #print intermediate_outputs[2]
        try:
            result=fitnessutil.ReplaceUsingBinaryMask(settings.inputdata,intermediate_outputs[0],intermediate_outputs[1],intermediate_outputs[2] )
            # expand the compact array
            uncompressed_result= [fitnessutil.UncompressList(result[x][0]) for x in xrange(len(result))]
            uncompressed_ideal_results= [fitnessutil.UncompressList(settings.ideal_results[x]) for x in xrange(len(result))]
            
            
            final_output= sum([(0,1)[uncompressed_result[x][y]!=uncompressed_ideal_results[x][y]] for x in xrange(len(uncompressed_result)) for y in xrange(len(uncompressed_result[x]))])
        except:
            final_output=float('inf')
        #print result[0][0]
        
        #final_output= sum([(math.fabs(settings.ideal_results[x][y]-intermediate_outputs[2][x][y]),math.fabs(settings.ideal_results[x][y]-intermediate_outputs[1][x][y])) [intermediate_outputs[0][x][y]] for x in xrange(len(intermediate_outputs[1])) for y in xrange(len(intermediate_outputs[1][x]))])
        #for i in xrange( len(result)):
        #    for j in xrange( len(result[i])):
        #        print result[i][j]
        
        return final_output
    

def FinalFitness_tutorial9(intermediate_outputs):
        """
        Function:  FinalFitness3
        ========================
        Compute global fitness of an individual. Intended when wanting to refine
        the fitness score.
 
        @param intermediate_outputs: the fitnesses of the tree over several sets of
        values
        @return: global fitness
        """ 
        final_output=0
        goal_function=[]
        
        #for i in xrange( len(settings.ideal_results)):
        #    for j in xrange( len(settings.ideal_results[i])):
        #        print settings.ideal_results[i][j]
        #print settings.inputdata
        #print intermediate_outputs
        #print intermediate_outputs[1]
        #print intermediate_outputs[2]
        
        try:
            #print list(xrange(1,(len(intermediate_outputs)/3)+1))
            temp_input=settings.inputdata
            #print temp_input
            for i in xrange(1,(len(intermediate_outputs)/3)+1): 
                temp_result=fitnessutil.ReplaceUsingBinaryMask(temp_input,intermediate_outputs[(i*3)-1],intermediate_outputs[(i*3)-2],intermediate_outputs[(i*3)-3] )
                temp_input=temp_result
                #print temp_input
           
            # expand the compact array
            uncompressed_result= [fitnessutil.UncompressList(temp_result[x][0]) for x in xrange(len(temp_result))]
            uncompressed_ideal_results= [fitnessutil.UncompressList(settings.ideal_results[x]) for x in xrange(len(temp_result))]
            
            
            final_output= sum([(0,1)[uncompressed_result[x][y]!=uncompressed_ideal_results[x][y]] for x in xrange(len(uncompressed_result)) for y in xrange(len(uncompressed_result[x]))])
        except:
            final_output=float('inf')
        
        #print result[0][0]
        
        #final_output= sum([(math.fabs(settings.ideal_results[x][y]-intermediate_outputs[2][x][y]),math.fabs(settings.ideal_results[x][y]-intermediate_outputs[1][x][y])) [intermediate_outputs[0][x][y]] for x in xrange(len(intermediate_outputs[1])) for y in xrange(len(intermediate_outputs[1][x]))])
        #for i in xrange( len(result)):
        #    for j in xrange( len(result[i])):
        #        print result[i][j]
        
        return final_output


if __name__ == '__main__':


    #for i in xrange(2000):
        #a=buildtree.buildTree().AddFullNode((0,3,'root'),0,2,8) 
        #a=buildtree.buildTree().AddFullNode((0,3,'root'),0,8) 
        a=buildtree.buildTree().AddFullNode((0,2,'root'),0,8)
        #print a
        #print i
       
        #print r
       
        #print FinalFitness_tutorial9(EvalTreeForOneListInputSet_tutorial9(a))
        
        #t1 = timeit.Timer('evalfitness.EvalTreeForOneListInputSet_tutorial9(a)' ,  'from __main__ import a ;import evalfitness')
        t2 = timeit.Timer('evalfitness.FinalFitness_tutorial9(evalfitness.EvalTreeForOneListInputSet_tutorial9(a))' ,  'from __main__ import a ;import evalfitness')
        #print t1.timeit(100)
        print t2.timeit(1000)
        #print FinalFitness_tutorial8(EvalTreeForOneListInputSet_tutorial8(a))
        
        #print FinalFitness3(EvalTreeForAllInputSets(a,xrange(20)))
        #print FinalFitness4(EvalTreeForOneListInputSet(a))
    #print EvalTreeForOneInputSet(a,0)
    
        #i=EvalTreeForOneListInputSet2(a)
        #print i
        #print FinalFitness4(i)
    #t1 = timeit.Timer('evalfitness.EvalTreeForOneInputSet(a,0)' ,  'from __main__ import a ;import evalfitness')
    #t2 = timeit.Timer('evalfitness.EvalTreeForAllInputSets(a,xrange(1000))' ,  'from __main__ import a ;import evalfitness')
    #t3 = timeit.Timer('i=evalfitness.EvalTreeForAllInputSets(a,xrange(1000)); evalfitness.FinalFitness(i)' ,  'from __main__ import a ;import evalfitness')
    
    #print t.timeit(100)
    #print t1.repeat(1,1000)
    #print t2.repeat(1,1000)
    #print t3.repeat(1,1000)
    #print sum(t1.repeat(1,1000))/1000
    #print sum(t2.repeat(1,1000))/1000
    #print sum(t3.repeat(1,1000))/1000