import numpy as np
import random
import math
import sys

class AntColony:
    rho = 0.8
    alpha = 2
    beta = 2
    Q = 1
            
    s = 0
    nc = 0
    def __init__(self, data, nants, ncmax):
        np.set_printoptions(threshold=np.nan)
        
        self.data = np.loadtxt(data)
            
        self.ncmax = ncmax
        self.nants = nants+1
        self.ncities = len(self.data)
        
        self.ants = np.empty((self.nants, 1), dtype=np.int32)
        self.lengthk = np.zeros((self.nants, 1))
        self.tabulist = np.zeros((self.nants, self.ncities), dtype=np.int32) 
        self.pheromones = np.zeros((self.ncities, self.ncities))
        self.pheromones.fill(1)
        self.deltapheromones = np.zeros((self.ncities, self.ncities))
    
        self.shortestlength = sys.maxsize
        self.shortestroute = np.zeros((self.ncities), dtype = np.int32)
        
    def distance(self, a, b):
        return math.sqrt(pow(self.data[a][1]-self.data[b][1], 2)+pow(self.data[a][2]-self.data[b][2], 2))
    
    def deltapheromonesk(self, i, j, k):
        useij = False
        for x in range(0, self.ncities-1): 
            if((self.tabulist[k][x] == i or self.tabulist[k][x] == j)
               and ((self.tabulist[k][x-1] == i or self.tabulist[k][x-1] == j)
               or (self.tabulist[k][x+1] == i or self.tabulist[k][x+1] == j))): useij = True
        return self.Q/self.calculatelength(k) if useij else 0
    
    def calculatelength(self, k):
        Lk = 0
        for x in range(0, self.ncities-2): 
            Lk += self.distance(self.tabulist[k][x]-1, self.tabulist[k][x+1]-1)
        Lk += self.distance(self.tabulist[k][0]-1, self.tabulist[k][self.ncities-1]-1)
        return Lk
    
    def findnewcity(self, i, citiestovisit):
        divisor = 0
        dividend = np.zeros((len(citiestovisit)))
        cumulativeprob = 0
        for x in range(0, len(citiestovisit)):
            cumulativeprob += pow(self.pheromones[i][citiestovisit[x]-1], self.alpha)*pow((1/self.distance(i, citiestovisit[x]-1)), self.beta)
            np.put(dividend, x, cumulativeprob)
            divisor += pow(self.pheromones[i][citiestovisit[x]-1], self.alpha)*pow((1/self.distance(i, citiestovisit[x]-1)), self.beta)
        dividend = dividend/divisor
        randnumber = random.random()
        return citiestovisit[(np.abs(dividend-randnumber)).argmin()]
    
    def antsroute(self, k, firstcity):
        citiestovisit = [n for n in range(1, self.ncities+1) if n != firstcity]
        visited = [firstcity]
        s = 0
        np.put(self.tabulist[k], [0], self.ants[k][0])
        for i in range(1, len(citiestovisit)):
            s += 1
            newcity = self.findnewcity(visited[i-1]-1, citiestovisit)
            visited.append(newcity)
            citiestovisit.remove(newcity)
        visited.append(citiestovisit[0])
        return visited
    
    def searchroute(self):
        for k in range (0, self.nants):
            np.put(self.ants[k], [0], random.randint(1, self.ncities))
            
        doloop = True
        
        while doloop:
            for k in range(0, self.nants):
                self.tabulist[k] = self.antsroute(k, self.ants[k][0])
            for k in range(0, self.nants):
                np.put(self.lengthk[k], [0], self.calculatelength(k-1))
                if(self.shortestlength>self.lengthk[k]):
                    self.shortestlength = self.lengthk[k]
                    self.shortestroute = self.tabulist[k]
            for k in range (0, self.nants): 
                deltapheromonesij = 0
                for i in range(1, self.ncities):
                    deltapheromonesij = self.deltapheromones[i-1][i]
                    deltapheromonesij += self.deltapheromonesk(i, i+1, k)
                    np.put(self.deltapheromones[i-1], [i], deltapheromonesij)
                    np.put(self.deltapheromones[i], [i-1], deltapheromonesij)
                    
            self.pheromones = self.rho*self.pheromones + self.deltapheromones
                    
            self.nc += 1
            
            self.deltapheromones = np.zeros((self.ncities, self.ncities))
            
            if (self.nc < self.ncmax):
                self.tabulist = np.zeros((self.nants, self.ncities), dtype=np.int32) 
            else:
                print('Shortest route \t\t= ', self.shortestroute)
                print('Length of the route \t= ', self.shortestlength)
                doloop = False
