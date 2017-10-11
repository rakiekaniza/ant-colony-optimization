import matplotlib.pyplot as plt
import numpy as np

class TSPGraph:
    def __init__(self, paths, points, nants, ncmax=1):
#        plt.subplots_adjust(left=0.1, bottom=0.25)
        
        self.paths = paths
        self.points = points
        self.ncmax = ncmax
        self.nants = nants
        self.nc = 0
        
        self.x = []
        self.y = []
        
        
        for i in range (0, len(self.points)):
            self.x.append(self.points[i][0])
            self.y.append(self.points[i][1])
            
        self.animateACO()
    
        plt.xlim(min(self.x)-3, max(self.x)+3)
        plt.ylim(min(self.y)-3, max(self.y)+3)
        plt.show()
        
    def plotTSP(self):
        self.fig = plt.figure()
        plt.close()
        plt.clf()
        plt.plot(self.x, self.y, 'co')
        widtharrow = np.zeros((len(self.points), len(self.points)))
        for i in range(0, self.nants):
            xi = [self.points[self.paths[self.nc][i][j]-1][0] for j in range(0, len(self.points))]
            yi = [self.points[self.paths[self.nc][i][j]-1][1] for j in range(0, len(self.points))]
            
            widtharrow[self.paths[self.nc][i][-1]-1][self.paths[self.nc][i][0]-1] += 0.4/float(self.ncmax)
            widtharrow[self.paths[self.nc][i][0]-1][self.paths[self.nc][i][-1]-1] += 0.4/float(self.ncmax)
            
            plt.arrow(xi[-1], yi[-1], (xi[0] - xi[-1]), (yi[0] - yi[-1]), color = 'r', 
            length_includes_head = True, width = widtharrow[-1][0], head_width = 0)
            
            for n in range(0, len(self.x) - 1):
                widtharrow[self.paths[self.nc][i][n]-1][self.paths[self.nc][i][n+1]-1] += 0.4/float(self.ncmax)
                widtharrow[self.paths[self.nc][i][n+1]-1][self.paths[self.nc][i][n]-1] += 0.4/float(self.ncmax)
                plt.arrow(xi[n], yi[n], (xi[n+1] - xi[n]), (yi[n+1] - yi[n]),
                          color = 'r', length_includes_head = True, width = widtharrow[n][n+1], head_width = 0)
        plt.title('Cycle '+str(self.nc+1))
        plt.draw()
        plt.pause(0.5)
                
    def animateACO(self):
        while(True):
            self.plotTSP()
            if(self.nc < self.ncmax-1):
                self.nc += 1
            else:
                self.nc = 0