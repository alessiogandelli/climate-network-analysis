#%%
import os
import pandas as pd
from igraph import Graph 
import igraph as ig
import networkx as nx
import matplotlib.pyplot as plt

import uunet.multinet as ml
path = '/Volumes/boot420/Users/data/climate_network/cop22/networks'


file = 'cop22retweets.gml'

toy = '/Users/alessiogandelli/dev/internship/tweets-to-topic-network/data/networks/toyretweets.gml'




def recursive_explore(graph, node, visited, start_node, is_start_node = False, edges = None):

    if edges is None:
        edges = []
    # it is a user 
    if node['bipartite'] == 0.0:
        if  not is_start_node and node != start_node:
           # print(start_node['label'], node['label'])
            edges.append((start_node['label'], node['label']))
            return edges
        elif node == start_node and not is_start_node:
            #print('ho incontrato di nuovo me')
            return 'me'
    # it is a tweet
   

    visited.add(node)
    neighbors = graph.neighborhood(node, mode='out')



    for neighbor in neighbors[1:]:
        if neighbor not in visited:
            node = g.vs[neighbor]
            
            result = recursive_explore(graph, node, visited, start_node, False, edges)
            if result is None:
                #print(start_node['label'], node['label'])
                return result

    #print(start_node['label'] , node['author'])
    edges.append((start_node['label'], node['author']))
    return edges
#%%

# remove the edges with the same source and target


#g = Graph.Read_GML(toy) # read graph 
g = Graph.Read_GML(os.path.join(path, file)) # read graph

edges = []

for n in g.vs.select(bipartite=0):
    # get all neighbors of g
    visited = set()
    result = recursive_explore(g, n, visited, start_node = n , is_start_node=True)
    edges += result

edges = set([e for e in edges if e[0] != e[1]])
# %%




pg = nx.from_edgelist(edges, create_using=nx.DiGraph())
# save grpah 
nx.write_gml(pg, os.path.join(path, 'projection_retweet.gml'))
# %%

# get only ones with outdegree > 5
pg = pg.subgraph([n for n in pg.nodes() if pg.out_degree(n) > 5])

nx.draw(pg, with_labels=False)
# %%
