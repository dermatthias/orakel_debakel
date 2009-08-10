"""
selection
=========
Contains methods to select individuals from a population.
So far fittest selection and tournament selection are supported.

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

import timeit
import evalfitness
import cPickle
from pysqlite2 import dbapi2 as sqlite
import psyco
import random
import operator
import copy
import wchoice
psyco.profile()



def GetDBKeysAndFitness(dbname,tablename):
    """
    Function:  GetDBKeysAndFitness
    ==============================
    the list of fitnesses with associated unique ids obtained 
    from the database. A lengthy operation. Should be only called once
    and used as an argument for the tournament or fitness selection functions. 
 
    @param dbname: path to database e.g. r'D:\3d_work\pythongp\pySTGP_0.51\src\pop_db'
    @param tablename: name of the databse table
    
    returns: the list of fitnesses with associated unique ids obtained 
    from the database
 
    """ 
    con = sqlite.connect(dbname)
    #SELECT = "select o_id, fitness from %s order by fitness" %tablename
    SELECT = "select o_id, fitness from %s" %tablename
    cur = con.cursor()
    cur.execute(SELECT)
    con.commit()
    result= cur.fetchall()
    con.close()
    sorted_result=sorted(result, key=operator.itemgetter(1))
    return sorted_result



def SelectFileFittest(pop_file):
    """
    Function:  SelectFileFittest
    ============================
    Select the fittest individual from a file
 
    @param pop_file: population file
    
    returns: the reference of one selected individual with 
 
    """ 
    # read the content of the file and evaluate add the fitness of each element in a list
    fileinput = open(pop_file,'rb')
    u = cPickle.Unpickler(fileinput)
        
    temp=u.load()
    result=[]
    # evaluate fitess of each element and store in in a list
    while temp:
        result.append(evalfitness.EvalFitness().FinalFitness(evalfitness.EvalFitness().EvalTreeForAllInputSets(temp,xrange(2))))
        try:
            temp=u.load()
        except:
            break
    fileinput.close()
    # select 'size' random indexes of elements
    mysample=xrange(len(result))
    # create the corresponding list of associated fitnesses
    mysample_fitnesses=[result[el] for el in mysample]
    ref_sample=[]
    # asssociate both in one data structure
    for i in xrange(len(mysample)):
        ref_sample.append((mysample[i],mysample_fitnesses[i])) 
    # sort them by fitness score
    ref_sample=sorted(ref_sample, key=operator.itemgetter(1))
    selected_individual=ref_sample[0]
    #print selected_individual
    return selected_individual
    
def SelectDBOneFittest(db_list):
    """
    Function:  SelectDBOneFittest
    =============================
    Select fittest individual
 
    @param db_list: the ordered list of fitnesses with associated unique ids obtained from the database
    
    returns: the reference of the one fittest individual
 
    """ 
    return db_list[0]

def SelectDBSeveralFittest(n, db_list):
    """
    Function:  SelectDBSeveralFittest
    =================================
    Select n fittest individual
    
    @param n: the number of fittest individuals
    @param db_list: the ordered list of fitnesses with associated unique ids obtained from the database
    
    @return: the reference of the one fittest individual
 
    """ 
    return db_list[:n]






    
def TournamentSelectFileOne(size, pop_file,prob_selection_fittest):
    """
    Function:  SelectFileOne
    ========================
    Select one individual from a file using Tournament selection
    appropriate and fast when using a small population (<=1000)
 
    @param size: number of individual choosen at random from the population
    @param pop_file: population file
    @param prob_selection_fittest: prob of selecting the fittest of the group
    
    @return: the reference of one selected individual with 
    prob of choosing fittest=p
    prob of choosing second fittest= p*(1-p)
    prob of choosing third fittest= p*((1-p)^2)...
 
    """ 
    # read the content of the file and evaluate add the fitness of each element in a list
    fileinput = open(pop_file,'rb')
    u = cPickle.Unpickler(fileinput)
        
    temp=u.load()
    result=[]
    # evaluate fitess of each element and store in in a list
    while temp:
        result.append(evalfitness.EvalFitness().FinalFitness(evalfitness.EvalFitness().EvalTreeForAllInputSets(temp,xrange(2))))
        try:
            temp=u.load()
        except:
            break
    fileinput.close()
    # select 'size' random indexes of elements
    mysample=random.sample(xrange(len(result)), size)
    # create the corresponding list of associated fitnesses
    mysample_fitnesses=[result[el] for el in mysample]
    ref_sample=[]
    # asssociate both in one data structure
    for i in xrange(len(mysample)):
        ref_sample.append((mysample[i],mysample_fitnesses[i])) 
    # sort them by fitness score
    ref_sample=sorted(ref_sample, key=operator.itemgetter(1))
    prob_selection=prob_selection_fittest
    # if probability of choosing fittest = 1 return fittest
    if prob_selection==1:
        selected_individual=ref_sample[0]
    # otherwise choose one element regarding the probability
    # prob of choosing fittest=p
    # prob of choosing second fittest= p*(1-p)
    # prob of choosing third fittest= p*((1-p)^2)...
    else:
        selection= [prob_selection*((1-prob_selection)**x) for x in xrange(1,len(ref_sample))]
        selection.insert(0,prob_selection)    
        wc= wchoice.wchoice(ref_sample, selection, True, True)
        selected_individual= [wc() for _ in xrange(1)]
    #print selected_individual
    return selected_individual
    
def TournamentSelectDBOne(size, prob_selection,db_list):
    """
    Function:  SelectDBOne
    ======================
    Select one individual from a database using Tournament selection
 
    @param size: number of individual choosen at random from the population
    @param prob_selection: prob of selecting the fittest of the group
    @param db_list: the list of fitnesses with associated unique ids obtained from the database
    
    @return: the reference of one selected individual with 
    prob of choosing fittest=p
    prob of choosing second fittest= p*(1-p)
    prob of choosing third fittest= p*((1-p)^2)...
 
    """ 
    
    ref_sample=random.sample(db_list, size)
    ref_sample=sorted(ref_sample, key=operator.itemgetter(1))
    #print ref_sample
    if prob_selection==1:
        selected_individual=[ref_sample[0]]
    else:
        selection= [prob_selection*((1-prob_selection)**x) for x in xrange(1,len(ref_sample))]  
        selection.insert(0,prob_selection)  
        #print selection  
        wc= wchoice.wchoice(ref_sample, selection, False, True)
        selected_individual= [wc() for _ in xrange(1)]
    #print selected_individual
    return selected_individual

def TournamentSelectDBSeveral(nb_outputs, size, prob_selection,db_list):
    """
    Function:  SelectDBSeveral
    ==========================
    Select one individual from a database using Tournament selection
 
    @param nb_outputs: repeat the tournament selection nb_outputs times, to 
    return a list nb_outputs selected individuals
    @param size: number of individual choosen at random from the population
    @param prob_selection: prob of selecting the fittest of the group
    @param db_list: the list of fitnesses with associated unique ids obtained from the database
    
    @return: return a list nb_outputs of references of individuals selected by 
    tournament
    """ 
    
    
    selection_result=[]
    i=0
    while i<nb_outputs:
        ref_sample=random.sample(db_list, size)
        ref_sample=sorted(ref_sample, key=operator.itemgetter(1))
        #print ref_sample
        if prob_selection==1:
            selected_individual=[ref_sample[0]]
        else:
            selection= [prob_selection*((1-prob_selection)**x) for x in xrange(1,len(ref_sample))]  
            selection.insert(0,prob_selection)  
            #print selection  
            wc= wchoice.wchoice(ref_sample, selection, False, True)
            selected_individual= [wc() for _ in xrange(1)]
        selection_result.append(selected_individual[0])
        i=i+1
    ##print selected_individual
    return selection_result
    
    


if __name__ == '__main__':
    #dbname=r'D:\3d_work\pythongp\pySTGP_0.51\src\pop_db'
    dbname=r'D:\mehdi\python projects\pySTGP_0.52\src\pop_db'
    tablename='tab1'
    #writepop.ClearDBTable(r'D:\3d_work\pythongp\pySTGP_0.51\src\pop_db','tab1')
    #writepop.WriteInitialPopulation2DB(100,(0,2,'root'),2,10,'AddHalfNode',dbname,tablename)
    #writepop.WriteInitialPopulation2File(100,2,2,10,'AddHalfNode','pop')
    db_list=GetDBKeysAndFitness(dbname,tablename)
    
    chosen_one1=TournamentSelectFileOne(7,'pop', 0.8)
    chosen_one2=TournamentSelectDBOne(7, 0.8,db_list)
    chosen_one3=TournamentSelectDBSeveral(20,7, 0.8,db_list)
    chosen_one4= SelectFileFittest('pop')
    chosen_one5=SelectDBOneFittest(db_list)
    chosen_one6=SelectDBSeveralFittest(5,db_list)
    #print db_list
    #print chosen_one1
    #print chosen_one2
    #print chosen_one3
    #print chosen_one4
    #print chosen_one5
    #print chosen_one6
    
    t1 = timeit.Timer('chosen_one=selection.GetDBKeysAndFitness(dbname,tablename)',  'from __main__ import dbname, tablename,db_list ;import selection')
    t2 = timeit.Timer('chosen_one=selection.TournamentSelectDBSeveral(20,7, 0.8,db_list)',  'from __main__ import dbname, tablename,db_list ;import selection')
    t3 = timeit.Timer('chosen_one=selection.TournamentSelectDBOne(7, 0.8,db_list)',  'from __main__ import dbname, tablename ,db_list;import selection')
    t4 = timeit.Timer('chosen_one=selection.SelectFileFittest(\'pop\')',  'from __main__ import dbname, tablename,db_list ;import selection')
    t5 = timeit.Timer('chosen_one=selection.SelectDBOneFittest(db_list)',  'from __main__ import dbname, tablename,db_list ;import selection')
    t6 = timeit.Timer('chosen_one=selection.SelectDBSeveralFittest(5,db_list)',  'from __main__ import dbname, tablename ,db_list;import selection')
    
    #print t.timeit(100)
    #print t3.repeat(1,10000)