import distance
import networkx as nx
import numpy as np
import time

class KTypeVertex:
    def __init__(self):
        self.count = 0
        self.nodes = []
        self.name = {}
        self.position = {}

# Implementation of Jaccard Similarity
def createJaccardSim(graph, k_type):
    CN_sim = []
    V = []
    for type_i in k_type:
        # to maintain the order of nodes, so that nodes in similarity matrix can be mapped
        temp = {'nodes':[], 'name':{}, 'position':{}}
        type_i_vertex = KTypeVertex()
        # extract the node values
        nodes = [node_label for node_label, node_attr in graph.G.nodes(data=True) if node_attr['type'] == type_i]
        type_i_vertex.nodes = nodes
        type_i_vertex.count = len(nodes)

        for index, node_label in enumerate(nodes):
            type_i_vertex.name[index] = node_label
            type_i_vertex.position[node_label] = index
            
        V.append(type_i_vertex)
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