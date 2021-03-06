import pulp as solver
from pulp import *
import Graph
import os
import gc
import signal
from tqdm import tqdm
z = 0
solvers = [solver.CPLEX(timeLimit=7200), solver.GLPK(), solver.GUROBI()]
solverUsado = 0

problems_packing = ["Instances/packing/"+i for i in os.listdir("Instances/packing/")]
problems_sep = ["Instances/separated/"+i for i in os.listdir("Instances/separated/")]
problems = problems_packing + problems_sep
print(problems)
#problems = problems[3:]
def signal_handler(signum, frame):
    raise Exception("Timed out!")

for ptk in problems:
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(8100)
    try:
        print("Initializing graph",ptk)
        g = Graph.Graph(400,16.67,z)
        g.initProblem(ptk)
        g.z = len(g.edgeCuts)*2
        print("Initializing variables X")
        var = [(i+','+str(t)) for i in g.edge for t in range(1,g.z)]
        print("Initializing variables Y")
        var2 = [(str(i)+','+str(t)) for i in g.vertices for t in range(1,g.z)]
        X = solver.LpVariable.dicts("X",var,cat=solver.LpBinary)
        Y = solver.LpVariable.dicts("Y",var2,cat=solver.LpBinary)
        problem = solver.LpProblem("The best Cut" , solver.LpMinimize)
        print("Initializing F.O")
        problem += (solver.lpSum(X.get(str(i.split(',')[0])+','+str(i.split(',')[1])+','+str(t))*g.mis[i.split(',')[0]][i.split(',')[1]] for i in tqdm(g.edge,desc="First sum F.O") for t in range(1,g.z)) + 
                        solver.lpSum(((g.pis[k.split(',')[0]][k.split(',')[1]]))-(
                                           (g.mis[k.split(',')[0]][k.split(',')[1]])) for k in tqdm(g.edgeCuts,desc="Second sum F.O"))/2)+solver.lpSum(X.get(str(i.split(',')[0])+','+str(i.split(',')[1])+','+str(1))*g.initDes[int(i.split(',')[0])-1] for i in tqdm(g.edge,desc="Third sum F.O"))
        print("Initializing First Restriction")
        for t in tqdm(range(1,g.z)):
            problem += solver.lpSum(X.get(str(i.split(',')[0])+','+str(i.split(',')[1])+','+str(t)) for i in g.edge) <= 1
        print("Initializing Second Restriction")   
        for i in tqdm(g.edgeCuts):
            problem += solver.lpSum(X.get(str(i.split(',')[0])+','+str(i.split(',')[1])+','+str(t))+X.get(str(i.split(',')[1])+','+str(i.split(',')[0])+','+str(t)) for t in range(1,g.z)) >= 1
        print("Initializing Third Restriction")  
        for i in tqdm(g.edge):
            for t in range(1,(g.z)-1):
                problem += (solver.lpSum(X.get(str(k)+','+str(i.split(',')[1])+','+str(t)) for k in g.arrive(i.split(',')[1])) - (solver.lpSum(X.get(str(i.split(',')[1])+','+str(j)+','+str(t+(1)))for j in g.leave(i.split(',')[1])))-Y.get(str(i.split(',')[1])+','+str(t))) == 0
    
        print("Initializing Solver")
        st = problem.solve(solvers[solverUsado])
        tempos = open("tempos.txt","a+")
        res = ""
        if problem.status == 1:
            res = "OPTIMAL"
        else:
            res = "TL exceeded"
        tempos.writelines("PROBLEM: "+ptk.replace(".txt","") +", F.O: "+str(solver.value(problem.objective)) + ", TIME: "+str(problem.solutionTime)+ " is_Optimal: "+res+ "\n")
        tempos.close()
        values = []
        try:
            print("Getting results...")
            for k in problem.variables():
                if(solver.value(k) > 0):
                    if(k.name.split('_')[0] == 'X'):
                        values.append(k)
            valuesOr = [None for i in range(len(values))]
            for i in values:
                ind = int(i.name.split(',')[2])
                cut = i.name.split(',')[0].split('_')[1]+','+i.name.split(',')[1]
                valuesOr[ind-1] = cut
            try:
                os.makedirs("Results/"+ptk.split("/")[-1].split(".")[0])
            except:
                pass
            g.plotCuts("Results/"+ptk.split("/")[-1].split(".")[0]+"/"+ptk.split("/")[-1].replace(".txt",""))
            g.plotCor("Results/"+ptk.split("/")[-1].split(".")[0]+"/"+ptk.split("/")[-1].replace(".txt",""))
            g.plotDesloc(valuesOr,"Results/"+ptk.split("/")[-1].split(".")[0]+"/"+ptk.split("/")[-1].replace(".txt",""))
            g.plotSolution(valuesOr,"Results/"+ptk.split("/")[-1].split(".")[0]+"/"+ptk.split("/")[-1].replace(".txt",""))
        except Exception as e:
            print("Fail problem",ptk,"error",str(e))
    except Exception as e:
        res = "TL exceeded "
        tempos = open("tempos.txt","a+")
        tempos.writelines("PROBLEM: "+ptk.replace(".txt"," ") +", F.O: -1"+" TIME: 2h"+ " is_Optimal: "+res+ "\n")
        tempos.close()
        print(e)
        pass
    del problem
    del X
    del Y
    del g
    gc.collect()
