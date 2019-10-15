import networkx as nx
import numpy as np

def InitializeMapping(n_t, p):
	return np.random.randint(low = 0, high = 2, size = (n_t, p))