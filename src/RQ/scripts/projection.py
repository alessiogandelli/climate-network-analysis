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


#%%

def recursive_explore(graph, node, visited, start_node, is_start_node = False, edges = None, topic= None):

    if edges is None:
        edges = {}
    # it is a user 
    if node['bipartite'] == 0.0:
        if  not is_start_node and node != start_node:
           # print(start_node['label'], node['label'])
            edges.setdefault(topic, []).append((start_node['label'], node['label']))
            #edges.append(((start_node['label'], node['label']), topic))
            return edges
        elif node == start_node and not is_start_node:
            #print('ho incontrato di nuovo me')
            return 'me'
    else :
        if topic is None:
            topic = node['topics']
    # it is a tweet
   

    visited.add(node)
    neighbors = graph.neighborhood(node, mode='out')


    for neighbor in neighbors[1:]:
        if neighbor not in visited:
            node = g.vs[neighbor]
            
            result = recursive_explore(graph, node, visited, start_node, False, edges, topic)
            if result is None:
                #print(start_node['label'], node['label'])
                return result

    #print(start_node['label'] , node['author'])
    #edges.append(((start_node['label'], node['author']), topic))
    edges.setdefault(topic, []).append((start_node['label'], node['author']))
    return edges, depth
#%%

# remove the edges with the same source and target


g = Graph.Read_GML(sample) # read graph 
#g = Graph.Read_GML(os.path.join(path, file)) # read graph

edges = {}

for n in g.vs.select(bipartite=0):
    # get all neighbors of g

    print(n)
    visited = set()
    result, depth = recursive_explore(g, n, visited, start_node = n , is_start_node=True)
    edges = {key: edges.get(key, []) + result.get(key, []) for key in set(edges) | set(result)}



# %%




pg = nx.from_edgelist(edges, create_using=nx.DiGraph())
# save grpah 
nx.write_gml(pg, os.path.join(path, 'projection_retweet.gml'))
# %%




# %%
sample = '/Volumes/boot420/Users/data/climate_network/test/networks/sampleretweets.gml'

def project_graph(sample):

    def recursive_explore(graph, node, visited, start_node, is_start_node = False, edges = None, topic= None):

        if edges is None:
            edges = {}
        # it is a user 
        if node['bipartite'] == 0.0:
            if  not is_start_node and node != start_node:
            # print(start_node['label'], node['label'])
                edges.setdefault(topic, []).append((start_node['label'], node['label']))
                #edges.append(((start_node['label'], node['label']), topic))
                return edges
            elif node == start_node and not is_start_node:
                #print('ho incontrato di nuovo me')
                return 'me'
        else :
            if topic is None:
                topic = node['topics']
        # it is a tweet
    

        visited.add(node)
        neighbors = graph.neighborhood(node, mode='out')


        for neighbor in neighbors[1:]:
            if neighbor not in visited:
                node = g.vs[neighbor]
                
                result = recursive_explore(graph, node, visited, start_node, False, edges, topic)
                if result is None:
                    #print(start_node['label'], node['label'])
                    return result

        #print(start_node['label'] , node['author'])
        #edges.append(((start_node['label'], node['author']), topic))
        edges.setdefault(topic, []).append((start_node['label'], node['author']))
        return edges

    g = Graph.Read_GML(sample)

    edges = {}

    for n in g.vs.select(bipartite=0):
        # get all neighbors of g
        visited = set()
        result = recursive_explore(g, n, visited, start_node = n , is_start_node=True)

        edges = {key: edges.get(key, []) + result.get(key, []) for key in set(edges) | set(result)}

    edges = {e: set(edges[e]) for e in edges }
    edges.pop(None, None)
    # drop key 

    return edges




# %%
edges = project_graph(sample)
# %%
graphs = {}
for t, e in edges.items():
    graphs[t] = nx.from_edgelist(e, create_using=nx.DiGraph())
# %%

