"""
evolver
=======
This module contains the methods to start and finish a complete evolutionary run. 
The present version can run strongly-typed  Koza-based GP using tournament
selection.

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

import settings
import timeit
import selection
import buildtree
import cPickle
import marshal
import pprint
#import shelve
import evalfitness
from pysqlite2 import dbapi2 as sqlite
import crossutil
import math
import writepop
import copy
import mutation
import psyco
import crossover
import os

psyco.profile()
# Exceptions related to operator probability
class CrossoverProbError(Exception): pass
class MutationProbError(Exception): pass
class OperatorProbError(Exception): pass
# Exceptions related to population size
class PopSizeError(Exception): pass


def EvolutionRun(popsize,root_node,mindepth,maxdepth,buildmethod,max_nb_runs, fitness_criterion ,crossover_prob,mutation_prob,size, prob_selection,dbname,verbose):
    """
    
    Function:  EvolutionRun
    =======================
    The highest level function of the package. 
    It starts an evolutionary run with given parameters,and gives indications of
    what is found after each generation.
    @param popsize: size of the population
    root_node: specify the root node and its arity (nb of children). e.g. (0,2,'root') 
    @param mindepth: min tree depth (at the moment only 2 working) 
    @param maxdepth: max depth of trees in new generation (should be >=3) 
    @param buildmethod: which Koza method is used to build the trees (either 
    'AddHalfNode' or 'AddFullNode' or 'AddGrowNodeMin' respectively for 
    Ramped Half-n-Half, Full, or Half)
    @param max_nb_runs: the search will gon on until a maximum number of generations
    is reached
    @param fitness_criterion: the search will stop if the fitness found is <= to
    the ideal fitness
    @param crossover_prob: probability of crossover (will determine what proportion of 
    the population will be replaced by crossover-generated offsprings)  
    @param mutation_prob: probability of crossover (will determine what proportion of 
    the population will be replaced by mutation-generated offsprings)  
    @param dbname: path to database e.g. r'D:\3d_work\pythongp\pySTGP_0.51\src\pop_db'    
    @param verbose: print the best tree of each generation
 
    """ 
    try:
        os.remove(dbname)
    except:
        pass
    
    current_best_fitness=float('inf')
    tablenames=[]
    #build the intial population of random trees at generation 0 
    tablenames.append('tab0')
    writepop.WriteInitialPopulation2DB(popsize,root_node,mindepth,maxdepth,buildmethod,dbname,tablenames[0])
    # get best fitness
    db_list=selection.GetDBKeysAndFitness(dbname,tablenames[0])
    chosen_one=selection.SelectDBOneFittest(db_list)
    current_best_fitness=chosen_one[1]
    print ''.join(['generation 0 (db table name = tab0): -> best fit individual has id:',`chosen_one[0]`,' and fitness:',`current_best_fitness`])
    
    if verbose==True:
        #writepop.GetPopStatFromDB(dbname,tablenames[0])
        con = sqlite.connect(dbname)
        SELECT = "select tree from %s where o_id=%d" % (tablenames[0],chosen_one[0])
        cur = con.cursor()
        cur.execute(SELECT)
        con.commit()
        myresult= cur.fetchone()
        con.close()
        best_tree=copy.deepcopy(marshal.loads(myresult[0]))
        print best_tree
    if current_best_fitness<=fitness_criterion:
        print ''.join(['found solution: generation 0, db_id:',`chosen_one[0]`,' and fitness:',`current_best_fitness`])
    else:    
        # evolve the population for max_nb_runs
        i=1
        while i<max_nb_runs and current_best_fitness>fitness_criterion:
            tablenames.append(''.join(['tab',`i`]))
            TournamentSelectionEvolveDBPopulation2(popsize,maxdepth,crossover_prob,mutation_prob,size, prob_selection,dbname,tablenames[i-1],tablenames[i])
            db_list=selection.GetDBKeysAndFitness(dbname,tablenames[i])
            chosen_one=selection.SelectDBOneFittest(db_list)
            current_best_fitness=chosen_one[1]
            print ''.join(['generation ',`i`,' (db table name = tab',`i`,'): -> best fit individual has id:',`chosen_one[0]`,' and fitness:',`current_best_fitness`])
            
            if verbose==True:
                #writepop.GetPopStatFromDB(dbname,tablenames[i])
                con = sqlite.connect(dbname)
                SELECT = "select tree from %s where o_id=%d" % (tablenames[i],chosen_one[0])
                cur = con.cursor()
                cur.execute(SELECT)
                con.commit()
                myresult= cur.fetchone()
                con.close()
                best_tree=copy.deepcopy(marshal.loads(myresult[0]))
                print best_tree
            
            i=i+1
        else:
            if current_best_fitness<=fitness_criterion:
                print ''.join(['found solution at generation ',`i-1`,', with fitness:',`current_best_fitness`])
                writepop.PrintPopFromDB(dbname,tablenames[i-1],'lastpop')
            else:
                print ''.join(['Fitness stopping criterion not found. Run ended at generation ',`i`])
             
    

    
    
    
def TournamentSelectionEvolveDBPopulation2(popsize,maxdepth,crossover_prob,mutation_prob,size, prob_selection,dbname,tablename,tablename2):
    """
    Function:  TournamentSelectionEvolveDBPopulation2
    =================================================
    create a new population of randomly generated trees and write this new generation
    to a new table of name 'tab'+generation number in the database.
 
    @param popsize: size of the population
    @param maxdepth: max depth of trees in new generation 
    @param crossover_prob: probability of crossover (will determine what proportion of 
    the population will be replaced by crossover-generated offsprings)
    @param mutation_prob: probability of crossover (will determine what proportion of 
    the population will be replaced by mutation-generated offsprings)
    @param dbname: path to database e.g. r'D:\3d_work\pythongp\pySTGP_0.51\src\pop_db'
    @param tablename: name of the database table of the initial population
    @param tablename2: name of the database table of the next generation
 
    """ 
    
    if crossover_prob>1 or crossover_prob<0:
        raise CrossoverProbError, "Crossover Probability should be in interval [0,1]"
        exit
    if mutation_prob>1 or mutation_prob<0:
        raise MutationProbError, "Crossover Probability should be in interval [0,1]"
        exit
    reproduction_prob= 1-(crossover_prob+mutation_prob)
    if reproduction_prob>1 or reproduction_prob<0:
        raise OperatorProbError, "Sum of Mutation and Crossover Probability should be in interval [0,1]"
        exit
    if popsize<3:
        raise PopSizeError, "The size of the population must be at least 3"
        exit
    
    new_pop=[]
    trees=[]
    
    # build the appropriate size for the crossover offsprings, 
    # mutation offsprings and reproduction offsprings
    crossover_size= math.ceil(popsize*crossover_prob)
    mutation_size= math.ceil(popsize*mutation_prob)
    reproduction_size= math.ceil(popsize*reproduction_prob)
    sizes=[crossover_size,mutation_size,reproduction_size]
    theoretical_size=sum(sizes)
    if theoretical_size >popsize:
        nb=theoretical_size-popsize
        if crossover_size>mutation_size and mutation_size>=reproduction_size:
            crossover_size=crossover_size-nb
        elif mutation_size>crossover_size and crossover_size>=reproduction_size:
            mutation_size=crossover_size-nb
        elif reproduction_size>crossover_size and crossover_size>=mutation_size:
            mutation_size=crossover_size-nb
        else:
            crossover_size=crossover_size-nb   
    #print crossover_size
    #print mutation_size
    #print reproduction_size
    # get the ordered list of fitnesses with identifier keys
    db_list=selection.GetDBKeysAndFitness(dbname,tablename)
    # start by selecting fittest parents for reproduction
    reprod=selection.SelectDBSeveralFittest(int(reproduction_size), db_list)
    #print reprod
    # then select parents for crossover
    cross=selection.TournamentSelectDBSeveral(int(crossover_size),size, prob_selection,db_list)
    #print cross
    # then select parents for mutation
    mut=selection.TournamentSelectDBSeveral(int(mutation_size),size, prob_selection,db_list)
    #print mut
    

    #open database
    con = sqlite.connect(dbname)
    #add to new population these reproduced offsprings
    #writepop.ClearDBTable(dbname,tablename2)
    #con.execute("create table %s(o_id INTEGER PRIMARY KEY,tree TEXT,\
    # tree_mapping TEXT, treedepth INTEGER, evaluated INTEGER, fitness FLOAT)"%tablename2)
    
    # apply reproduction operator and copy to new population database
    for elem in reprod:
        o_id=elem[0]
        #print o_id
        SELECT = "select tree, tree_mapping, treedepth, evaluated, fitness from %s where o_id=%d" % (tablename,o_id)
        cur = con.cursor()
        cur.execute(SELECT)
        con.commit()
        myresult= cur.fetchone()
        my_tree=copy.deepcopy(marshal.loads(myresult[0]))
        my_tree_mapping=copy.deepcopy(marshal.loads(myresult[1]))
        my_treedepth=myresult[2]
        my_evaluated=myresult[3]
        my_fitness=myresult[4]
        # write a copy of the selected parent in the new database
        new_pop.append((o_id,my_tree, my_tree_mapping,my_treedepth,my_evaluated,my_fitness))
        trees.append(my_tree)
        #con.execute("insert into %s(o_id,tree,tree_mapping,treedepth,evaluated,fitness) values (NULL,?,?,?,?,?)"%tablename2,(buffer(marshal.dumps(myresult[0],-1)),buffer(marshal.dumps(myresult[1],-1)),my_treedepth,my_evaluated,my_fitness))
        con.commit()
    # apply mutation operator and copy to new population database  
    for elem in mut:
        o_id=elem[0]
        #print o_id
        SELECT = "select tree, tree_mapping, treedepth, evaluated, fitness from %s where o_id=%d" % (tablename,o_id)
        cur = con.cursor()
        cur.execute(SELECT)
        con.commit()
        myresult= cur.fetchone()
        my_tree=copy.deepcopy(marshal.loads(myresult[0]))
        my_tree_mapping=copy.deepcopy(marshal.loads(myresult[1]))
        my_treedepth=myresult[2]
        my_evaluated=myresult[3]
        my_fitness=myresult[4]
        same_tree=True
        mt=mutation.Mutate(maxdepth,my_tree,my_tree_mapping,my_treedepth)
        same_tree=mt[0]
        if mt in trees:
            same_tree=True
        # make sure to try another mutation if the offspring is identical to the parent
        if same_tree==True:
            while same_tree==True:
                mt=mutation.Mutate(maxdepth,my_tree,my_tree_mapping,my_treedepth)
                same_tree=mt[0]
        mt_map=crossutil.GetIndicesMappingFromTree(mt[1])
        mt_depth=crossutil.GetDepthFromIndicesMapping(mt_map)
        mt_evaluated=1
        # get fitness of the tree
        result_fitness=settings.FitnessFunction(mt[1])
        #mt_fitness=evalfitness.EvalTreeForAllInputSets(mt[1],xrange(settings.nb_eval))
        #mt_fitness=evalfitness.EvalTreeForOneListInputSet(mt[1])
        #result_fitness=evalfitness.FinalFitness(mt_fitness)
        #result_fitness=evalfitness.FinalFitness2(mt_fitness)
        #result_fitness=evalfitness.FinalFitness3(mt_fitness)
        #result_fitness=evalfitness.FinalFitness4(mt_fitness)
        #print result_fitness
        # write a copy of the selected parent in the new database
        new_pop.append((o_id,mt[1], mt_map,mt_depth,mt_evaluated,result_fitness))
        #con.execute("insert into %s(o_id,tree,tree_mapping,treedepth,evaluated,fitness) values (NULL,?,?,?,?,?)"%tablename2,(buffer(marshal.dumps(mt[1],-1)),buffer(marshal.dumps(mt_map,-1)),mt_depth,mt_evaluated,result_fitness))
        con.commit()
      
    # apply crossover operator and copy to new population database  
    for elem in cross:
        # select the second parent using tournament selection
        parent2=selection.TournamentSelectDBSeveral(2,7, 0.8,db_list)
        # make sure parent2 is different from parent1
        if elem==parent2[0]:
            elem2=parent2[1]
        else:
            elem2=parent2[0]
        
           
        o_id=elem[0]
        o_id2=elem2[0]
        #print o_id
        #print o_id2
        cur = con.cursor()
        SELECT1 = "select tree, tree_mapping, treedepth, evaluated, fitness from %s where o_id=%d" % (tablename,o_id) 
        cur.execute(SELECT1)
        con.commit()
        myresult1= cur.fetchone()
        SELECT2 = "select tree, tree_mapping, treedepth, evaluated, fitness from %s where o_id=%d" % (tablename,o_id2)
        cur.execute(SELECT2)
        con.commit()
        myresult2= cur.fetchone()
        
        my_tree1=copy.deepcopy(marshal.loads(myresult1[0]))
        my_tree1_mapping=copy.deepcopy(marshal.loads(myresult1[1]))
        my_tree1depth=myresult1[2]
        my_evaluated1=myresult1[3]
        my_fitness1=myresult1[4]
        
        my_tree2=copy.deepcopy(marshal.loads(myresult2[0]))
        my_tree2_mapping=copy.deepcopy(marshal.loads(myresult2[1]))
        my_tree2depth=myresult2[2]
        my_evaluated2=myresult2[3]
        my_fitness2=myresult2[4]
        #cs=crossover.Koza1PointCrossover(maxdepth,my_tree1,my_tree2,my_tree1_mapping,my_tree2_mapping,my_tree1depth,my_tree2depth)
        #print cs
        #cs=mutation.Mutate(maxdepth,my_tree,my_tree_mapping,my_treedepth)
        
        
        
        cs_evaluated=1
        # get fitness of the tree
        input_sets=xrange(settings.nb_eval)
        cs=[[0,0,0,0]]
        i=0
        while cs[0]!=[1,1,1,1] and i<100 :
            #cp_my_tree1=copy.deepcopy(marshal.loads(myresult1[0]))
            #cp_my_tree1_mapping=copy.deepcopy(marshal.loads(myresult1[1]))
            #cp_my_tree2=copy.deepcopy(marshal.loads(myresult2[0]))
            #cp_my_tree2_mapping=copy.deepcopy(marshal.loads(myresult2[1]))
            cp_my_tree1=marshal.loads(myresult1[0])
            cp_my_tree1_mapping=marshal.loads(myresult1[1])
            cp_my_tree2=marshal.loads(myresult2[0])
            cp_my_tree2_mapping=marshal.loads(myresult2[1])
            cs=crossover.Koza1PointCrossover(maxdepth,cp_my_tree1,cp_my_tree2,cp_my_tree1_mapping,cp_my_tree2_mapping,my_tree1depth,my_tree2depth)
            #trees.append(cs[1])
            #trees.append(cs[2])
            i=i+1
        #print cs[1]
        #print cs[2]
        
        # if after trying 50 times , the crossover cannot give a correct offspring, then 
        # create a new offspring using mutation...
        if cs[0]!=[1,1,1,1] and settings.Substitute_Mutation==1:
            mt=mutation.Mutate(maxdepth,cp_my_tree1,cp_my_tree1_mapping,my_tree1depth)
            mt_map=crossutil.GetIndicesMappingFromTree(mt[1])
            mt_depth=crossutil.GetDepthFromIndicesMapping(mt_map)
            mt_evaluated=1
            # get fitness of the tree
            result_fitness=settings.FitnessFunction(mt[1])
            new_pop.append((o_id,mt[1], mt_map,mt_depth,mt_evaluated,result_fitness))
        else:
            
            try:
                offspring1_result_fitness=settings.FitnessFunction(cs[1])
                
                #cs_offspring1_fitness=evalfitness.EvalTreeForAllInputSets(cs[1],input_sets)
                #cs_offspring1_fitness=evalfitness.EvalTreeForOneListInputSet(cs[1])
            except:
                print 'pb when applying fitness function to results of crossover'
                print cs[1]
                
                print cs[0]
            try:
                
                offspring2_result_fitness=settings.FitnessFunction(cs[2])
                #cs_offspring1_fitness=evalfitness.EvalTreeForAllInputSets(cs[1],input_sets)
                #cs_offspring1_fitness=evalfitness.EvalTreeForOneListInputSet(cs[1])
            except:
                print 'pb when applying fitness function to results of crossover'
                
                print cs[2]
                print cs[0]
            #try:
            #    cs_offspring2_fitness=evalfitness.EvalTreeForAllInputSets(cs[2],input_sets)
                #cs_offspring2_fitness=evalfitness.EvalTreeForOneListInputSet(cs[2])
            #except:
            #    print cs[2]
            #    print cs[0]
            #offspring1_result_fitness=evalfitness.FinalFitness(cs_offspring1_fitness)
            #offspring2_result_fitness=evalfitness.FinalFitness(cs_offspring2_fitness)
            #offspring1_result_fitness=evalfitness.FinalFitness2(cs_offspring1_fitness)
            #offspring2_result_fitness=evalfitness.FinalFitness2(cs_offspring2_fitness)
            #offspring1_result_fitness=evalfitness.FinalFitness3(cs_offspring1_fitness)
            #offspring2_result_fitness=evalfitness.FinalFitness3(cs_offspring2_fitness)
            #offspring1_result_fitness=evalfitness.FinalFitness4(cs_offspring1_fitness)
            #offspring2_result_fitness=evalfitness.FinalFitness4(cs_offspring2_fitness)
            #print result_fitness
            # write a copy of the selected parent in the new database
            if offspring1_result_fitness>=offspring2_result_fitness:
                cs_map=crossutil.GetIndicesMappingFromTree(cs[1])
                cs_depth=crossutil.GetDepthFromIndicesMapping(cs_map)
                #con.execute("insert into %s(o_id,tree,tree_mapping,treedepth,evaluated,fitness) values (NULL,?,?,?,?,?)"%tablename2,(buffer(marshal.dumps(cs[1],-1)),buffer(marshal.dumps(cs_map,-1)),cs_depth,cs_evaluated,offspring1_result_fitness))
                new_pop.append((o_id,cs[1], cs_map,cs_depth,cs_evaluated,offspring1_result_fitness))
                #trees.append(cs[1])
            if offspring1_result_fitness<offspring2_result_fitness:
                cs_map=crossutil.GetIndicesMappingFromTree(cs[2])
                cs_depth=crossutil.GetDepthFromIndicesMapping(cs_map)
                #con.execute("insert into %s(o_id,tree,tree_mapping,treedepth,evaluated,fitness) values (NULL,?,?,?,?,?)"%tablename2,(buffer(marshal.dumps(cs[2],-1)),buffer(marshal.dumps(cs_map,-1)),cs_depth,cs_evaluated,offspring2_result_fitness))
                new_pop.append((o_id,cs[2], cs_map,cs_depth,cs_evaluated,offspring2_result_fitness))
            #trees.append(cs[2])
        con.commit()     
    con.close()
    
    con = sqlite.connect(dbname)
    #writepop.ClearDBTable(dbname,tablename2)
    con.execute("create table %s(o_id INTEGER PRIMARY KEY,tree TEXT,\
     tree_mapping TEXT, treedepth INTEGER, evaluated INTEGER, fitness FLOAT)"%tablename2)
    #print len(new_pop)
    for i in xrange(0,popsize):
        con.execute("insert into %s(o_id,tree,tree_mapping,treedepth,evaluated,fitness) values (NULL,?,?,?,?,?)"%tablename2,(buffer(marshal.dumps(new_pop[i][1],-1)),buffer(marshal.dumps(new_pop[i][2],-1)),new_pop[i][3],new_pop[i][4],new_pop[i][5]))
    con.commit()
    con.close()
    
    
    
    

    
if __name__ == '__main__':
    #dbname=r'D:\3d_work\pythongp\pySTEP_0.95\src\pop_db'
    dbname=r'D:\mehdi\python projects\pySTEP_0.95\src\pop_db'
    #tablename='tab8'    
    #tablename2='tab9'
    #db_list=selection.GetDBKeysAndFitness(dbname,tablename)
    #TournamentSelectionEvolveDBPopulation(100,8,0.9,0.05,dbname,tablename,tablename2)
    #(popsize,maxdepth,crossover_prob,mutation_prob,dbname,tablename,tablename2)
    #t2 = timeit.Timer('new_generation=evolver.TournamentSelectionEvolveDBPopulation2(6000,10,0.9,0.05,dbname,tablename,tablename2)',  'from __main__ import dbname, tablename, db_list,tablename2 ;import evolver')
    #print t2.repeat(1,1)
    
    
    #EvolutionRun(2000,(0,2,'root'),2,6,'AddHalfNode',100, 0.1 ,0.5,0.49,dbname,True)
    EvolutionRun(2000,(0,3,'root'),2,6,'AddHalfNode',100, 0.1 ,0.5,0.49,7,0.8,dbname,True)