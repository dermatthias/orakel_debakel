import evolver

if __name__ == "__main__":
    
    dbname=r'C:\pop_db'
    evolver.EvolutionRun(2000,(0,1,'root'),2,8,'AddHalfNode',100, 0.00001 ,0.5,0.49,7,0.8,dbname,True)