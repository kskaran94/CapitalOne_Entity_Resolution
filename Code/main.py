from graph import Graph
from helper import create_jaccard_sim, calculate_diagonal_matrix, get_optimal_supernode, get_difference_c,\
get_difference_l, compute_objective_function
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

for i in range(3):
    # Step 2: Call Search(G,S(G))
    get_optimal_supernode(graph, c_mapping, superlinks)

    # Step 3: update C and L
    C_values = []
    change_C = []
    L_values = []
    change_L = []
    for j in range(1):
        c_old = c_mapping
        c_mapping = c_mapping.update_mapping(graph, superlinks, similarity_matrix, diagonal_matrix)

        l_old = superlinks
        superlinks = superlinks.update_links(graph, c_mapping)

        change_in_c = get_difference_c(c_mapping, c_old)
        change_in_l = get_difference_l(superlinks, l_old)

        print(change_in_c, change_in_l)
        change_C.append(change_in_c)
        change_L.append(change_in_l)
        C_values.append(c_mapping)
        L_values.append(superlinks)

    index = change_C.index(min(change_C))
    C = C_values[index]
    index = change_L.index(min(change_L))
    L = L_values[index]

    # Calculate the new objective function
    final_objective = compute_objective_function(graph, c_mapping, superlinks, similarity_matrix)
    print(final_objective)
