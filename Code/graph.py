import os
import networkx as nx
import OrderedDict
import pandas as pd

class KTypeVertex:
    def __init__(self):
        self.count = 0
        self.nodes = []
        self.name = {} # to maintain the order of nodes, so that nodes in similarity matrix can be mapped
        self.position = {}

class Graph:
    def __init__(self, k_type):
        self.G = nx.Graph()
        self.vertices = []
        self.types = k_type

    def create_graph(self, column_ktype_mapping, *datasets):
        dataset_dfs = self._csv_to_dataframe(datasets)
        self._add_nodes_edges_to_graph(dataset_dfs, column_ktype_mapping)
        self._get_vertices_per_type()
        self._create_Gtt_matrix()

    # converts csv into dataframe
    # type casts all columns to String type
    def _preprocess_data(self, datasets):
        dataset_dfs = []
        for dataset in datasets:
            df = pd.read_csv(dataset, encoding = "latin")
            # Converting all the data to string
            for column in df.columns:
                df[column] = df[column].apply(str)
            dataset_dfs.append(df)
        return dataset_dfs

    def _add_nodes_edges_to_graph(self, dataset_dfs, column_ktype_mapping):
        # creating nodes
        for dataset in dataset_dfs:
            for column_name in dataset.columns:
                if column_name in column_ktype_mapping:
                    self.G.add_nodes_from(dataset[column_name], type=column_ktype_mapping[column_name])


        #creating edges
        for dataset in dataset_dfs:
            column_list = dataset.columns; column_list.remove('id')
            for column_name in dataset.columns:
                if column_name in column_list:
                    self.G.add_edges_from(list(zip(dataset['id'], dataset[column_name])))

        self.G.remove_node("nan")

    def _get_vertices_per_type(self):
        for type_i in range(self.types):
            
            type_i_vertex = KTypeVertex()
            # extract the node values
            nodes = [node_label for node_label, node_attr in self.G.nodes(data=True) if node_attr['type'] == type_i]
            type_i_vertex.nodes = nodes
            type_i_vertex.count = len(nodes)

            for index, node_label in enumerate(nodes):
                type_i_vertex.name[index] = node_label
                type_i_vertex.position[node_label] = index
                
            self.vertices.append(type_i_vertex)

    def _create_Gtt_matrix(self):
        self.Gtt = OrderedDict()
        for type_1 in range(self.types):
            for type_2 in range(type_1+1, self.types):

                subgraph = self.G.subgraph(self.vertices[type_1].nodes + self.vertices[type_2].nodes)
                G_t_t_dash = np.zeros((self.vertices[type_1].count, self.vertices[type_2].count)))
                type_1_vertex_position = self.vertices[type_1].position
                type_2_vertex_position = self.vertices[type_2].position

                for edge in subgraph.edges():
                    G_t_t_dash[type_1_vertex_position[edge[0]], type_2_vertex_position[edge[1]]] = 1
                
                Gtt[(type_1, type_2)]=G_t_t_dash

