import antcolony
import time

if __name__ == '__main__':
    start_time = time.time()
    aco = antcolony.AntColony('data/Swarm052.txt', 8, 10)
    aco.searchroute()
    print("--- %s seconds ---" % (time.time() - start_time))