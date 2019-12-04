import copy
import math
import networkx as nx
import numpy as np

from collections import defaultdict
from collections import OrderedDict

class CMappings:
    # Initial value of C : random initialization
    # p is the number of supernodes for every k-type (assumption)
    def __init__(self):
        self.C = []

    def initialize_mapping(self, vertices, number_super_nodes):
        for k_type, vertex_collection in enumerate(vertices):
            # C_t is a mapping from all the nodes of t-type to its t-type supernode
            C_t = np.zeros((vertex_collection.count, number_super_nodes[k_type]))
            for v in range(vertex_collection.count):
                # Randomly maps the t-type node to a t-type supernode
                C_t[v]=np.random.dirichlet(np.ones(number_super_nodes[k_type]),size=1)[0]
            self.C.append(C_t)

    def update_mapping():

class SummaryGraph:
    def __init__(self):
        pass


class SuperLinks:
    def __init__(self):

    def update_links():


# for each k-type vertex, initial number of super nodes
# is set to the square root of count of vertices in that type (assumption)
def calculate_initial_super_nodes(V):
    number_super_nodes =[]
    for v in V:
        number_super_nodes.append(int(math.sqrt(len(v['name']))))
    
    return number_super_nodes

# Initial value of C : random initialization
# p is the number of supernodes for every k-type (assumption)
def initializeMapping(sim, p):
    C = []
    for i in range(len(sim)):
        # C_t is a mapping from all the nodes of t-type to its t-type supernode
        C_t = np.zeros((sim[i].shape[0], p[i]))
        for j in range(sim[i].shape[0]):
            # Randomly maps the t-type node to a t-type supernode
            C_t[j]=np.random.dirichlet(np.ones(p[i]),size=1)[0]
            #C_t[j, np.random.randint(low = 0, high = p[i])] = 1
        C.append(C_t)
    return C


def createSummaryGraph(G, C, V, k_type):
    SG = copy.deepcopy(G)
    S = []
    for i in range(len(C)):
        S_t = {'super_nodes':defaultdict(list), 'name':{}, 'position':{}}
        for j in range(C[i].shape[0]):
            ind = list(C[i][j]).index(max(C[i][j]))
            S_t['super_nodes'][ind].append(V[i]['name'][j])
        
        for k,v in S_t['super_nodes'].items():
            S_t['name'][k]=v[0]
            S_t['position'][v[0]]=k
            for j in range(1,len(v)):
                SG = nx.contracted_nodes(SG, v[0], v[j])
                
        S.append(S_t)
            
    return SG, S

def createTheSuperLinkMatrix(S):
    L = OrderedDict()
    for i in range(len(S)):
        S_t = S[i]
        for j in range(i+1,len(S)):
            S_t_dash = S[j]
            L_t_t_dash = {i:list(S_t['position'].keys()),
                          j:list(S_t_dash['position'].keys()),
                          'adj_matrix':np.zeros((len(S_t['super_nodes']), len(S_t_dash['super_nodes'])))}
            for k in range(0, len(S_t['super_nodes'])):
                L_t_t_dash['adj_matrix'][k]=np.random.dirichlet(np.ones(len(S_t_dash['super_nodes'])),size=1)[0]
            
            L[(i,j)] = L_t_t_dash
            
    return L


# number_super_nodes = calculate_initial_super_nodes(V)
# start_time = time.time()
# C = initializeMapping(CN_sim, number_super_nodes)
# print("Time taken to create the C Mapping:", (time.time()-start_time)/60)

# start_time = time.time()
# SG, S = createSummaryGraph(G, C, V, k_type)
# print("Time taken to create the Summary Graph:", (time.time()-start_time)/60)

# L = createTheSuperLinkMatrix(S)

