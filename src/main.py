#%%
import os
import pandas as pd
from igraph import Graph 
import igraph as ig
import networkx as nx
import matplotlib.pyplot as plt

path = '/Volumes/boot420/Users/data/climate_network/cop22/networks'

file = 'cop22retweets.gml'

#load gml file igraph
g = Graph.Read_GML(os.path.join(path, file))
#g = Graph.Load(os.path.join(path, file), format='gml')


# %%
# sample of 100 nodes of bipartite = 0 and its neighbors
bipartite = 1
sample = g.vs.select(bipartite=bipartite)[0:10]
sample_neighbors = g.neighborhood(sample, order=1, mode='all')

nodes = [a for e in sample_neighbors for a in e]
# create graph from sampleneighbors
gg = g.subgraph(nodes)



# %%
# plot with matpltolib
# only label for bipartite = 0

fig, ax = plt.subplots(figsize=(10,10))
ig.plot(
    gg,
    target=ax,
    layout= "fr",
    vertex_label= gg.vs["bipartite"],
    vertex_color = ["red" if v["bipartite"] == 0.0 else "blue" for v in gg.vs],
    vertex_label_color = "black",  # Adjust the label color
    vertex_label_size = 14  # Use a single value for the label size
)


# %%
