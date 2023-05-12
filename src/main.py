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

#load gml file igraph
#g = Graph.Read_GML(os.path.join(path, file))
#g = Graph.Load(os.path.join(path, file), format='gml')
g = Graph.Read_GML(toy)

# %%
# sample of 100 nodes of bipartite = 0 and its neighbors
bipartite = 1
sample = g.vs.select(bipartite=bipartite)[0:10]
sample_neighbors = g.neighborhood(sample, order=1, mode='all')

nodes = [a for e in sample_neighbors for a in e]

# add all neighbor of the nodes that are bipartite = 0
nodes_neighbors = g.neighborhood(nodes, order=1, mode='all')
nodes2 = [a for e in nodes_neighbors for a in e]
# get onòy nodes that are bipartite = 0
nodes2 = [a for a in nodes2 if g.vs[a]['bipartite'] == 0]

nodes = nodes + nodes2




# create graph from sampleneighbors
gg = g.subgraph(set(nodes))



# %%
# plot with matpltolib
# only label for bipartite = 0
def plot_graph(gg):
    fig, ax = plt.subplots(figsize=(10,10))
    ig.plot(
        gg,
        target=ax,
        layout= "fr",
        #vertex_label= None,
        #vertex_label= gg.vs["bipartite"],
        vertex_color = ["red" if v["bipartite"] == 0.0 else "blue" for v in gg.vs],
        #vertex_label_color = "black",  # Adjust the label color
        #vertex_label_size = 14  # Use a single value for the label size
        #vertex_size = [a for a in gg.vs['degree']],
    )


# %%
# degree analysis 
def degree_analysis(g):
    g.vs['in_degree'] = g.indegree()
    g.vs['out_degree'] = g.outdegree()
    g.vs['degree'] = g.degree()


    d = {i['label']:i['degree'] for i in g.vs}
    degree = pd.DataFrame.from_dict(d, orient='index')
    degree.columns = ['degree']
    degree['bipartite'] = g.vs['bipartite']
    degree['degree'] = degree['degree'].astype(int)
    degree['bipartite'] = degree['bipartite'].astype(int)
    degree['indegree'] = g.vs['in_degree']
    degree['outdegree'] = g.vs['out_degree']

    top_users = degree[degree['bipartite'] == 0].sort_values(['degree', 'bipartite'], ascending=False).head(20) 
    top_tweets = degree[degree['bipartite'] == 1].sort_values(['degree', 'bipartite'], ascending=False).head(20)

    return degree

# %%


tweet = 800010279136305152
g.vs.select(label=tweet)

# neighbors of tweet
g.neighbors(tweet, mode='all')

# %%
pablo = 'pablorodas'
pablo = g.vs.select(label=pablo)
pablo_n = g.neighborhood(pablo, order=2, mode = 'out')
nodes = [a for e in pablo_n for a in e]

pablo_g = g.subgraph(nodes)
# %%
# remove nodes with outdegree < 5
pablo_g.vs['outdegree'] = pablo_g.outdegree()

pablo_g.vs.select(outdegree=0).delete()



# %%
import pandas as pd 

df = pd.read_pickle('/Volumes/boot420/Users/data/climate_network/cop22/cache/tweets_cop22.pkl')
# %%

# get the tweets with mentions field that is not empty list 
df = df[df['mentions_name'].map(lambda d: len(d)) > 0]

# %%



# %



# %%
g = Graph.Read_GML(toy) # read graph 
start_nodes = g.vs.select(bipartite=0) # get all aithora 

def recursive_explore(graph, node, visited, start_node, is_start_node = False, edges = None):

    if edges is None:
        edges = []
    # it is a user 
    if node['bipartite'] == 0.0:
        if  not is_start_node and node != start_node:
            edges.append((start_node['label'], node['label']))
            #return (start_node['label'], node['label'])
        elif node == start_node and not is_start_node:
            #print('ho incontrato di nuovo me')
            return 'me'
    # it is a tweet
   

    visited.add(node)
    neighbors = graph.neighborhood(node, mode='out')



    for neighbor in neighbors[1:]:
        if neighbor not in visited:
            node = g.vs[neighbor]
            edges = recursive_explore(graph, node, visited, start_node, False, edges)


    print(start_node['label'] , node['author'])
    return edges
#%%

# %%
