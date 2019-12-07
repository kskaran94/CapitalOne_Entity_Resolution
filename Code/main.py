from graph import Graph
# from helper import createJaccardSim
import os

# Importing data
path = '../Data/Amazon-GoogleProducts/'
DATASET_1 = os.path.join(path, "Amazon.csv")
DATASET_2 = os.path.join(path, "GoogleProducts.csv")

# mapping between column_name and kth-type
column_ktype_mapping = {'id': 0, 'title': 1, 'name': 1, 'description': 1}

graph = Graph(k_type=2)
graph.create_graph(column_ktype_mapping, DATASET_1, DATASET_2)
