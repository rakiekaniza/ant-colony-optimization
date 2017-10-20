import antcolony
import time
import numpy as np

if __name__ == '__main__':
    start_time = time.time()
    data = np.loadtxt('data/Swarm202.txt')
    ncmax = 10
    nants = 40
    
    aco = antcolony.AntColony(data, nants, ncmax)
    
    tabulist, shortestroute, shortestlength = aco.searchroute()
    
    print('Shortest route \t\t= ', shortestroute)
    print('Length of the route \t= ', shortestlength)
#    print(aco.calculatelk(shortestroute))
                              
    print("--- %s seconds ---" % (time.time() - start_time))