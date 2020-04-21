import random as rd

quant_p = rd.randint(5,10)
quant_l = rd.randint(10,20)

arq = open("doi.txt",'w')
p = []
e = []
for i in range(quant_p):
    p.append((rd.randint(1,50),rd.randint(1,50)))
for i in range(quant_l):
    n1 = rd.randint(1,quant_p)
    n2 = rd.randint(1,quant_p)
    while n1 == n2:
        n1 = rd.randint(1,quant_p)
        n2 = rd.randint(1,quant_p)
    e.append((n1,n2))

s = str(quant_p)+" "+str(quant_l)+'\n'
arq.write(s)

for i in p:
    s = str(str(i[0])+","+str(i[1])+"\n")
    arq.write(s)
for i in e:
    s = str(str(i[0])+"-"+str(i[1])+" nc\n")
    arq.write(s)
    
    
arq.close()
