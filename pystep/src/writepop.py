"""
writepop
========
Contains all classes used to write and extract individuals and populations 
on the SQLite database.

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
import buildtree
import cPickle
import marshal
import pprint
import psyco
import timeit
import evalfitness
from pysqlite2 import dbapi2 as sqlite
import crossutil


psyco.profile()



def ClearDBTable(dbname,table):
    """
    Function:  ClearDBTable
    =======================
    clear the table of the database
    
    @param dbname: path to database e.g. r'D:\3d_work\pythongp\pySTGP_0.51\src\pop_db'
    @param table: name of the database table
    
    """ 

    con = sqlite.connect(dbname)
    con.execute("drop table %s"%table)
    con.commit()
    con.close()



def WriteInitialPopulation2DB(popsize,root_node,mintreesize,maxtreesize,buildmethod,dbname,tablename):
    """
    Function:  WriteInitialPopulation2DB
    ====================================
    create a new population of randomly generated trees and write them to a database
 
    @param popsize: size of the population
    @param root_node: specify the root node and its arity (nb of children). e.g. (0,2,'root')
    @param mintreesize: min tree depth (at the moment only 2 working)
    @param maxtreesize: max tree depth (At least 2)
    @param buildmethod: which Koza method is used to build the trees (either 
    'AddHalfNode' or 'AddFullNode' or 'AddGrowNodeMin' respectively for 
    Half, Full, or Ramped Half-n-Half)
    @param dbname: path to database e.g. r'D:\3d_work\pythongp\pySTGP_0.51\src\pop_db'
    @param tablename: name of the database table
 
    """ 

    con = sqlite.connect(dbname)
    con.execute("create table %s(o_id INTEGER PRIMARY KEY,tree TEXT,\
     tree_mapping TEXT, treedepth INTEGER, evaluated INTEGER, fitness FLOAT)"%tablename)
    trees=[]
    i=0
    while i <popsize:
        # create a tree individual
        method = getattr(buildtree.buildTree(),buildmethod)
        my_tree = method(root_node,0,mintreesize,maxtreesize)
        if my_tree not in trees:
        #    my_tree = method(root_node,0,mintreesize,maxtreesize)
            trees.append(my_tree)
        # create its tree mapping
            my_tree_indices=crossutil.GetIndicesMappingFromTree(my_tree)
        # get depth of the tree
            depth=crossutil.GetDepthFromIndicesMapping(my_tree_indices)
        # get fitness of the tree
            resultfitness=settings.FitnessFunction(my_tree)
            #myfitness=evalfitness.EvalTreeForAllInputSets(my_tree,xrange(settings.nb_eval))
            #myfitness=evalfitness.EvalTreeForOneListInputSet(my_tree)
        #print myfitness
            #resultfitness=evalfitness.FinalFitness(myfitness)
            #resultfitness=evalfitness.FinalFitness2(myfitness)
            #resultfitness=evalfitness.FinalFitness4(myfitness)
        #print resultfitness
            con.execute("insert into %s(o_id,tree,tree_mapping,treedepth,evaluated,fitness) values (NULL,?,?,?,?,?)"%tablename,(buffer(marshal.dumps(my_tree,-1)),buffer(marshal.dumps(my_tree_indices,-1)),depth,1,resultfitness))
            i=i+1
    con.commit()
    con.close()

    

def PrintPopFromDB(dbname,tablename,filename):
    """
    Function:  PrintPopFromDB
    =========================
    print the population of trees with id references, tree depth and fitness scores
    
    @param dbname: path to database e.g. r'D:\3d_work\pythongp\pySTGP_0.51\src\pop_db'
    @param tablename: name of the database table
 
    """ 

    con = sqlite.connect(dbname)
    SELECT = "select o_id,tree,treedepth,fitness from %s order by fitness" % tablename
    cur = con.cursor()
    cur.execute(SELECT)
    con.commit()
    myresult= cur.fetchall()
    con.close()
    
    output = open(filename,'w')
    for elem in myresult:
        output.write(''.join([`elem[0]`,`marshal.loads(elem[1])`,`elem[2]`,`elem[3]`,'\n']))
    output.close()



def GetPopStatFromDB(dbname,tablename):
    """
    Function:  GetPopStatFromDB
    ===========================
    get statistical data about the population
    
    @param dbname: path to database e.g. r'D:\3d_work\pythongp\pySTGP_0.51\src\pop_db'
    @param tablename: name of the database table
 
    """ 

    con = sqlite.connect(dbname)
    SELECT = "select o_id,tree,treedepth,fitness from %s order by fitness" % tablename
    cur = con.cursor()
    cur.execute(SELECT)
    con.commit()
    myresult= cur.fetchall()
    con.close()
    
    
    depths=[]
    fit=[]
    trees=[]
    for elem in myresult:
        ntree=marshal.loads(elem[1])
        if ntree not in trees:
            trees.append(ntree)
        depths.append(elem[2])
        #fit.append(elem[3])
    lengt=len(depths)
    uniques_trees=len(trees)
    av_depth=sum(depths)/len(myresult)
    av_fit=sum(fit)/len(myresult)
    print ''.join(['average depth: ',`av_depth`,' nb of unique trees: ',`uniques_trees`, ' over ', `lengt`])
    
    



if __name__ == '__main__':
    #dbname=r'D:\3d_work\pythongp\pySTGP_0.51\src\pop_db'
    dbname=r'D:\mehdi\python projects\pySTGP_0.52\src\pop_db'
    tablename='tab1'
    #ClearDBTable(dbname,tablename)
    #WriteInitialPopulation2DB(100,(0,2,'root'),2,10,'AddHalfNode',dbname,tablename)
    #WriteInitialPopulation2File(100,2,2,10,'AddHalfNode','pop')
    #WriteInitialPopulation2DB2(100,(0,2,'root'),2,10,'AddHalfNode',dbname,tablename)

    #t1 = timeit.Timer("writepop.WriteInitialPopulation2DB2(100,(0,2,'root'),2,10,'AddHalfNode',dbname,tablename)",  'from __main__ import dbname, tablename ;import writepop')
    t2 = timeit.Timer("writepop.WriteInitialPopulation2DB(10000,(0,2,'root'),2,10,'AddHalfNode',dbname,tablename)",  'from __main__ import dbname, tablename ;import writepop')
    print t2.repeat(1,1)



