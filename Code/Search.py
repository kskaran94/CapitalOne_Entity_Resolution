import numpy as np
import copy

def computeTheta(C_t):
    vertex_cluster_contribution_sum = np.sum(C_t, axis = 0)
    theta = min(vertex_cluster_contribution_sum)
    return theta, vertex_cluster_contribution_sum

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

def removeSuperNodeFromL(L, t_type, supernode, index):
    L_temp = copy.deepcopy(L)
    for types, superlinks in L_temp.items():
        if types[0] > t_type:
            break
        elif types[0] == t_type:
            superlinks['adj_matrix'] = np.delete(superlinks['adj_matrix'], index , 0)
            superlinks[types[0]].remove(supernode)
        
        elif types[1] == t_type:
            superlinks['adj_matrix'] = np.delete(superlinks['adj_matrix'], index , 1)
            superlinks[types[1]].remove(supernode)

return L_temp

def getOptimalSuperNode(G, SG, S, C, L, V, CN_sim):
    VC = []
    for i in range(0,len(C)):
        theta, vertex_cluster_contribution_sum = computeTheta(C[i])
        #print("theta:",theta)
        #VC.append(vertex_cluster_contribution_sum)
        index = np.argmin(vertex_cluster_contribution_sum)
        name_node = S[i]['name'][index]
        SG.remove_node(name_node)
        C[i] = np.delete(C[i],index,1)
        L = removeSuperNodeFromL(L,i,name_node,index)
    
    return SG, C, L
# def getOptimalSuperNode(G, SG, S, C, L, V, CN_sim):
#     for i in range(0,len(C)): #i denotes the k-type
#         theta, vertex_cluster_contribution_sum = computeTheta(C[i])
#         S_t = S[i]['position']
#         for s,index in S_t.items():
#             info = vertex_cluster_contribution_sum[index]
#             SG_temp = copy.deepcopy(SG)
#             SG_temp.remove_node(s)

#             C_temp = copy.deepcopy(C)
#             C_temp[i] = np.delete(C_temp[i], index, 1)

#             #create L_temp
#             L_temp = removeSuperNodeFromL(L, i, s, index)
#             start_time = time.time()
#             SG_obj = computeObjectiveFunction(C, L, V, CN_sim, G)
#             print("Time taken to compute obj function for Summary graph:", (time.time()-start_time)/60)
#             start_time = time.time()
#             SG_temp_obj = computeObjectiveFunction(C_temp, L_temp, V, CN_sim, G)
#             print("Time taken to compute obj function for Summary graph w/o a node:", (time.time()-start_time)/60)
#             change_in_objective_function = SG_obj - SG_temp_obj
#             if info == theta and change_in_objective_function > 0:
#                 SG.remove_node(s)
#                 C = C_temp
#                 L = L_temp
#                 #update C and Ltt too

#     return SG, C, L
