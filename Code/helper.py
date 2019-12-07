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

def compute_objective_function(graph, c_mapping, superlinks, similarity_matrix):
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

def compute_theta(C_t):
    vertex_cluster_contribution_sum = np.sum(C_t, axis = 0)
    theta = min(vertex_cluster_contribution_sum)
    return theta, vertex_cluster_contribution_sum

def remove_supernode_from_L(superlinks, t_type, index_to_remove):
    for types, links in superlinks.L.items():
        if types[0] > t_type:
            break
        elif types[0] == t_type:
            links['adj_matrix'] = np.delete(links['adj_matrix'], index_to_remove , 0)
            #superlinks[types[0]].remove(supernode)
        
        elif types[1] == t_type:
            links['adj_matrix'] = np.delete(links['adj_matrix'], index_to_remove , 1)
            #superlinks[types[1]].remove(supernode)

def get_optimal_supernode(G, SG, S, C, L, V, CN_sim): (graph, summary_graph, c_mapping, superlinks, similarity_matrix)

    for type_i in range(graph.types):
        theta, vertex_cluster_contribution_sum = compute_theta(c_mapping.C[type_i])
        min_info_index = np.argmin(vertex_cluster_contribution_sum)
        #name_node = S[i]['name'][index]
        c_mapping.C[type_i] = np.delete(c_mapping.C[type_i], min_info_index, 1)
        remove_supernode_from_L(superlinks, type_i, min_info_index) #does it work in-place?
    
    # start_time = time.time()
    # SG, S = createSummaryGraph(G, C, V, k_type)
    # print("Time taken to update the summary graph:", (time.time()-start_time)/60)
    return C, L