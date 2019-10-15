import networkx as nx
import numpy as np

def InitializeMapping(sim, p):
	C = []
	for i in range(len(sim)):
		C_t = np.zeros((sim[i].shape[0], p[i]))
		for j in range(sim[i].shape[0]):
			C_t[j, np.random.randint(low = 0, high = p[i])] = 1
			C.append(C_t)
	return C