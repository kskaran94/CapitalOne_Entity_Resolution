import numpy as np
import copy

def ComputeTheta(C_t):
    vertex_cluster_contribution_sum = np.sum(C_t, axis = 0)
    theta = min(vertex_cluster_contribution_sum)
    return theta, vertex_cluster_contribution_sum

def ComputeObjectiveFunction(S, C, L, V, CN_sim, k_type):
    #k_type = 2
    first_term, second_term = 0, 0
    for type_ in range(k_type):
        sim_t = CN_sim[type_]
        C_t = C[type_]
        n_t = len(sim_t)

        for i in range(n_t):
            for j in range(i):
                first_term += sim_t[i][j]*np.sum((C_t[i] - C_t[j])**2)

    l=0
    for t in range(k_type):
        for t_dash in range(i+1,k_type):
            G_t_t_dash = np.zeros((len(V[t]['nodes']), len(V[t_dash]['nodes'])))
            for edge in subgraph.edges():
                G_t_t_dash[V[t]['position'][edge[0]], V[t_dash]['position'][edge[1]]] = 1
            
            temp1 = np.matmul(L[l]['adj_matrix'],C[t_dash].transpose())
            temp2 = np.matmul(C[t], temp1)
            l+=1

            second_term += np.sum((G_t_t_dash - temp2)**2)

    objective = first_term + second_term
    return objective


def GetOptimalSuperNode(G, SG, S, C):
    #S is a list of dictionaries; C is a list of numpy matrices
    #Keys in dictionary: order, name, position
    #Another key exists for the merged nodes - **** need to give key name ****
    #Should we keep a key to indicate which k-type?
    for i in range(0,len(C)):
        theta, vertex_cluster_contribution_sum = ComputeTheta(C[i])
        S_t = list(S[i]['position'].keys())
        for index,s in enumerate(S_t):
            info = vertex_cluster_contribution_sum[index]
            SG_temp = copy.deepcopy(SG)
            SG_temp.remove_node(s)
            change_in_objective_function = ComputeObjectiveFunction(SG) - ComputeObjectiveFunction(SG_temp)
            if info == theta and change_in_objective_function > 0:
                SG.remove_node(s)
                
    return SG



