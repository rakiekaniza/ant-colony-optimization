import antcolony
import time
import tspgraph
import numpy as np

if __name__ == '__main__':
    start_time = time.time()
    data = np.loadtxt('data/Swarm202.txt')
    ncmax = 40
    nants = 40
    
    aco = antcolony.AntColony(data, nants, ncmax)
    
    points = []
    
    tabulist, shortestroute, shortestlength = aco.searchroute()
    
    for i in range(0, len(data)):
        points.append((data[i][1], data[i][2]))
    graph = tspgraph.TSPGraph(tabulist, points, nants, ncmax)
                              
    print("--- %s seconds ---" % (time.time() - start_time))