import networkx as nx
import numpy as np
import distance
import time

# Implementation of Jaccard Similarity
def createJaccardSim(G, k_type):
    CN_sim = []
    V = []
    for i in k_type:
        # to maintain the order of nodes, so that nodes in similarity matrix can be mapped
        temp = {'nodes':[], 'name':{}, 'position':{}}
        
        # extract the node values
        nodes = [x for x,y in G.nodes(data=True) if y['t'] == i]
        temp['nodes'] = nodes
        for x in range(len(nodes)):
            temp['name'][x] = nodes[x]
            temp['position'][nodes[x]] = x
        V.append(temp)
        n_t = len(nodes)
        
        # Similarity between the t-type nodes
        sim_t = np.zeros((n_t, n_t))
        for x in range(n_t):
            for y in range(n_t):
                sim_t[x][y] = 1 - distance.jaccard(nodes[x], nodes[y])
        
        # CN_sim has similarity matrices for all the k-type nodes	
        CN_sim.append(sim_t)
    return CN_sim, V


# start_time = time.time()
# CN_sim, V = createJaccardSim(G, k_type)
# print("Time taken to create similarity matrix:", (time.time()-start_time)/60)