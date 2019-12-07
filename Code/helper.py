import distance
import networkx as nx
import numpy as np
import time


# Implementation of Jaccard Similarity
def createJaccardSim(graph):
    similarity_matrix = []
    for ith_type_vertices in graph.vertices:
        vertices_count = ith_type_vertices.count
        nodes = ith_type_vertices.nodes
        sim_matrix = np.zeros((vertices_count, vertices_count))
        for v1 in range(n_t):
            for v2 in range(n_t):
                sim_matrix[x][y] = 1 - distance.jaccard(nodes[x], nodes[y])

        similarity_matrix.append(sim_matrix)
    return similarity_matrix

def calculate_diagonal_matrix(similarity_matrix):
    D=[]
    for index, type_i_sim_matrix in enumerate(similarity_matrix):
        D.append(np.diag(np.sum(type_i_sim_matrix, axis=1)))
    
    return D

def computeObjectiveFunction(C, L, V, CN_sim, G):
    k_type = len(C)
    first_term, second_term = 0, 0
    for type_ in range(k_type):
        sim_t = CN_sim[type_]
        C_t = C[type_]
        n_t = len(sim_t)#n_t: number of vertices in the type

        for i in range(n_t):
            for j in range(i):
                first_term += sim_t[i][j]*np.sum((C_t[i] - C_t[j])**2)

    for t in range(k_type):
        for t_dash in range(t+1,k_type):
            G_t_t_dash = Gtt[(t,t_dash)]
            temp1 = np.matmul(L[(t, t_dash)]['adj_matrix'],C[t_dash].transpose())
            temp2 = np.matmul(C[t], temp1)

            second_term += np.sum((G_t_t_dash - temp2)**2)

    objective = first_term + second_term
    return objective