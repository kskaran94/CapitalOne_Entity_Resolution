import networkx as nx
import numpy as np
from fuzzywuzzy import fuzz
import distance

# This is the Common Neighbor similarity mentioned in equation 6 of the paper
def CreateCommonNeighborSim(G, k_type):
	CN_sim = []
	V = []
	for i in k_type:
		# to maintain the order of nodes, so that nodes in similarity matrix can be mapped
		temp = {'order':{}, 'name':{}, 'position':{}}

		# extract the node values
		nodes = [x for x,y in G.nodes(data=True) if y['t'] == i]
		temp['order'] = nodes
		for x in range(len(nodes)):
			temp['name'][x] = nodes[x]
			temp['position'][nodes[x]] = x

		V.append(temp)
		n_t = len(nodes)

		# Similarity between the t-type nodes
		sim_t = np.zeros((n_t, n_t))

		for x in range(n_t):
			for y in range(x, n_t):
				# Get the common neighbors of the two nodes in a graph
				z = list(nx.common_neighbors(G, nodes[x], nodes[y]))

				# Find the degree of each neighbors
				D = list(G.degree(z))

				# Implementation of similarity equation 6
				sim_x_y = sum(1/np.log([d for CN, d in D]))
				sim_t[x][y] = sim_x_y
				sim_t[y][x] = sim_x_y

		# CN_sim has similarity matrices for all the k-type nodes	
		CN_sim.append(sim_t)
	return CN_sim, V


# Implementation of Jaccard Similarity - (only similarity function changed)
def CreateCommonNeighborSimJaccard(G, k_type):
    CN_sim = []
    V = []
    for i in k_type:
        temp = {'order':{}, 'name':{}, 'position':{}}
        nodes = [x for x,y in G.nodes(data=True) if y['t'] == i]
        temp['order'] = nodes
        for x in range(len(nodes)):
            temp['name'][x] = nodes[x]
            temp['position'][nodes[x]] = x
        V.append(temp)
        n_t = len(nodes)
        sim_t = np.zeros((n_t, n_t))
        for x in range(n_t):
            for y in range(n_t):
                sim_t[x][y] = distance.jaccard(nodes[x], nodes[y])
        CN_sim.append(sim_t)
    return CN_sim, V


# This is a type of string similarity - Do not run this, very high execution time (has to be optimized)
def CreateLevenshteinSim(G, k_type):
	L_sim = []
	V = []
	for i in k_type:
		nodes = [x for x,y in G.nodes(data=True) if y['t'] == i]
		V.append(nodes)
		n_t = len(nodes)
		sim_t = np.zeros((n_t, n_t))
		for x in range(n_t):
			for y in range(x, n_t):
				sim_x_y = fuzz.ratio(nodes[x], nodes[y])
				sim_t[x][y] = sim_x_y
				sim_t[y][x] = sim_x_y
		L_sim.append(sim_t)
	return L_sim, V
