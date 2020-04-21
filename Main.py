import pulp as solver
from pulp import *
import Graph
import time

z = 0
solvers = [solver.CPLEX(), solver.GLPK(), solver.GUROBI(), solver.PULP_CBC_CMD(), solver.COIN()]
solverUsado = 0
listaProblemas = ["instance_01_5pol.txt"]
for ptk in listaProblemas:
    g = Graph.Graph(5,1,z)
    g.initProblem(ptk)
    g.z = len(g.edgeCuts)*2
    var = [(i+','+str(t)) for i in g.edge for t in range(1,g.z)]
    var2 = [(str(i)+','+str(t)) for i in g.vertices for t in range(1,g.z)]
    X = solver.LpVariable.dicts("X",var,cat=solver.LpBinary)
    Y = solver.LpVariable.dicts("Y",var2,cat=solver.LpBinary)
    problem = solver.LpProblem("The best Cut" , solver.LpMinimize)
        
    problem += (solver.lpSum(X.get(str(i.split(',')[0])+','+str(i.split(',')[1])+','+str(t))*g.mis[i.split(',')[0]][i.split(',')[1]] for i in g.edge for t in range(1,g.z)) + 
                    solver.lpSum(((g.pis[k.split(',')[0]][k.split(',')[1]]))-(
                                       (g.mis[k.split(',')[0]][k.split(',')[1]])) for k in g.edgeCuts)/2)+solver.lpSum(X.get(str(i.split(',')[0])+','+str(i.split(',')[1])+','+str(1))*g.initDes[int(i.split(',')[0])-1] for i in g.edge)
    for t in range(1,g.z):
        problem += solver.lpSum(X.get(str(i.split(',')[0])+','+str(i.split(',')[1])+','+str(t)) for i in g.edge) <= 1
       
    for i in g.edgeCuts:
        problem += solver.lpSum(X.get(str(i.split(',')[0])+','+str(i.split(',')[1])+','+str(t))+X.get(str(i.split(',')[1])+','+str(i.split(',')[0])+','+str(t)) for t in range(1,g.z)) >= 1
        
    for i in g.edge:
        for t in range(1,(g.z)-1):
            problem += (solver.lpSum(X.get(str(k)+','+str(i.split(',')[1])+','+str(t)) for k in g.arrive(i.split(',')[1])) - (solver.lpSum(X.get(str(i.split(',')[1])+','+str(j)+','+str(t+(1)))for j in g.leave(i.split(',')[1])))-Y.get(str(i.split(',')[1])+','+str(t))) == 0
    timeIn = time.time()
    problem.writeLP(ptk.replace(".txt",".lp"))
    #sCplex = solver.CPLEX()
    #solver.GLPK()
    st = problem.solve(solvers[solverUsado])
    tempos = open("tempos.txt","a+")
    tempos.writelines("PROBLEM ===== "+ptk.replace(".txt","") +" --- F.O ===== "+str(solver.value(problem.objective)) + "   ----     TIME  ===== "+str(problem.solutionTime)+"\n")
    tempos.close()
    values = []
    for k in problem.variables():
        if(solver.value(k) > 0):
            if(k.name.split('_')[0] == 'X'):
                values.append(k)
    valuesOr = [None for i in range(len(values))]
    
    for i in values:
        ind = int(i.name.split(',')[2])
        cut = i.name.split(',')[0].split('_')[1]+','+i.name.split(',')[1]
        valuesOr[ind-1] = cut
    for i in valuesOr:
        print(i)
    g.plotSoluation(valuesOr,ptk.replace(".txt",""))
    g.plotCuts(ptk.replace(".txt",""))
    g.plotCor(ptk.replace(".txt",""))
    g.plotDesloc(valuesOr,ptk.replace(".txt",""))
    print("VALUE OF F.O = ",solver.value(problem.objective))
