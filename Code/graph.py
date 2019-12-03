import networkx as nx
import pandas as pd

class Graph:
    def __init__(self):
        self.G = nx.Graph()

    def create_graph(self, column_ktype_mapping, *datasets):
        dataset_dfs = self._csv_to_dataframe(datasets)
        self._add_nodes_edges_to_graph(dataset_dfs, column_ktype_mapping)
        
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

# Importing data
path = '../Data/Amazon-GoogleProducts/'
DATASET_1 = "Amazon.csv"
DATASET_2 = "GoogleProducts.csv"

#mapping between column_name and kth-type
column_ktype_mapping = {'id':0, 'title':1, 'name':1, 'description':1}

graph = Graph()
graph.create_graph(column_ktype_mapping, DATASET_1, DATASET_2)
