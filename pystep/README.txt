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

http://sourceforge.net/projects/pystep/

===============================================================
WELCOME TO PYSTEP or Python Strongly Typed gEnetic Programming:
===============================================================


 

A light Genetic Programming API that allows the user to easily evolve populations of trees with precise grammatical and structural constraints.

Presently functional, running and, as far as I can see, stable. 

I wish to add more tutorials, add extra features for reading the populations from the database, features from the GP litterature such as co-evolution, more fency operators and modify some of the crossover code. 

There has been a lot of improvement going on since the first version:

- The Koza Strongly-Typed flavoured build methods have been simplified and optimized (around 10 times faster for a code length reduced by five!) 

- It is now possible to use a specific function-terminal sets for each of the children node. And these children node are built in the order they appear in the tree constraints (this feature only existed for ADF in the previous version). This makes pySTEP very competitive and gives it a serious advantage over existing Strongly typed GP packages :) 

- It is now possible to specify what happens after the system has tried 100 times to produced rules-compliant offsprings using crossover but has failed (this might happens if we use a lot of constraining rules). Either we accept the unfit offsprings with Substitute_Mutation=0 or we substitute them with a mutated tree by setting Substitute_Mutation=1.

- The parameters of the tournament selection are integrated in the main function that calls the evolutionary run. 

- Code for crossover and mutation is now simplified and clearer. 

You need to have installed:

- Python 2.6.1

- psyco for python 2.6

- pysqlite for python 2.6 and the corresponding version of SQlite

- numpy for python 2.6

To execute the evolution run of the first tutorial, create a main method in Python (there is one already made for you in the package if you want...).
Inside, you need to:
1- import the module called "evolver"
2- define a name and path for you database.
3- and then call the EvolutionRun method from the evolver module.
e.g. of a main file:
     
import evolver
    if __name__ == "__main__":
    	dbname=r'C:\pop_db'
    	evolver.EvolutionRun(2000,(0,1,'root'),2,8,'AddHalfNode',100, 0.00001 ,0.5,0.49,7,0.8,dbname,True)

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

The run will create a database file containing tables of names tab0, tab1,... where every table contains the population for the corresponding generation. 

For those who want details of the populations, there are methods in the module writepop that allow to:
- get stats from a database table: GetPopStatFromDB(dbname,tablename)
- print the population from a database table to a file: PrintPopFromDB(dbname,tablename,filename)


A detailed html documentation explains how to set and describes each and every of the 5 different tutorials (see tutorial1 to tutorial5 in the index.html).
Tutorial 1 is about a simple polynomial regression with one variable.
Tutorial 2 is about a simple polynomial regression with two variables and Integers Random Constants
Tutorial 3 is about evolving a forest of trees in a certain order. Each tree being a different polynomial, able to reuse previous trees. This is the equivalent of Strongly Typed ADF.
Tutorial 4 is like tutorial 4, but shows how to modify the system to run an evolution through 1000 different data points without having to evaluate a tree 1000 times but simply 1 time !
Tutorial 5 shows how to evolve a hybrid system mixing discretes and continuous values, arithmetic and logical operators.

On a more personal note, I enjoyed programming this API using the Eclipse IDE (there is a pyDev module that allows to use Eclipse to programm in Python. It's great and I recommend it :) )

Feedback and input are highly welcomed :)

Cheers!

Mehdi Khoury