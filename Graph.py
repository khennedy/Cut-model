import matplotlib.pyplot as plt
class Graph():
    def __init__(self,mi, pi, z):
        self.vertice = dict()
        self.edge = [] # All edges of graph
        self.edgeCuts = [] # Only edges to cut
        self.points = [] # The points in cartesiane plane
        self.distance = dict() # Distance between the points
        self.z = z # upper bound of the amount of movements
        self.mi = mi #Velocity of Deslocate
        self.pi = pi #Velocity of Cut
        self.mis = dict() # Relation between distance of point and velocity deslocate
        self.pis = dict() #Relation between distance of point and velocity cut
        self.initDes = []
    def initProblem(self, file):
        arq = open(file,'r')
        l = arq.readline()
        p = int(l.split(" ")[0])
        ed = int(l.split(" ")[1].split('\n')[0])
        self.vertices = [i for i in range(1,p+1)]
        for i in range(p):
            l = arq.readline()
            n1 = float(l.split(',')[0])
            n2 = float(l.split(',')[1].split('\n')[0])
            
            self.points.append((n1,n2))
        for i in range(ed):
            l = arq.readline()
            n1 = int(l.split('-')[0])
            n2 = int(l.split('-')[1].split(' ')[0])
            w = l.split('-')[1].split(' ')[1].split('\n')[0]
            if(w == 'c'):
                self.edgeCuts.append(str(n1)+","+str(n2))
            self.edge.append(str(n1)+","+str(n2))
        self.calculateDistances()
        arq.close()

    def calculateDistances(self):
        for i in self.edge:
            s = i.split(',')[0]
            f = i.split(',')[1]
            self.distance[s] = {}
            self.mis[s] = {}
            self.pis[s] = {}
        for i in self.edge:
            s = i.split(',')[0]
            f = i.split(',')[1]
            self.distance[s].update({f:self.euclidianDistance(self.points[int(s)-1],self.points[int(f)-1])})
            self.mis[s].update({f:(self.distance[s][f]/self.mi)})
            self.pis[s].update({f:(self.distance[s][f]/self.pi)})
        for i in range(1,len(self.vertices)+1):
            self.initDes.append(self.euclidianDistance([0,0],self.points[i-1]))
    def leave(self, x):
        l = []
        for i in self.edge:
            s = i.split(',')[0]
            if(x == s):
                f = i.split(',')[1]
                l.append(f)
        return l
    def arrive(self, x):
        l = []
        for i in self.edge:
            s = i.split(',')[1]
            if(x == s):
                f = i.split(',')[0]
                l.append(f)
        return l
    

    def plot(self, p, e):
        for i in e:
            s = i.split(',')[0]
            f = i.split(',')[1]
            plt.plot([p[int(f)-1][0],p[int(s)-1][0]],[p[int(f)-1][1],p[int(s)-1][1]])
        plt.show()
        plt.close()
    def plotCor(self,name):
        for i in self.edge:
            s = i.split(',')[0]
            f = i.split(',')[1]
            if(not i in self.edgeCuts):
                plt.plot([self.points[int(f)-1][0],self.points[int(s)-1][0]],[self.points[int(f)-1][1],self.points[int(s)-1][1]],'blue')
                plt.text(self.points[int(s)-1][0],self.points[int(s)-1][1],s)
        for i in self.edgeCuts:
            s = i.split(',')[0]
            f = i.split(',')[1]
            plt.plot([self.points[int(f)-1][0],self.points[int(s)-1][0]],[self.points[int(f)-1][1],self.points[int(s)-1][1]],'red',label='1')
        plt.savefig(name+"problemImage"+".jpg")
        #plt.show()
        plt.close()
    def plotCuts(self,name):
        for i in self.edgeCuts:
            s = i.split(',')[0]
            f = i.split(',')[1]
            plt.plot([self.points[int(f)-1][0],self.points[int(s)-1][0]],[self.points[int(f)-1][1],self.points[int(s)-1][1]],'red',label='1')
        plt.savefig(name+"OnlyCuts"+".jpg")
        #plt.show()
        plt.close()
    
    def plotDesloc(self,cuts,name):
        save = []
        for i in range(len(cuts)):
            s = int(cuts[i].split(',')[0])
            f = int(cuts[i].split(',')[1])
            
            if(not cuts[i] in save and (not str(str(f)+","+str(s)) in save)):
                plt.plot([self.points[int(f)-1][0],self.points[int(s)-1][0]],[self.points[int(f)-1][1],self.points[int(s)-1][1]],'red',label='1')
                plt.text((self.points[s-1][0]+self.points[f-1][0])/2,(self.points[s-1][1]+self.points[f-1][1])/2,str(i+1))
            else:
                plt.plot([self.points[int(f)-1][0],self.points[int(s)-1][0]],[self.points[int(f)-1][1],self.points[int(s)-1][1]],'blue',label='1')
                plt.text((self.points[s-1][0]+self.points[f-1][0])/2,(self.points[s-1][1]+self.points[f-1][1])/2,str(i+1))
                
            save.append(cuts[i])
            plt.savefig(name+str(i)+".jpg")
            
        #plt.show()
        plt.close()
    
    def plotSoluation(self, cuts,name):
        for i in self.edge:
            s = i.split(',')[0]
            f = i.split(',')[1]
            if(not i in self.edgeCuts):
                plt.plot([self.points[int(f)-1][0],self.points[int(s)-1][0]],[self.points[int(f)-1][1],self.points[int(s)-1][1]],'blue')
                plt.text(self.points[int(s)-1][0],self.points[int(s)-1][1],s)
        for i in self.edgeCuts:
            s = i.split(',')[0]
            f = i.split(',')[1]
            plt.plot([self.points[int(f)-1][0],self.points[int(s)-1][0]],[self.points[int(f)-1][1],self.points[int(s)-1][1]],'red',label='1')
        for i in range(len(cuts)):
            s = int(cuts[i].split(',')[0])
            f = int(cuts[i].split(',')[1])
            
            plt.text((self.points[s-1][0]+self.points[f-1][0])/2,(self.points[s-1][1]+self.points[f-1][1])/2,str(i+1))
        #plt.show()
        plt.savefig(name+"solutationFinal"+".jpg")
        plt.close()
    
    def euclidianDistance(self, p1, p2):
        return (((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2))**(1/2)
    
    
    
    
    
    
    
    