"""
settings
========
Contains all parameters for the evolutionary run, grammar rules, constraints, 
and specifics about the terminal and function set of the trees.

First we have to create a Terminal set and a Function set for the tree.
A Node object is a tuple composed of three elements e.g. (0,2,'root')
    - The first element represent the type of node:
        - 0 Root Branch
        - 1 Function Branch
        - 2 ADF Defining Branch
        - 3 Variable Leaf
        - 4 Constant Leaf
        - 5 ADF Leaf
    - The second element is the arity of the Node (number of children).
    If the number of children >0 then it is a branch node, if arity = 0 
    then it is a leaf node... e.g. (0,2,'root') means the root node has two children.

    - The third element is the name or unique identifier of the Node.
    e.g (1,2,'+') is a function branch node with two children and unique identifier '+'
    while (1,2,'*') is a function branch node with two children and unique identifier '*'


Then we define the terminal nodes, and map them with corresponding methods.
e.g.

>>>    terminals = {
'x':all_x,
'y':all_y,
'1-10':random.random()*10
}

Then we have to map values to the leaf nodes.
We define the number of examples we learn from 

>>>    nb_ex=100

We define all variable x in a list of corresponding size, and same for y.
e.g.

>>>    all_x=[]
all_y=[]
for i in xrange(nb_ex):
>>>    all_x.append(random.random()*10)
>>>    all_y.append(random.random()*10)



Then we have to define and map functions to the branch nodes to perform operations  
such as for example: arithmetic addition, subtraction, multiplication... Whatever operation is
needed in the function set of a tree should be created here.
e.g.

>>>    functions = {'+':add,
'*':multiply,
'adf2_+':add,
'adf2_*':multiply,
'adf1':adfBranch,
'adf2':adfBranch,
'root':rootBranch
}

Where functions like add are defined like this:

>>>    def add(listElem):
try:
>>>    return listElem[0]+listElem[1]
except:
>>>    raise WrongValues, "Wrong values sent to function node.\nCan't get result"
exit

We finally need to define some kind of rules or constraints that will dictate 
the shapes of the generated trees. 

We define how strongly typed we want the evolution to be. 
 
>>>    Strongly_Typed_Crossover_degree=1 

It means the trees generated have to be compliant with the constraints, and that
the crossover and mutation operations will spend some computational time 
trying to make sure offspring are compliant. 
We also specify what happens after the system has tried 100 times to produced rules-compliant offsprings using crossover but has failed.
Either we accept the unfit offsprings with Substitute_Mutation=0 or we substitute them with a mutated tree by setting Substitute_Mutation=1.
In our case, the rules are very simple, so we can set : 

>>>    Substitute_Mutation=0

Next, we need to specify a fitness function. e.g.

>>>    def FitnessFunction(my_tree):
>>>        return evalfitness.FinalFitness(evalfitness.EvalTreeForAllInputSets(my_tree,xrange(nb_eval)))

This fitness function reuses two functions :
EvalTreeForAllInputSets: parse the tree by plugging input values and computing the result obtained at the top of the tree. 
FinalFitness: returns the overall fitness of a tree over a set of datapoints using the result of the previous function as an input. It contains problem specific aspects of the fitness calculation. 

Then we set the rules treeRules for producing a tree. e.g.

>>>    # the crossover mapping spec is empty in this case
crossover_mapping=[]
# default function set applicable by for branches:
defaultFunctionSet= [(1,2,'+'),(1,2,'*'),(1,2,'-'),(1,1,'neg'),(1,1,'^2')]
# default terminal set applicable by for branches:
defaultTerminalSet= [(3,0,'x'),(3,0,'y')]
defaultTerminalSet.extend(set_ERC)
treeRules = {'root':[(defaultFunctionSet,defaultTerminalSet)],
>>>      '+':[(defaultFunctionSet,defaultTerminalSet),(defaultFunctionSet,defaultTerminalSet)],
>>>      '*':[(defaultFunctionSet,defaultTerminalSet),(defaultFunctionSet,defaultTerminalSet)],
>>>      '^2':[(defaultFunctionSet,defaultTerminalSet)],
>>>      '-':[(defaultFunctionSet,defaultTerminalSet),(defaultFunctionSet,defaultTerminalSet)],
>>>      'neg':[([(1,2,'+'),(1,2,'*'),(1,2,'-'),(1,1,'^2')],defaultTerminalSet)]
>>>      }

We also define what function branches can be changed during crossover, to make an
a fragment compliant with a new parent tree.
e.g. 

>>>    crossover_mapping=[('+','adf2_+'),('adf2_+','+'),('*','adf2_*'),('adf2_*','*')]

We finally precise that order matters in the appearance of the ADF defining branches

>>>    adfOrdered = True 

means that the ADF1 defining branch will appear before the ADF2 defining branch. 
This is especially useful if you need to define a model a forest of ordered 
sub trees...

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
import tutorial1
import tutorial2
import tutorial3
import tutorial4
import tutorial5
#import tutorial6
#import tutorial7
#import tutorial8
#import tutorial9
psyco.profile()

# setup for running tutorial 1
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

## setup for running tutorial 2
#functions = tutorial2.functions
#crossover_mapping=tutorial2.crossover_mapping
#nb_eval=tutorial2.nb_eval
#ideal_results=tutorial2.GetIdealResultsData()
#terminals =tutorial2.terminals
#Strongly_Typed_Crossover_degree=tutorial2.Strongly_Typed_Crossover_degree
#Substitute_Mutation=tutorial2.Substitute_Mutation
#treeRules = tutorial2.treeRules
#adfOrdered = tutorial2.adfOrdered
#FitnessFunction = tutorial2.FitnessFunction

## setup for running tutorial 3
#functions = tutorial3.functions
#crossover_mapping=tutorial3.crossover_mapping
#nb_eval=tutorial3.nb_eval
#ideal_results=tutorial3.GetIdealResultsData()
#terminals =tutorial3.terminals
#Strongly_Typed_Crossover_degree=tutorial3.Strongly_Typed_Crossover_degree
#Substitute_Mutation=tutorial3.Substitute_Mutation
#treeRules = tutorial3.treeRules
#adfOrdered = tutorial3.adfOrdered
#FitnessFunction = tutorial3.FitnessFunction

## setup for running tutorial 4
#functions = tutorial4.functions
#crossover_mapping=tutorial4.crossover_mapping
#nb_eval=tutorial4.nb_eval
#nb_ex=tutorial4.nb_ex
#ideal_results=tutorial4.GetIdealResultsData()
#terminals =tutorial4.terminals
#Strongly_Typed_Crossover_degree=tutorial4.Strongly_Typed_Crossover_degree
#Substitute_Mutation=tutorial4.Substitute_Mutation
#treeRules = tutorial4.treeRules
#adfOrdered = tutorial4.adfOrdered
#FitnessFunction = tutorial4.FitnessFunction

## setup for running tutorial 5
#functions = tutorial5.functions
#crossover_mapping=tutorial5.crossover_mapping
#nb_eval=tutorial5.nb_eval
#ideal_results=tutorial5.GetIdealResultsData()
#terminals =tutorial5.terminals
#Strongly_Typed_Crossover_degree=tutorial5.Strongly_Typed_Crossover_degree
#Substitute_Mutation=tutorial5.Substitute_Mutation
#treeRules = tutorial5.treeRules
#adfOrdered = tutorial5.adfOrdered
#FitnessFunction = tutorial5.FitnessFunction

