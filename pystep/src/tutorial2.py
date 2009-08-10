"""
tutorial2
=========
Contains all parameters for the evolutionary run, grammar rules, constraints, 
and specifics about the terminal and function set of the trees in tutorial2.
This example file gather all the settings for a simple polynomial regression
using this time 2 variables x and y, and adding random integer constants between 1 and 5,
and the following mathematical operators: '+','-','neg','*','^2'(or square).
We try to find the following polynomial: x^2+3y+4
from 5 sets of testing data (5 different values for x and y).
As Koza said, random constants are the "skeleton in Genetic Programming closet".
Using them will definitely slow down a search...
Any suggestions of current alternative strategies solving this problem would be 
highly welcomed :)
Considering the constraints for building the trees, the root node will only have
one child, and there will be no need for ADF in the function and terminal set.
A typical way to run the tutorial would be to:
    - modify the settings file so that:
    
    >>>     #setup for running tutorial 2
            functions = tutorial2.functions
            crossover_mapping=tutorial2.crossover_mapping
            nb_eval=tutorial2.nb_eval
            ideal_results=tutorial2.GetIdealResultsData()
            terminals =tutorial2.terminals
            Strongly_Typed_Crossover_degree=tutorial2.Strongly_Typed_Crossover_degree
            Substitute_Mutation=tutorial2.Substitute_Mutation
            treeRules = tutorial2.treeRules
            adfOrdered = tutorial2.adfOrdered
            FitnessFunction = tutorial2.FitnessFunction
    
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

from treeutil import PostOrder_Search
from collections import deque
import psyco
import random
import math
import evalfitness

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
            'root':rootBranch
            }
    
# we create the list of all possible values a variable can have in the learning examples
nb_eval=5
all_x=[]
all_y=[]
for i in xrange(nb_eval):
    all_x.append(random.random()*10)
    all_y.append(random.random()*10)

ideal_results=[]  

def GetIdealResultsData():
    for nb in xrange(nb_eval):
            ideal_results.append([all_x[nb]**2+(3*all_y[nb])+4])
    return ideal_results 


            
# then, we create a mapping of terminals
# the variables will be given a value coming from a set of examples
# the constants will just be given as such or produced by a
# random producer

terminals = {
        'x':all_x,
        'y':all_y
        }
# add a set of ephemeral random constants terminals depending on
# the number of random constants to be provided in the primitive set,
# and their range
# here we produce 5 random integer constants from ranging from 1 to 5
set_ERC=[]
for i in xrange(5):
    terminals[':'+str(i+1)]=i
    set_ERC.append((4,0,':'+str(i+1)))
    
def FitnessFunction(my_tree):
    return evalfitness.FinalFitness(evalfitness.EvalTreeForAllInputSets(my_tree,xrange(nb_eval)))

# the crossover mapping spec is empty in this case
crossover_mapping=[]
# default function set applicable by for branches:
defaultFunctionSet= [(1,2,'+'),(1,2,'*'),(1,2,'-'),(1,1,'neg'),(1,1,'^2')]
# default terminal set applicable by for branches:
defaultTerminalSet= [(3,0,'x'),(3,0,'y')]
defaultTerminalSet.extend(set_ERC)

treeRules = {'root':[(defaultFunctionSet,defaultTerminalSet)],
                    '+':[(defaultFunctionSet,defaultTerminalSet),(defaultFunctionSet,defaultTerminalSet)],
                    '*':[(defaultFunctionSet,defaultTerminalSet),(defaultFunctionSet,defaultTerminalSet)],
                    '^2':[(defaultFunctionSet,defaultTerminalSet)],
                    '-':[(defaultFunctionSet,defaultTerminalSet),(defaultFunctionSet,defaultTerminalSet)],
                    'neg':[([(1,2,'+'),(1,2,'*'),(1,2,'-'),(1,1,'^2')],defaultTerminalSet)]
                    }

Strongly_Typed_Crossover_degree=0
Substitute_Mutation=0
adfOrdered = False