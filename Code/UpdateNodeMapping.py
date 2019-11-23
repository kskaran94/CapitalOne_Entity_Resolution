import networkx as nx
import numpy as np

def calcDiagonalMatrix(sim):
    D=[]
    for i in range(0,len(sim)):
        D.append(np.diag(np.sum(sim[i],axis=1)))
        
    return D
        
def updateC(G, V, C, L, sim, D):
    l=0
    for i in range(len(C)):
        C_t = C[i]
        D_t = D[i]
        sum1 = np.zeros(C_t.shape)
        sum2 = np.zeros(C_t.shape)
        for j in range(i+1, len(C)):
            C_t_dash = C[j]
            subgraph = G.subgraph(V[i]['nodes'] + V[j]['nodes'])
            G_t_t_dash = np.zeros((len(V[i]['nodes']), len(V[j]['nodes'])))
            for edge in subgraph.edges():
                G_t_t_dash[V[i]['position'][edge[0]], V[j]['position'][edge[1]]] = 1
            L_t_t_dash = L[l]['adj_matrix']
            temp1 = np.matmul(C_t_dash, L_t_t_dash.transpose())
            sum1 += np.matmul(G_t_t_dash, temp1)
            sum2 += np.matmul(C_t, np.matmul(L_t_t_dash, np.matmul(C_t_dash, temp1)))
            l+=1
        sum1 += np.matmul(sim[i], C_t)
        sum2 += np.matmul(D_t, C_t)
        C[i] = np.multiply(C_t, np.sqrt(np.divide(sum1, sum2)))
    return C

def updateL(G, V, C, L):
    l=0
    for i in range(len(C)):
        C_t = C[i]
        for j in range(i+1, len(C)):
            L_t_t_dash = L[l]['adj_matrix']
            C_t_dash = C[j]
            subgraph = G.subgraph(V[i]['nodes'] + V[j]['nodes'])
            G_t_t_dash = np.zeros((len(V[i]['nodes']), len(V[j]['nodes'])))
            for edge in subgraph.edges():
                G_t_t_dash[V[i]['position'][edge[0]], V[j]['position'][edge[1]]] = 1
            temp1 = np.matmul(C_t.transpose(), np.matmul(G_t_t_dash, C_t_dash))
            temp2 = np.matmul(L_t_t_dash, np.matmul(C_t_dash.transpose(), C_t_dash))
            temp3 = np.matmul(C_t.transpose(), np.matmul(C_t, temp2))
            L[l]['adj_matrix'] = np.multiply(L_t_t_dash, np.sqrt(np.divide(temp1, temp3)))
            l+=1
    return L