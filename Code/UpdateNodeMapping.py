import networkx as nx
import numpy as np

def UpdateC(G, V, C, L, sim, D):
	for i in range(len(C)):
		C_t = C[i]
		D_t = D[i]
		sum1 = np.zeros(C_t.shape)
		sum2 = np.zeros(C_t.shape)
		for j in range(i+1, len(C)):
			C_t_dash = C[j]
			subgraph = G.subgraph(V[i][order] + V[j][order])
			G_t_t_dash = np.zeros((len(V[i]['order']), len(V[j]['order'])))
			for edge in subgraph.edges():
				G_t_t_dash[V[i]['position'][edge[0]], V[j]['position'][edge[1]]] = 1
			L_t_t_dash = L[i][j]['mat']
			temp1 = np.matmul(C_t_dash, L_t_t_dash.transpose())
			sum1 += np.matmul(G_t_t_dash, temp1)
			sum2 += np.matmul(C_t, np.matmul(L_t_t_dash, np.matmul(C_t_dash, temp1)))
		sum1 += np.matmul(sim[i], C_t)
		sum2 += np.matmul(D_t, C_t)
		C[i] = np.multiply(C_t, np.sqrt(np.divide(sum1, sum2)))
	return C

def UpdateL(G, V, C, L):
	for i in range(len(C)):
		C_t = C[i]
		for j in range(i+1, len(C)):
			L_t_t_dash = L[i][j]['mat']
			C_t_dash = C[j]
			subgraph = G.subgraph(V[i][order] + V[j][order])
			G_t_t_dash = np.zeros((len(V[i]['order']), len(V[j]['order'])))
			for edge in subgraph.edges():
				G_t_t_dash[V[i]['position'][edge[0]], V[j]['position'][edge[1]]] = 1
			temp1 = np.matmul(C_t.transpose(), np.matmul(G_t_t_dash, C_t_dash))
			temp2 = np.matmul(L_t_t_dash, np.matmul(C_t_dash.transpose(), C_t_dash))
			temp3 = np.matmul(C_t.transpose(), np.matmul(C_t, temp2))
			L[i][j]['mat'] = np.multiply(L_t_t_dash, np.sqrt(np.divide(temp1, temp3)))
	return L