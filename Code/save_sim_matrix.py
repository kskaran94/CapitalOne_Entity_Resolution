import pickle
from SimilarityMatrix import CreateCommonNeighborSimJaccard

CN_sim, V = CreateCommonNeighborSimJaccard(G, k_type)
with open("sim_matrix.pickle", 'wb') as f:
    pickle.dump([CN_sim,V], f)
