# for each k-type vertex, initial number of super nodes
# is set to the square root of count of vertices in that type (assumption)
def calculate_initial_super_nodes(V):
    number_super_nodes =[]
    for v in V:
        number_super_nodes.append(int(math.sqrt(len(v['name']))))
    
    return number_super_nodes

def calculate_diagonal_matrix(sim):
    D=[]
    for i in range(0,len(sim)):
        D.append(np.diag(np.sum(sim[i],axis=1)))
    
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