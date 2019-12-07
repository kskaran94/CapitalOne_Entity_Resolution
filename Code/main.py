from graph import Graph
import pickle
from helper import create_jaccard_sim, calculate_diagonal_matrix
import os
from summary_graph import CMappings, SummaryGraph, SuperLink

# Importing data
path = '../Data/Amazon-GoogleProducts/'
DATASET_1 = os.path.join(path, "Amazon.csv")
DATASET_2 = os.path.join(path, "GoogleProducts.csv")

# mapping between column_name and kth-type
column_ktype_mapping = {'id': 0, 'title': 1, 'name': 1, 'description': 1}

graph = Graph(k_type=2)
graph.create_graph(column_ktype_mapping, DATASET_1, DATASET_2)
similarity_matrix = create_jaccard_sim(graph)
diagonal_matrix = calculate_diagonal_matrix(similarity_matrix)
c_mapping = CMappings()
c_mapping.initialize_mapping(graph)
summary_graph = SummaryGraph()
summary_graph.create_summary_graph(graph, c_mapping)
superlinks = SuperLink()
superlinks.create_super_links(summary_graph)

