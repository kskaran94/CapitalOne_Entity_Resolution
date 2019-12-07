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
    diagonal_matrix = []
    for index, type_i_sim_matrix in enumerate(similarity_matrix):
        diagonal_matrix.append(np.diag(np.sum(type_i_sim_matrix, axis=1)))
    
    return diagonal_matrix

def computeObjectiveFunction(graph, c_mapping, superlinks, similarity_matrix):
    first_term, second_term = 0, 0
    for type_i in range(graph.types):
        sim_t = similarity_matrix[type_i]
        C_t = c_mapping.C[type_i]
        n_t = len(sim_t)#n_t: number of vertices in the type

        for vertex_i in range(n_t):
            for vertex_j in range(i):
                first_term += sim_t[vertex_i][vertex_j]*np.sum((C_t[vertex_i] - C_t[vertex_j])**2)

    for t in range(graph.types):
        for t_dash in range(t+1, graph.types):
            G_t_t_dash = graph.Gtt[(t,t_dash)]
            temp1 = np.matmul(superlinks.L[(t, t_dash)]['adj_matrix'], c_mapping.C[t_dash].transpose())
            temp2 = np.matmul(c_mapping.C[t], temp1)

            second_term += np.sum((G_t_t_dash - temp2)**2)

    objective = first_term + second_term
    return objective