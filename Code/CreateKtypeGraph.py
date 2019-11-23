#!/usr/bin/env python
# Importing packages

import networkx as nx
import pandas as pd

def createGraph(data_1, data_2, data_col, combined_col):

    # Creating graph and nodes from dataset

    G = nx.Graph()
    for k in range(len(data_col)):
        if data_1.columns[k] in combined_col:
            G.add_nodes_from(data_1[data_1.columns[k]], t = "combined_col")
        else:
            G.add_nodes_from(data_1[data_1.columns[k]], t = data_col[k])
        if data_2.columns[k] in combined_col:
            G.add_nodes_from(data_2[data_2.columns[k]], t = "combined_col")
        else:
            G.add_nodes_from(data_2[data_2.columns[k]], t = data_col[k])

    # Creating edges

    for i in range(len(data_1)):
        for k in combined_col:
            if k in data_1.columns:
                G.add_edge(data_1.id[i], data_1[k][i])

    for i in range(len(data_2)):
        for k in combined_col:
            if k in data_2.columns:
                G.add_edge(data_2.id[i], data_2[k][i])

    k_type = [i for i in data_col if i not in combined_col]
    if len(combined_col) > 0:
        k_type.append("combined_col")
    return G, k_type

# Importing data

path = '../Data/Amazon-GoogleProducts/'
data_1 = pd.read_csv('Amazon.csv', encoding = "latin")
data_2 = pd.read_csv('GoogleProducts.csv', encoding = "latin")

# Converting all the data to string
for col in data_1.columns:
	data_1[col] = data_1[col].apply(str)
for col in data_2.columns:
	data_2[col] = data_2[col].apply(str)

# Defining k_type and columns to be combined into one type
data_col = ["id", "title", "description", "manufacturer"]
word = ["title", "name", "description", "manufacturer"]

# Function call
#G, k_type = createGraph(data_1, data_2, data_col, word)