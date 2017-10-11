import antcolony
import time
import numpy as np

if __name__ == '__main__':
    start_time = time.time()
    data = np.loadtxt('data/Swarm016.txt')
    ncmax = 5
    nants = 5
    
    aco = antcolony.AntColony(data, nants, ncmax)
    
    tabulist, shortestroute, shortestlength = aco.searchroute()
    
    print('Shortest route \t\t= ', shortestroute)
    print('Length of the route \t= ', shortestlength)
                              
    print("--- %s seconds ---" % (time.time() - start_time))