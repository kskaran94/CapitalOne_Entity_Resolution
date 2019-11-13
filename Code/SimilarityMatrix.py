import networkx as nx
import numpy as np
from fuzzywuzzy import fuzz
import distance

# This is the Common Neighbor similarity mentioned in equation 6
def CreateCommonNeighborSim(G, k_type):
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
			for y in range(x, n_t):
				z = list(nx.common_neighbors(G, nodes[x], nodes[y]))
				D = list(G.degree(z))
				sim_x_y = sum(1/np.log([d for CN, d in D]))
				sim_t[x][y] = sim_x_y
				sim_t[y][x] = sim_x_y
		CN_sim.append(sim_t)
	return CN_sim, V


def CreateJaccardSim(G, k_type):
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
