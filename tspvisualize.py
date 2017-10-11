import antcolony
import time
import tspgraph
import numpy as np

if __name__ == '__main__':
    start_time = time.time()
    data = np.loadtxt('data/Swarm052.txt')
    ncmax = 50
    nants = 8
    
    aco = antcolony.AntColony(data, nants, ncmax)
    
    points = []
    
    tabulist, shortestroute, shortestlength = aco.searchroute()
    
    for i in range(0, len(data)):
        points.append((data[i][1], data[i][2]))
    graph = tspgraph.TSPGraph(tabulist, points, nants, ncmax)
                              
    print("--- %s seconds ---" % (time.time() - start_time))