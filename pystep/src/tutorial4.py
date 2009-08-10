"""
tutorial4
=========
Contains all parameters for the evolutionary run, grammar rules, constraints, 
and specifics about the terminal and function set of the trees in tutorial4.
This example file gather all the settings for a 'multiple' polynomial regression.
We want to evolve a system of ordered polynomial equations by using the
mathematical operators: '+','*' and the ADF: ADF1 and ADF2, in the said order.
an ADF2 branch could then call for an ADF1 terminal, but not the opposite.  
We try to find the following model being shaped as a system of polynomials: 

|ADF1=x+y

|ADF2=ADF1^3

from 1 set of 1000 testing data (1000 different values for x and y).
This time, each tree does not have to be evaluated 1000 times. We will input
a list of 1000 data points in the variable leafs of the tree. There is not much time
difference to process 1000 data-points than 5 when we use this trick!
Considering the constraints for building the trees, the root node will have 2 
children ADF1 and ADF2 (in order), and ADF2 must be able to reuse ADF1 as a 
terminal... A typical way to run the tutorial would be to:
    - modify the settings file so that:
    
    >>>     # setup for running tutorial 4
            functions = tutorial4.functions
            crossover_mapping=tutorial4.crossover_mapping
            nb_eval=tutorial4.nb_eval
            nb_ex=tutorial4.nb_ex
            ideal_results=tutorial4.GetIdealResultsData()
            terminals =tutorial4.terminals
            Strongly_Typed_Crossover_degree=tutorial4.Strongly_Typed_Crossover_degree
            Substitute_Mutation=tutorial4.Substitute_Mutation
            treeRules = tutorial4.treeRules
            adfOrdered = tutorial4.adfOrdered
            FitnessFunction = tutorial4.FitnessFunction
    
    - use a different fitness function for the evaluation of a list
     of values instead of a value. We create 2 new fitness functions:
         - EvalTreeForOneListInputSet is a modification of the original 
         EvalTreeForOneInputSet.
         - FinalFitness2 is a modification of FinalFitness that take as input
         the result returned by the new EvalTreeForOneListInputSet
         
         These fitness functions are called in FitnessFunction in the tutorial4 module. 
         
         >>>    def FitnessFunction(my_tree):
         >>>        return evalfitness.FinalFitness2(evalfitness.EvalTreeForOneListInputSet(my_tree))  
        
    - run the evolution in the main method, and make sure that the root node parameter
    only have two children.e.g.
    
    >>>    import evolver
    if __name__ == "__main__":
    >>>    dbname=r'C:\pop_db'
    >>>    evolver.EvolutionRun(2000,(0,2,'root'),2,8,'AddHalfNode',100, 0.00001 ,0.5,0.49,7,0.8,dbname,True)

    This means that we define:
    - a population size of 2000 individuals,
    - a root node with 2 children
    - a minimum tree depth of 2
    - a maximum tree depth of 8
    - the use of a Ramped half and Half Koza tree building method
    - a maximum number of runs of 100 generations before we stop
    - a stoping fitness criteria of 0.1 (if the fitness<=0.1, solution found)
    - a crossover probability of 0.5
    - a mutation probability of 0.49
    - a reproduction probability of 0.01 (automatically deduced from the 2 previous values)
    - the size of the tournament selection
    - the probability of selecting the fitttest during tournament selection 
    - a database of name and path dbname
    - a run done in verbose mode (printing the fittest element of each generation) 
    
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

import array
import psyco
import random
import math
from treeutil import PostOrder_Search
from collections import deque
import evalfitness

psyco.profile()

# first, we create result processing methods for each function:
def add(listElem):
    try:
        result=[]
        for i in xrange(len(listElem[0])):
            result.append(listElem[0][i]+listElem[1][i])
        return result
    except:
        raise WrongValues, "Wrong values sent to function node.\nCan't get result"
        exit
    

def multiply(listElem):
    try:
        result=[]
        for i in xrange(len(listElem[0])):
            result.append(listElem[0][i]*listElem[1][i])
        return result
    except:
        raise WrongValues, "Wrong values sent to function node.\nCan't get result"
        exit

def adfBranch(x):
    try:
        return x
    except:
        raise WrongValues, "Wrong values sent to function node.\nCan't get result"
        exit

def rootBranch(x):
    try:
        return x
    except:
        raise WrongValues, "Wrong values sent to function node.\nCan't get result"
        exit

# then, we create a set of functions and associate them with the corresponding
# processing methods
functions = {'+':add,
            '*':multiply,
            'adf2_+':add,
            'adf2_*':multiply,
            'adf1':adfBranch,
            'adf2':adfBranch,
            'root':rootBranch
            }
# when swapping subtrees during crossover, we can transform the following branches:
# + can be transformed into ADF2_+, and so on...
crossover_mapping=[('+','adf2_+'),('adf2_+','+'),('*','adf2_*'),('adf2_*','*')]
    
    
# we create the list of all possible values a variable can have 
# Here we tell the system it only learn from one example, so it will 
# only evaluate the tree one time. The difference will be that this unique
# variable will be an array of 200 of format 'double' ! These 200 variables
# will then be evaluated at once when a tree is evaluated. 
nb_eval=1
all_x=[]
all_y=[]

nb_ex=1000
for i in xrange(nb_ex):
    all_x.append(random.random()*10)
    all_y.append(random.random()*10)
#print all_x
#print all_y
#print add([all_x,all_y])
#print multiply([all_x,all_y])
# encapsulate all data of x and y inside arrays so that the tree
# will evaluate a whole array in one go...

ideal_results=[]

def GetIdealResultsData():
    temp1=[]
    for nb in xrange(nb_ex):
        temp1.append(all_x[nb]+all_y[nb])
    temp2=[]
    for nb in xrange(nb_ex):
        temp2.append((all_x[nb]+all_y[nb])**3)
    ideal_results.append(temp1)
    ideal_results.append(temp2)
    return ideal_results
    # then, we create a mapping of terminals
    # the variables will be given a value coming from a set of examples
    # the constants will just be given as such or produced by a
# random producer
terminals = {
        'x':all_x,
        'y':all_y
        }

#MaxDepth=5
Strongly_Typed_Crossover_degree=1

def FitnessFunction(my_tree):
    return evalfitness.FinalFitness2(evalfitness.EvalTreeForOneListInputSet(my_tree))

# default function set applicable by for branches:
defaultFunctionSet= [(1,2,'+'),(1,2,'*')]
# default terminal set applicable by for branches:
defaultTerminalSet= [(3,0,'x'),(3,0,'y')]
Adf2DefaultFunctionSet= [(1,2,'adf2_+'),(1,2,'adf2_*')]
Adf2DefaultTerminalSet= [(3,0,'x'),(3,0,'y'),(5,0,'adf1')]
treeRules = {'root':[ ([(2,1,'adf1')],[]) , ([(2,1,'adf2')],[]) ],
                    'adf1':[(defaultFunctionSet,defaultTerminalSet)],
                    'adf2':[(Adf2DefaultFunctionSet,Adf2DefaultTerminalSet)],
                    '+':[(defaultFunctionSet,defaultTerminalSet),(defaultFunctionSet,defaultTerminalSet)],
                    '*':[(defaultFunctionSet,defaultTerminalSet),(defaultFunctionSet,defaultTerminalSet)],
                    'adf2_+':[(Adf2DefaultFunctionSet,Adf2DefaultTerminalSet),(Adf2DefaultFunctionSet,Adf2DefaultTerminalSet)],
                    'adf2_*':[(Adf2DefaultFunctionSet,Adf2DefaultTerminalSet),(Adf2DefaultFunctionSet,Adf2DefaultTerminalSet)],
                    }

Strongly_Typed_Crossover_degree=1
Substitute_Mutation=0
adfOrdered = True