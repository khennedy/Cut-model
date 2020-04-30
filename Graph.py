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
        plt.savefig(name+"problemImage"+".png",dpi=300)
        #plt.show()
        plt.close()
    def plotCuts(self,name):
        for i in self.edgeCuts:
            s = i.split(',')[0]
            f = i.split(',')[1]
            plt.plot([self.points[int(f)-1][0],self.points[int(s)-1][0]],[self.points[int(f)-1][1],self.points[int(s)-1][1]],'red',label='1')
        plt.savefig(name+"OnlyCuts"+".png",dpi=300)
        #plt.show()
        plt.close()
    
    def plotDesloc(self,cuts,name):
        save = []
        for i in range(len(cuts)):
            s = int(cuts[i].split(',')[0])
            f = int(cuts[i].split(',')[1])
            
            if(not cuts[i] in save and (not str(str(f)+","+str(s)) in save) and (cuts[i] in self.edgeCuts or (str(str(f)+","+str(s)) in self.edgeCuts))):
                plt.plot([self.points[int(f)-1][0],self.points[int(s)-1][0]],[self.points[int(f)-1][1],self.points[int(s)-1][1]],'red',label='1')
                plt.text((self.points[s-1][0]+self.points[f-1][0])/2,(self.points[s-1][1]+self.points[f-1][1])/2,str(i+1))
            else:
                plt.plot([self.points[int(f)-1][0],self.points[int(s)-1][0]],[self.points[int(f)-1][1],self.points[int(s)-1][1]],'blue',label='1')
                plt.text((self.points[s-1][0]+self.points[f-1][0])/2,(self.points[s-1][1]+self.points[f-1][1])/2,str(i+1))
                
            save.append(cuts[i])
            plt.savefig(name+str(i)+".png",dpi=300)
            
        #plt.show()
        plt.close()
    
    def plotSolution(self, cuts,name):
        vis = []
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
        plt.savefig(name+"solutationFinal"+".png",dpi=300)
        plt.close()
    
    def plotSolution2(self, cuts ,name):
        plot1 = plt.subplot(1,2,1)
        plot2 = plt.subplot(1,2,2)
        max_x = 0
        max_y = 0
        vis = []
        count = 1
        for i in cuts:
            s = int(i.split(',')[0])
            f = int(i.split(',')[1])
            if (not i in self.edgeCuts) or (i in vis):
                plot2.plot([self.points[int(f)-1][0],self.points[int(s)-1][0]],[self.points[int(f)-1][1],self.points[int(s)-1][1]],'red',marker='>')
                plot2.text((self.points[s-1][0]+self.points[f-1][0])/2,(self.points[s-1][1]+self.points[f-1][1])/2,str(count))
            else:
                vis.append(i)
                vis.append(i.split(',')[1]+','+i.split(',')[0])
                plot1.plot([self.points[int(f)-1][0],self.points[int(s)-1][0]],[self.points[int(f)-1][1],self.points[int(s)-1][1]],'blue',marker='>')
                plot1.text((self.points[s-1][0]+self.points[f-1][0])/2,(self.points[s-1][1]+self.points[f-1][1])/2,str(count))
            count += 1
        plot1.set_xlim(min(plot1.get_xlim()[0],plot2.get_xlim()[0]),max(plot1.get_xlim()[1],plot2.get_xlim()[1]))
        plot2.set_xlim(min(plot1.get_xlim()[0],plot2.get_xlim()[0]),max(plot1.get_xlim()[1],plot2.get_xlim()[1]))
        plot1.set_ylim(min(plot1.get_ylim()[0],plot2.get_ylim()[0]),max(plot1.get_ylim()[1],plot2.get_ylim()[1]))
        plot2.set_ylim(min(plot1.get_ylim()[0],plot2.get_ylim()[0]),max(plot1.get_ylim()[1],plot2.get_ylim()[1]))
        
        #plt.show()
        plt.savefig(name+"solutationFinal"+".png",dpi=300)
        plt.close()
    def plotSolution3(self, cuts ,name, fo):
        plt.figure()
        vis = []
        count = 1
        add_x = max(self.points)[0]*0.05
        add_y = max(self.points)[1]*0.05
        for i in cuts:
            s = int(i.split(',')[0])
            f = int(i.split(',')[1])
            if (not i in self.edgeCuts) or (i in vis):
                if i in vis:
                    if self.points[int(s)-1][0] == self.points[int(f)-1][0]:
                        qv_d = plt.quiver(self.points[int(s)-1][0]+add_x,self.points[int(s)-1][1],self.points[int(f)-1][0]-self.points[int(s)-1][0],(self.points[int(f)-1][1])-self.points[int(s)-1][1], scale_units='xy', angles='xy', scale=1,color='red')
                        plt.text((self.points[s-1][0]+self.points[f-1][0])/2+add_x,(self.points[s-1][1]+self.points[f-1][1])/2,str(count))
                
                    elif self.points[int(s)-1][1] == self.points[int(f)-1][1]:
                        qv_d = plt.quiver(self.points[int(s)-1][0],self.points[int(s)-1][1]+add_y,self.points[int(f)-1][0]-self.points[int(s)-1][0],(self.points[int(f)-1][1])-self.points[int(s)-1][1], scale_units='xy', angles='xy', scale=1,color='red')
                        plt.text((self.points[s-1][0]+self.points[f-1][0])/2,(self.points[s-1][1]+self.points[f-1][1])/2+add_y,str(count))
                    else:
                        qv_d = plt.quiver(self.points[int(s)-1][0]+add_x,self.points[int(s)-1][1]+add_y,self.points[int(f)-1][0]-self.points[int(s)-1][0],(self.points[int(f)-1][1])-self.points[int(s)-1][1], scale_units='xy', angles='xy', scale=1,color='red')
                        plt.text((self.points[s-1][0]+self.points[f-1][0])/2+add_x,(self.points[s-1][1]+self.points[f-1][1])/2+add_y,str(count))
                    
                else:
                    qv_d = plt.quiver(self.points[int(s)-1][0],self.points[int(s)-1][1],self.points[int(f)-1][0]-self.points[int(s)-1][0],self.points[int(f)-1][1]-self.points[int(s)-1][1], scale_units='xy', angles='xy', scale=1,color='red')
                    plt.text((self.points[s-1][0]+self.points[f-1][0])/2,(self.points[s-1][1]+self.points[f-1][1])/2,str(count))
                    
            else:
                vis.append(i)
                vis.append(i.split(',')[1]+','+i.split(',')[0])
                qv_c = plt.quiver(self.points[int(s)-1][0],self.points[int(s)-1][1],self.points[int(f)-1][0]-self.points[int(s)-1][0],self.points[int(f)-1][1]-self.points[int(s)-1][1], scale_units='xy', angles='xy', scale=1,color='blue')
                plt.text((self.points[s-1][0]+self.points[f-1][0])/2,(self.points[s-1][1]+self.points[f-1][1])/2,str(count))
            count += 1
        #plt.xlim(0,250)
        #plt.ylim(0,250)
        #plt.show()
        plt.quiverkey(qv_d,(plt.xlim()[1]//2)-(plt.xlim()[1]//2)*.5, plt.ylim()[1]+plt.ylim()[1]*.05,150, 'Moves', coordinates='data')
        plt.quiverkey(qv_c,(plt.xlim()[1]//2)+(plt.xlim()[1]//2)*.5, plt.ylim()[1]+plt.ylim()[1]*.05, 150, 'Cut', coordinates='data')
        plt.text((plt.xlim()[1]//2)-(plt.xlim()[1]//2)*.35, plt.ylim()[1]+plt.ylim()[1]*.05,"Time Required: {:.2f}".format(fo))
            
        #plt.ylim(plt.ylim()[0],plt.ylim()[1]+60)
        plt.savefig(name+"solutationFinalAdd"+".png",dpi=300)
        plt.close()
    
    def euclidianDistance(self, p1, p2):
        return max(abs(p1[0]-p2[0]),abs(p1[1]-p2[1]))
        #return (((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2))**(1/2)
    
    
    
    
    
    
    
    