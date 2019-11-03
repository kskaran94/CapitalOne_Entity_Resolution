import networkx as nx
import numpy as np
import copy

def InitializeMapping(sim, p):
	C = []
	for i in range(len(sim)):
		C_t = np.zeros((sim[i].shape[0], p[i]))
		for j in range(sim[i].shape[0]):
			C_t[j, np.random.randint(low = 0, high = p[i])] = 1
			C.append(C_t)
	return C

def CreateSummaryGraph(G, C, V, k_type):
	SG = copy.deepcopy(G)
	S = []
	for i in range(len(C)):
		S_t = {'order':[], 'name':{}, 'position':{}}
		for p in range(C[i].shape[1]):
			C_t = C[i]
			merge_nodes = np.argwhere(C_t[:,p] == 1)
			merge_nodes = merge_nodes.reshape((merge_nodes.shape[0],))
			S_t['order'].append(V[i][merge_nodes[0]])
			S_t['name'][merge_nodes[0]] = V[i][merge_nodes[0]]
			S_t['position'][V[i][merge_nodes[0]]] = merge_nodes[0]
			S_t[merge_nodes[0]] = merge_nodes
			for j in range(1,len(merge_nodes)):
				SG = nx.contracted_nodes(SG, V[i][merge_nodes[0]], V[i][merge_nodes[j]])
		S.append(S_t)
	L = {}
	for i in range(len(S)):
		temp = {}
		for j in range(i+1, len(S)):
			L_t_t_dash = {'name_0':{}, 'position_0':{}, 'name_1':{}, 'position_1':{}}
			S_t = S[i]
			S_t_dash = S[j]
			for x in range(len(S_t['order'])):
				L_t_t_dash['name_0'][x] = S_t['order'][x]
				L_t_t_dash['position_0'][S_t['order'][x]] = x
			for x in range(len(S_t_dash['order'])):
				L_t_t_dash['name_1'][x] = S_t_dash['order'][x]
				L_t_t_dash['position_1'][S_t_dash['order'][x]] = x
			mat = np.zeros((len(S_t['order']), len(S_t_dash['order'])))
			subgraph = SG.subgraph(S_t['order'] + S_t_dash['order'])
			for edge in subgraph.edges():
				mat[L_t_t_dash['position_0'][edge[0]], L_t_t_dash['position_1'][edge[1]]] = 1
			L_t_t_dash['mat'] = mat
			temp[j] = L_t_t_dash
		L[i] = temp
	return SG, S, L

C = InitializeMapping(CN_sim, [2, 5])
SG, S, L = CreateSummaryGraph(G, C, V, k_type)