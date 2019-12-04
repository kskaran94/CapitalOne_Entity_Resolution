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

D = calcDiagonalMatrix(CN_sim)