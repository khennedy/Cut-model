arq = open("instance_01_3pola.txt",'r')

l = arq.readline()
v = int(l.split(" ")[0])
q = int(l.split(" ")[1].split("\n")[0])
for i in range(v):
    arq.readline()
edges = []
for i in range(q):
    ed = arq.readline().split("\n")[0].split("c")[0]
    edges.append(ed)

arq.close()
edgesN = []

for i in range(1,v+1):
    for j in range(1,v+1):
        if(i != j):
            ed = str(i)+"-"+str(j)+" nc\n"
            edV = str(i)+"-"+str(j)+" "
            if(not edV in edges):
                edgesN.append(ed)

arq = open("instance_01_3polaC.txt","a+")
for i in edgesN:
    arq.write(i)
arq.close()
print(len(edges)+len(edgesN))
