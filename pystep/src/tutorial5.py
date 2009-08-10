"""
tutorial5
=========
Contains all parameters for the evolutionary run, grammar rules, constraints, 
and specifics about the terminal and function set of the trees in tutorial5.
In this example, we evolve hybrid system: a model containing discrete values 
and logic operators and numerical operations.
More specifically, we will evolve if_then_else types rules that will determine 
the application of different polynomials...
from 20 sets of testing data (20 different values for x and y).
Considering the constraints for building the trees, the root node will have
3 children, and these will be ordered ADF defining branches (we simply won't use ADF terminals nodes)
describing the structure of the if then else statement.
The solution found should be the equivalent of this expression:
if x>y then cos(x) else sin(y)
  
A typical way to run the tutorial would be to:
    - modify the settings file so that: 
    
    >>>     # setup for running tutorial 5
            functions = tutorial5.functions
            crossover_mapping=tutorial5.crossover_mapping
            nb_eval=tutorial5.nb_eval
            ideal_results=tutorial5.GetIdealResultsData()
            terminals =tutorial5.terminals
            Strongly_Typed_Crossover_degree=tutorial5.Strongly_Typed_Crossover_degree
            Substitute_Mutation=tutorial5.Substitute_Mutation
            treeRules = tutorial5.treeRules
            adfOrdered = tutorial5.adfOrdered
            FitnessFunction = tutorial5.FitnessFunction
    
    - use a different fitness function for the evaluation of a hybrid system (we
    use both discrete and continuous values now!)
    We create 1 new fitness function:
         - FinalFitness3 is a modification of FinalFitness that take as input
         sets of If Then Else types of trees and return the sum of their fitnesses.
         These fitness functions are called in 3 different places. We need to update
         the code that call them.
         These fitness functions are called in FitnessFunction in the tutorial5 module. 
         
         >>>    def FitnessFunction(my_tree):
         >>>        return evalfitness.FinalFitness3(evalfitness.EvalTreeForAllInputSets(my_tree,xrange(nb_eval)))
         
    - run the evolution in the main method, and make sure that the root node parameter
    only have three children.e.g.
    
    >>>    import evolver
    if __name__ == "__main__":
    >>>    dbname=r'C:\pop_db'
    >>>    evolver.EvolutionRun(2000,(0,3,'root'),3,8,'AddHalfNode',100, 0.00001 ,0.5,0.49,7,0.8,dbname,True)

    This means that we define:
    - a population size of 2000 individuals,
    - a root node with 3 children
    - a minimum tree depth of 3 (because the constraints of the tree would not work for a depth <3)
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

from treeutil import PostOrder_Search
from collections import deque
import psyco
import random
import math
import evalfitness

psyco.profile()



def equal_(listElem):
    try:
         if listElem[0]==listElem[1]:
             return True
         else:
             return False
    except:
        raise WrongValues, "Wrong values sent to function node.\nCan't get result"
        exit

def superior_(listElem):
    try:
         if listElem[0]>listElem[1]:
             return True
         else:
             return False
    except:
        raise WrongValues, "Wrong values sent to function node.\nCan't get result"
        exit
        
def inferior_(listElem):
    try:
         if listElem[0]<listElem[1]:
             return True
         else:
             return False
    except:
        raise WrongValues, "Wrong values sent to function node.\nCan't get result"
        exit

def and_(listElem):
    try:
         if listElem[0] and listElem[1]:
             return True
         else:
             return False
    except:
        raise WrongValues, "Wrong values sent to function node.\nCan't get result"
        exit

def or_(listElem):
    try:
         if listElem[0] or listElem[1]:
             return True
         else:
             return False
    except:
        raise WrongValues, "Wrong values sent to function node.\nCan't get result"
        exit



# first, we create result processing methods for each function:
def add(listElem):
    try:
        return listElem[0]+listElem[1]
    except:
        raise WrongValues, "Wrong values sent to function node.\nCan't get result"
        exit
    
def sub(listElem):
    try:
        return listElem[0]-listElem[1]
    except:
        raise WrongValues, "Wrong values sent to function node.\nCan't get result"
        exit

def neg(listElem):
    try:
        return 0-listElem[0]
    except:
        raise WrongValues, "Wrong values sent to function node.\nCan't get result"
        exit


        
def multiply(listElem):
    try:
        return listElem[0]*listElem[1]
    except:
        raise WrongValues, "Wrong values sent to function node.\nCan't get result"
        exit

def square(listElem):
    try:
        return listElem[0]*listElem[0]
    except:
        raise WrongValues, "Wrong values sent to function node.\nCan't get result"
        exit

def cos(listElem):
    try:
        return math.cos(listElem[0])
    except:
        raise WrongValues, "Wrong values sent to function node.\nCan't get result"
        exit
        
def sin(listElem):
    try:
        return math.sin(listElem[0])
    except:
        raise WrongValues, "Wrong values sent to function node.\nCan't get result"
        exit

def if_(x):
    try:
        return x
    except:
        raise WrongValues, "Wrong values sent to function node.\nCan't get result"
        exit

def then_(x):
    try:
        return x
    except:
        raise WrongValues, "Wrong values sent to function node.\nCan't get result"
        exit

def else_(x):
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
            '-':sub,
            'neg':neg,
            '*':multiply,
            '^2':square,
            'cos':cos,
            'sin':sin,
            '=':equal_,
            '>':superior_,
            '<':inferior_,
            'and':and_,
            'or':or_,
            'if':if_,
            'then':then_,
            'else':else_,
            'root':rootBranch
            }
    
    # we create the list of all possible values a variable can have in the learning examples
nb_eval=20
all_x=[]
all_y=[]
for i in xrange(nb_eval):
    all_x.append(random.random()*10)
    all_y.append(random.random()*10)
# then, we create a mapping of terminals
# the variables will be given a value coming from a set of examples
# the constants will just be given as such or produced by a
# random producer    
terminals = {
        'x':all_x,
        'y':all_y
        }

# ideal polynomial to find    
ideal_results=[]  
def GetIdealResultsData():
    for nb in xrange(nb_eval):
            #ideal_results.append([all_x[nb]**3-all_x[nb]+math.cos(all_x[nb])])
            if all_x[nb]>all_y[nb]:
                ideal_results.append([math.cos(all_x[nb])])
            else:
                ideal_results.append([math.sin(all_y[nb])])
    return ideal_results 

            
def FitnessFunction(my_tree):
    return evalfitness.FinalFitness3(evalfitness.EvalTreeForAllInputSets(my_tree,xrange(nb_eval)))


crossover_mapping=[]

# default function set applicable by for branches:
defaultFunctionSet= [(1,2,'+'),(1,2,'*'),(1,1,'^2'),(1,2,'-'),(1,1,'cos'),(1,1,'sin'),(1,1,'neg')]
# default terminal set applicable by for branches:
defaultTerminalSet= [(3,0,'x'),(3,0,'y')]
treeRules = {'root':[([(2,1,'if')],[]),([(2,1,'then')],[]),([(2,1,'else')],[])],
                    'if':[([(1,2,'and'),(1,2,'or'),(1,2,'>'),(1,2,'<'),(1,2,'=')],[])],
                    'then':[(defaultFunctionSet,defaultTerminalSet)],
                    'else':[(defaultFunctionSet,defaultTerminalSet)],
                    'and':[([(1,2,'and'),(1,2,'or'),(1,2,'>'),(1,2,'<'),(1,2,'=')],[]),([(1,2,'and'),(1,2,'or'),(1,2,'>'),(1,2,'<'),(1,2,'=')],[])],
                    'or':[([(1,2,'and'),(1,2,'or'),(1,2,'>'),(1,2,'<'),(1,2,'=')],[]),([(1,2,'and'),(1,2,'or'),(1,2,'>'),(1,2,'<'),(1,2,'=')],[])],
                    '=':[(defaultFunctionSet,defaultTerminalSet),(defaultFunctionSet,defaultTerminalSet)],
                    '>':[(defaultFunctionSet,defaultTerminalSet),(defaultFunctionSet,defaultTerminalSet)],
                    '<':[(defaultFunctionSet,defaultTerminalSet),(defaultFunctionSet,defaultTerminalSet)],
                    '+':[(defaultFunctionSet,defaultTerminalSet),(defaultFunctionSet,defaultTerminalSet)],
                    '*':[(defaultFunctionSet,defaultTerminalSet),(defaultFunctionSet,defaultTerminalSet)],
                    '^2':[(defaultFunctionSet,defaultTerminalSet),(defaultFunctionSet,defaultTerminalSet)],
                    '-':[(defaultFunctionSet,defaultTerminalSet),(defaultFunctionSet,defaultTerminalSet)],
                    'neg':[([(1,2,'+'),(1,2,'*'),(1,2,'-'),(1,1,'cos'),(1,1,'sin')],defaultTerminalSet)],
                    'cos':[([(1,2,'+'),(1,2,'*'),(1,2,'-'),(1,1,'sin'),(1,1,'neg')],defaultTerminalSet)],
                    'sin':[([(1,2,'+'),(1,2,'*'),(1,2,'-'),(1,1,'cos'),(1,1,'neg')],defaultTerminalSet)]
                    }

Strongly_Typed_Crossover_degree=0
Substitute_Mutation=0
adfOrdered = True