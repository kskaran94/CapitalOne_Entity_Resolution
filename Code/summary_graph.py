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

    # random initialization
    def initialize_mapping(self, graph):
        number_super_nodes = _calculate_initial_super_nodes(graph)
        for k_type, vertex_collection in enumerate(graph.vertices):
            # C_t is a mapping from all the nodes of t-type to its t-type supernode
            C_t = np.zeros((vertex_collection.count, number_super_nodes[k_type]))
            for v in range(vertex_collection.count):
                # Randomly maps the t-type node to a t-type supernode
                C_t[v]=np.random.dirichlet(np.ones(number_super_nodes[k_type]),size=1)[0]
            self.C.append(C_t)

    # for each k-type vertex, initial number of super nodes
    # is set to the square root of count of vertices in that type (assumption)
    def _calculate_initial_super_nodes(self, graph):
        number_super_nodes =[]
        for v in graph.vertices:
            number_super_nodes.append(int(math.sqrt(v.count)))
        
        return number_super_nodes

    def update_mapping():
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
            if i >=1:
                C[i] = np.multiply(C_t, np.sqrt(np.divide(sum1, sum2)))
            for j in range(0,len(C[i])):
                C[i][j] = C[i][j]/sum(C[i][j])
        return C


class SuperNode:
    def __init__(self):
        self.nodes_to_cluster = defaultdict(list)
        self.supernode_count = 0

class SuperLink:
    def __init__(self):
        self.L = OrderedDict()

    def create_super_links(self, summary_graph):
        for type_i, type_i_supernodes in enumerate(summary_graph.S):
            type_i_count = type_i_supernodes.supernode_count
            for type_j in range(type_i+1, len(summary_graph)):
                type_j_supernodes = summary_graph[type_j]
                type_j_count = type_j_supernodes.supernode_count

                L_t_t_dash = {'adj_matrix':np.zeros((type_i_count, type_j_count))}
                for k in range(0, type_i_count):
                    L_t_t_dash['adj_matrix'][k]=np.random.dirichlet(np.ones(type_j_count), size=1)[0]
                
                self.L[(i,j)] = L_t_t_dash
        


    def update_links():
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

class SummaryGraph:
    def __init__(self):
        self.S = []

    def create_summary_graph(self, graph, c_mapping):
        for type_i, type_i_c_mapping in enumerate(c_mapping):
            S_t = SuperNode()
            for vertex_index, vertex_mapping in enumerate(type_i_c_mapping):
                supernode_index = np.argmax(vertex_mapping)
                S_t.nodes_to_cluster[supernode_index].append(graph.vertices[type_i].name[vertex_index])

            S_t.supernode_count = len(S_t.nodes_to_cluster)
            
            # for k,v in S_t['super_nodes'].items():
            #     S_t['name'][k]=v[0]
            #     S_t['position'][v[0]]=k
            #     for j in range(1,len(v)):
            #         SG = nx.contracted_nodes(SG, v[0], v[j])
                    
            self.S.append(S_t)



