import numpy as np
import random
import math
import sys

class AntColony:
    #rho = penguapan, alpha = pangkat dari intensitas phereomone dalam probabilitas
    #beta = pangkat dari visibilitas dalam probabilitas, Q = konstanta
    rho = 0.7
    alpha = 3
    beta = 3
    Q = 2
            
    s = 0
    nc = 0
    
    #inisialisasi matriks tabulist, pheromones, delta pheromones, dan variabel-variabel yang akan digunakan
    def __init__(self, data, nants, ncmax):
        np.set_printoptions(threshold=np.nan)
        
        self.data = data
            
        self.ncmax = ncmax
        self.nants = nants+1
        self.ncities = len(data)
        
        self.ants = np.empty((self.nants, 1), dtype=np.int32)
        self.length = np.zeros((self.nants, 1))
        self.tabulist = np.zeros((self.ncmax, self.nants, self.ncities), dtype=np.int32) 
        self.pheromones = np.zeros((self.ncities, self.ncities))
        self.pheromones.fill(1)
        self.deltapheromones = np.zeros((self.ncities, self.ncities))
    
        self.shortestlength = sys.maxsize
        self.shortestroute = np.zeros((self.ncities), dtype = np.int32)
        
    #menghitung jarak dari kota a ke kota b
    def distance(self, a, b):
        return math.sqrt(pow(self.data[a][1]-self.data[b][1], 2)+pow(self.data[a][2]-self.data[b][2], 2))
    
    #mengitung delta pheromones jalur dari kota i ke kota j yang dilalui oleh semut k
    def deltapheromonesk(self, i, j, k):
        useij = False
        for x in range(0, self.ncities-1): 
            if((self.tabulist[self.nc][k][x] == i or self.tabulist[self.nc][k][x] == j)
               and ((self.tabulist[self.nc][k][x-1] == i or self.tabulist[self.nc][k][x-1] == j)
               or (self.tabulist[self.nc][k][x+1] == i or self.tabulist[self.nc][k][x+1] == j))): useij = True
        return self.Q/self.length[k] if useij else 0
    
    #menghitung panjang rute semut k
    def calculatelength(self, k):
        Lk = 0
        for x in range(0, self.ncities-2): 
            Lk += self.distance(self.tabulist[self.nc][k][x]-1, self.tabulist[self.nc][k][x+1]-1)
        Lk += self.distance(self.tabulist[self.nc][k][0]-1, self.tabulist[self.nc][k][self.ncities-1]-1)
        return Lk
    
    #mencari kota baru menggunakan rumus probabilitas
    def findnewcity(self, i, citiestovisit):
        divisor = 0
        dividend = np.zeros((len(citiestovisit)))
        cumulativeprob = 0
        #menghitung probabilitas dari setiap kota yang bisa dilaui
        for x in range(0, len(citiestovisit)):
            cumulativeprob += pow(self.pheromones[i][citiestovisit[x]-1], self.alpha)*pow((1/self.distance(i, citiestovisit[x]-1)), self.beta)
            np.put(dividend, x, cumulativeprob)
            divisor += pow(self.pheromones[i][citiestovisit[x]-1], self.alpha)*pow((1/self.distance(i, citiestovisit[x]-1)), self.beta)
        dividend = dividend/divisor
        #menggunakan teknik roulette wheel selection
        randnumber = random.random()
        return citiestovisit[np.searchsorted(dividend, randnumber)]
    
    #menhasilkan rute yang dilallui oleh semut k
    def antsroute(self, k, firstcity):
        #list kota yang harus dilalui oleh semut k
        citiestovisit = [n for n in range(1, self.ncities+1) if n != firstcity]
        #rute yang sudah dilalui oleh semut k
        visited = [firstcity]
        for i in range(1, len(citiestovisit)):
            newcity = self.findnewcity(visited[i-1]-1, citiestovisit)
            #menambahkan kota yang dihasilkan oleh fungsi findnewcity ke rute
            visited.append(newcity)
            #menghapus kota yang sudah dilalui dari list kota yang akan dilalui
            citiestovisit.remove(newcity)
        visited.append(citiestovisit[0])
        return visited
    
    #digunakan untuk memulai proses
    def searchroute(self):
        #meletakkan semut k dikota awal
        for k in range (0, self.nants):
            np.put(self.ants[k], [0], random.randint(1, self.ncities))
            
        doloop = True
        
        while doloop:
            #menggunakan fungsi antsroute untuk mengisi tabulist
            for k in range(0, self.nants):
                self.tabulist[self.nc][k] = self.antsroute(k, self.ants[k][0])
                
            #mencari rute terpendek yang dilalui oleh semua semut
            for k in range(0, self.nants):
                np.put(self.length[k], [0], self.calculatelength(k-1))
                if(self.shortestlength>self.length[k]):
                    self.shortestlength = self.length[k]
                    self.shortestroute = self.tabulist[self.nc][k]
                
            #menghitung delta peheromone dari setiap jalur
            for k in range (0, self.nants): 
                deltapheromonesij = 0
                for i in range(1, self.ncities):
                    deltapheromonesij = self.deltapheromones[i-1][i]
                    deltapheromonesij += self.deltapheromonesk(i, i+1, k)
                    #karena jalur/graph tidak berarah, maka update jalur dilakukan di dua cell
                    np.put(self.deltapheromones[i-1], [i], deltapheromonesij)
                    np.put(self.deltapheromones[i], [i-1], deltapheromonesij)
                    
            #update pheromone
            self.pheromones = self.rho*self.pheromones + self.deltapheromones
                    
            self.nc += 1
            
            #mengosongkan delta pheromone
            self.deltapheromones = np.zeros((self.ncities, self.ncities))
            
            if (self.nc >= self.ncmax):
                doloop = False
                return self.tabulist, self.shortestroute, self.shortestlength