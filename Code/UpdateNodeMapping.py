import networkx as nx
import numpy as np

def createTheGttMatrix(G,V):
    Gtt = OrderedDict()
    for i in range(len(V)):
        for j in range(i+1,len(V)):
            subgraph = G.subgraph(V[i]['nodes'] + V[j]['nodes'])
            G_t_t_dash = np.zeros((len(V[i]['nodes']), len(V[j]['nodes'])))
            for edge in subgraph.edges():
                G_t_t_dash[V[i]['position'][edge[0]], V[j]['position'][edge[1]]] = 1
            
            Gtt[(i,j)]=G_t_t_dash
    return Gtt

def calcDiagonalMatrix(sim):
    D=[]
    for i in range(0,len(sim)):
        D.append(np.diag(np.sum(sim[i],axis=1)))
    
    return D

def updateC(G, V, C, L, sim, D):
    for i in range(len(C)):
        C_t = C[i]
        D_t = D[i]
        sum1 = np.zeros(C_t.shape)
        sum2 = np.zeros(C_t.shape)
        for j in range(i+1, len(C)):
            C_t_dash = C[j]
            G_t_t_dash = Gtt[(i,j)]
            L_t_t_dash = L[(i,j)]['adj_matrix']
            temp1 = np.dot(C_t_dash, L_t_t_dash.transpose())
            sum1 += np.dot(G_t_t_dash, temp1)
            sum2 += np.dot(C_t, np.dot(L_t_t_dash, np.dot(C_t_dash.transpose(), temp1)))
        sum1 += np.matmul(sim[i], C_t)
        sum2 += np.matmul(D_t, C_t)
        C[i] = np.multiply(C_t, np.sqrt(np.divide(sum1, sum2)))
        for j in range(0,len(C[i])):
            C[i][j] = C[i][j]/sum(C[i][j])
    return C

def updateL(G, V, C, L):
    for i in range(len(C)):
        C_t = C[i]
        for j in range(i+1, len(C)):
            L_t_t_dash = L[(i,j)]['adj_matrix']
            C_t_dash = C[j]
            G_t_t_dash = Gtt[(i,j)]
            temp1 = np.dot(C_t.transpose(), np.dot(G_t_t_dash, C_t_dash))
            temp2 = np.dot(L_t_t_dash, np.dot(C_t_dash.transpose(), C_t_dash))
            temp3 = np.dot(C_t.transpose(), np.dot(C_t, temp2))
            L[(i,j)]['adj_matrix'] = np.multiply(L_t_t_dash, np.sqrt(np.divide(temp1, temp3)))
            for k in range(0,len(L[(i,j)]['adj_matrix'])):
                L[(i,j)]['adj_matrix'][k] = L[(i,j)]['adj_matrix'][k]/sum(L[(i,j)]['adj_matrix'][k])
    return L



Gtt = createTheGttMatrix(G,V)

