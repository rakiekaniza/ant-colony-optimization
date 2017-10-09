import antcolony
import time

if __name__ == '__main__':
    start_time = time.time()
    aco = antcolony.AntColony('data/Swarm202.txt', 20, 8)
    aco.searchroute()
    print("--- %s seconds ---" % (time.time() - start_time))