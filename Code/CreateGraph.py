#!/usr/bin/env python
# Importing packages

import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt


# Importing data

path = '../Data/Amazon-GoogleProducts/'
data_1 = pd.read_csv(path + 'Amazon.csv', encoding = "latin")
data_2 = pd.read_csv(path + 'GoogleProducts.csv', encoding = "latin")

# Creating graph and nodes from dataset

k_type = ["id", "title", "description", "manufacturer", "price"]
G_amazon = nx.Graph()

G_google = nx.Graph()

for k in range(len(k_type)):
    G_amazon.add_nodes_from(data_1[data_1.columns[k]], t = k_type[k])
    G_google.add_nodes_from(data_2[data_2.columns[k]], t = k_type[k])

# Creating edges

for i in range(len(data_1)):
    G_amazon.add_edge(data_1.manufacturer[i], data_1.id[i])
    G_amazon.add_edge(data_1.id[i], data_1.price[i])
    G_amazon.add_edge(data_1.id[i], data_1.title[i])

for i in range(len(data_2)):
    G_google.add_edge(data_2.manufacturer[i], data_2.id[i])
    G_google.add_edge(data_2.id[i], data_2.price[i])
    G_google.add_edge(data_2.id[i], data_2.name[i])
