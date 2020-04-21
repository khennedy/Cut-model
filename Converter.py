import os
for k in os.listdir("SBPO/separated"):
    arq = open("SBPO/separated/"+k,'r')
    q = int(arq.readline())
    
    points = []
    edges = []
    edgesNotCut = []
    def findPoint(point, points):
        for i in range(len(points)):
            if(points[i] == point):
                return i+1
            
    for i in range(q):
        l = arq.readline()
        l = l.split(" ")
        p1 = l[0] +" "+ l[1]
        
        p2 = l[2] +" "+ l[3].split("\n")[0]
        
        if(not p1 in points):
            print("PI = ",p1)
            points.append(p1)
        if(not p2 in points):
            points.append(p2)
            print("P2 = ",p2)
        edge = str(findPoint(p1,points)) + "-" + str(findPoint(p2,points))
        if(not edge in edges):
        	edges.append(edge)
    add = []
    for i in range(len(edges)):
        p1 = edges[i].split("-")[0]
        p2 = edges[i].split("-")[1]
        if(not p2+"-"+p1 in edges):
            add.append(p2+"-"+p1)
    for i in add:
        edges.append(i)
    arq.close()
    arq = open("Instancias/"+k,'a+')
    for i in range(1,len(points)+1):
        for j in range(1,len(points)+1):
            bol = True
            if(i != j):
                for k in edges:
                    if(str(i)+"-"+str(j) == k):
                        bol = False
                        break
                if(bol):
                    edgesNotCut.append(str(i)+"-"+str(j))
    
    f = str(len(points)) + " "+ str(len(edges)+len(edgesNotCut)) + "\n"
    arq.write(f)
    for i in points:
        x = i.split(" ")
        if(len(x[1].split('\n')) == 2):
            arq.write(x[0]+","+x[1])
        else:
            arq.write(x[0]+","+x[1]+"\n")
            
    for i in edges:
        arq.write(i+" c"+"\n")
    for i in edgesNotCut:
        arq.write(i+" nc"+"\n")
    
    arq.close()
