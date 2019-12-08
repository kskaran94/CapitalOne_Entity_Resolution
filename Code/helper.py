import distance
import numpy as np


# Implementation of Jaccard Similarity
def create_jaccard_sim(graph):
    similarity_matrix = []
    for ith_type_vertices in graph.vertices:
        vertices_count = ith_type_vertices.count
        nodes = ith_type_vertices.nodes
        sim_matrix = np.zeros((vertices_count, vertices_count))
        for v1 in range(vertices_count):
            for v2 in range(vertices_count):
                sim_matrix[v1][v2] = 1 - distance.jaccard(nodes[v1], nodes[v2])
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
        n_t = len(sim_t)  # n_t: number of vertices in the type

        for vertex_i in range(n_t):
            for vertex_j in range(vertex_i):
                first_term += sim_t[vertex_i][vertex_j]*np.sum((C_t[vertex_i] - C_t[vertex_j])**2)

    for t in range(graph.types):
        for t_dash in range(t+1, graph.types):
            G_t_t_dash = graph.Gtt[(t, t_dash)]
            temp1 = np.matmul(superlinks.L[(t, t_dash)]['adj_matrix'], c_mapping.C[t_dash].transpose())
            temp2 = np.matmul(c_mapping.C[t], temp1)

            second_term += np.sum((G_t_t_dash - temp2)**2)

    objective = first_term + second_term
    return objective


def compute_theta(C_t):
    vertex_cluster_contribution_sum = np.sum(C_t, axis=0)
    theta = min(vertex_cluster_contribution_sum)
    return theta, vertex_cluster_contribution_sum


def remove_supernode_from_L(superlinks, t_type, index_to_remove):
    for types, links in superlinks.L.items():
        if types[0] > t_type:
            break
        elif types[0] == t_type:
            links['adj_matrix'] = np.delete(links['adj_matrix'], index_to_remove, 0)
            # superlinks[types[0]].remove(supernode)
        
        elif types[1] == t_type:
            links['adj_matrix'] = np.delete(links['adj_matrix'], index_to_remove, 1)
            # superlinks[types[1]].remove(supernode)


def get_optimal_supernode(graph, c_mapping, superlinks):

    for type_i in range(graph.types):
        theta, vertex_cluster_contribution_sum = compute_theta(c_mapping.C[type_i])
        min_info_index = np.argmin(vertex_cluster_contribution_sum)
        # name_node = S[i]['name'][index]
        c_mapping.C[type_i] = np.delete(c_mapping.C[type_i], min_info_index, 1)
        remove_supernode_from_L(superlinks, type_i, min_info_index)  # does it work in-place?

    # return c_mapping, superlinks


def get_difference_c(c_new, c_old):
    change_in_c = 0
    for type_i in range(0, len(c_new.C)):
        change_in_c += np.sum(abs(c_new.C[type_i] - c_old.C[type_i]))

    return change_in_c


def get_difference_l(l_new, l_old):
    change_in_l = 0
    for tt_dash in l_new.L:
        change_in_l += np.sum(abs(l_new.L[tt_dash]['adj_matrix'] - l_old.L[tt_dash]['adj_matrix']))

    return change_in_l
