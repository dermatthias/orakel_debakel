"""
tutorial1
=========
Contains all parameters for the evolutionary run, grammar rules, constraints, 
and specifics about the terminal and function set of the trees in tutorial1.
This example file gather all the settings for a simple polynomial regression
using one variable x and the following mathematical operators: '+','-','neg','*','^2'(or square),'cos','sin'.
We try to find a third degree polynomial: x^3 + x^2 + cos(x)
from 2 sets of testing data (2 different values for x).
Considering the constraints for building the trees, the root node will only have
one child, and there will be no need for ADF in the function and terminal set.
A typical way to run the tutorial would be to:
    - modify the settings file so that: 
    
    >>>     #setup for running tutorial 1
            functions = tutorial1.functions
            terminals =tutorial1.terminals
            crossover_mapping=tutorial1.crossover_mapping
            nb_eval=tutorial1.nb_eval
            ideal_results=tutorial1.GetIdealResultsData()
            Strongly_Typed_Crossover_degree=tutorial1.Strongly_Typed_Crossover_degree
            Substitute_Mutation=tutorial1.Substitute_Mutation
            treeRules = tutorial1.treeRules
            adfOrdered = tutorial1.adfOrdered
            FitnessFunction = tutorial1.FitnessFunction
    
    - run the evolution in the main method, and make sure that the root node parameter
    only have one child.e.g.
    
    >>>    import evolver
    if __name__ == "__main__":
    >>>    dbname=r'C:\pop_db'
    >>>    evolver.EvolutionRun(2000,(0,1,'root'),2,8,'AddHalfNode',100, 0.00001 ,0.5,0.49,7,0.8,dbname,True)

    This means that we define:
    - a population size of 2000 individuals,
    - a root node with 1 child
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



import psyco
import evalfitness
import random
import math

psyco.profile()


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
            'root':rootBranch
            }
    
    # we create the list of all possible values a variable can have in the learning examples
nb_eval=2
all_x=[]
for i in xrange(nb_eval):
    all_x.append(random.random()*10)
    
# then, we create a mapping of terminals
# the variables will be given a value coming from a set of examples
# the constants will just be given as such or produced by a
# random producer    
terminals = {
        'x':all_x
        }

# ideal polynomial to find    
ideal_results=[]  
def GetIdealResultsData():
    for nb in xrange(nb_eval):
            ideal_results.append([all_x[nb]**3+all_x[nb]**2+math.cos(all_x[nb])])
    return ideal_results 

            
def FitnessFunction(my_tree):
    return evalfitness.FinalFitness(evalfitness.EvalTreeForAllInputSets(my_tree,xrange(nb_eval)))
    

crossover_mapping=[]

# default function set applicable by for branches:
defaultFunctionSet= [(1,2,'+'),(1,2,'*'),(1,1,'^2'),(1,2,'-'),(1,1,'cos'),(1,1,'sin'),(1,1,'neg')]
# default terminal set applicable by for branches:
defaultTerminalSet= [(3,0,'x')]
treeRules = {'root':[(defaultFunctionSet,defaultTerminalSet)],
                    '+':[(defaultFunctionSet,defaultTerminalSet),(defaultFunctionSet,defaultTerminalSet)],
                    '*':[(defaultFunctionSet,defaultTerminalSet),(defaultFunctionSet,defaultTerminalSet)],
                    '^2':[(defaultFunctionSet,defaultTerminalSet)],
                    '-':[(defaultFunctionSet,defaultTerminalSet),(defaultFunctionSet,defaultTerminalSet)],
                    'neg':[([(1,2,'+'),(1,2,'*'),(1,2,'-'),(1,1,'cos'),(1,1,'sin')],defaultTerminalSet)],
                    'cos':[([(1,2,'+'),(1,2,'*'),(1,2,'-'),(1,1,'sin'),(1,1,'neg')],defaultTerminalSet)],
                    'sin':[([(1,2,'+'),(1,2,'*'),(1,2,'-'),(1,1,'cos'),(1,1,'neg')],defaultTerminalSet)]
                    }

Strongly_Typed_Crossover_degree=0
Substitute_Mutation=0
adfOrdered = False
