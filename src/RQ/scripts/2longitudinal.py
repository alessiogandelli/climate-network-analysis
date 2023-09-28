#%%
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import json
import uunet.multinet as ml
import diptest
from latent_ideology.latent_ideology_class import latent_ideology as li
import networkx as nx
import matplotlib.colors as mcolors


n_cop = '2x'
folder = '/Users/alessiogandelli/data/cop' + str(n_cop) + '/'
retweet_df_path = folder + 'cache/retweets_labeled_cop'+str(n_cop)+'.pkl'
projected_path = folder + 'networks/cop' + str(n_cop) +'_retweet_network_ml.gml'
retweet_df = pd.read_pickle(retweet_df_path)
# drop cop 22
retweet_df = retweet_df[retweet_df['cop'] != 'cop22']
retweet_df = retweet_df[retweet_df['topic'] != -1]



cop_topic = retweet_df.groupby(['cop','topic']).count()['author'].reset_index()
cop_topic = cop_topic.pivot(index='cop', columns='topic', values='author')
cop_topic = cop_topic.div(cop_topic.sum(axis=0), axis=1)#normalize columns so the sum of the column is 1

#%% !!!!!! this is good 
################################################################
# divergin bar plot cop21 one side cop26 the other side
import matplotlib.pyplot as plt
import pandas as pd

# Assuming df is your DataFrame
df_transposed = cop_topic.transpose().sort_values(by='cop26', ascending=False).reset_index()

# get topics only in res.keys()
df_transposed = df_transposed[df_transposed['topic'].astype('int').isin(list(res.keys()))]





# index of p match with topic column, add it , not like this
df_transposed = df_transposed.merge(p.rename('polarization'), left_on='topic', right_index=True)

# use this order, do not use categorical 
#df_transposed.sort_values(by='polarization', inplace=True)
df_transposed['topic'] = df_transposed['topic'].astype('str')

# Create figure and axes
fig, ax = plt.subplots()

fig.set_size_inches(5, 7)

# Create a bar for cop26
ax.barh(df_transposed['topic'], df_transposed['cop26'], color='b', label='cop26')

# Create a bar for cop21 in the opposite direction
ax.barh(df_transposed['topic'], -df_transposed['cop21'], color='r', label='cop21')

# Set labels and title
ax.set_xlabel('Count')
ax.set_ylabel('Topic')

ax.set_title('Comparison of cop21 and cop26 for each topic')

#yticks 


# Add a vertical line at x=0
ax.axvline(0, color='black')

# Show legend
ax.legend()

# Show the plot
plt.show()



#%%

def draw_network(topic, ax, l, ris, only_influencers=False):
    net = l[topic]
    df1 = ris[topic][1]
    df2 = ris[topic][2]

    # merge dataframe of users 
    df1.rename(columns={'target':'user'}, inplace=True)
    df2.rename(columns={'source':'user'}, inplace=True)
    df = pd.concat([df1, df2], ignore_index=True)
    df.set_index('user', inplace=True)

    # add score to network
    nx.set_node_attributes(net, df['score'].to_dict(), 'score')




    influencers, users = get_influencers(net, 30)


    # remove self loops
    net.remove_edges_from(nx.selfloop_edges(net))

    net = net.subgraph(influencers) if only_influencers else net.subgraph(influencers + users)

    net = net.to_undirected()

    # delete node when score does not exist, because it's a user that never interacted with an influencer
    for node in net.copy():
        if 'score' not in net.nodes[node]:
            net.remove_node(node)

    # gradient color depending on the score 
    cmap = plt.get_cmap('spring')
    scores = [d['score'] for n, d in net.nodes(data=True)]
    norm = mcolors.Normalize(vmin=min(scores), vmax=max(scores))
    colors = [cmap(norm(score)) for score in scores]


    # remove edges that do not involve a influencer
    edges = list(net.edges())
    for e in edges:
        if e[0] not in influencers and e[1] not in influencers:
            net.remove_edge(e[0], e[1])





    size_map = [100 if node in influencers else 5 for node in net]

    x_noise = 0.0 if only_influencers else 0.01

    # use score for position but add noise in the other dimension
    pos = {n: [d['score'] + np.random.normal(0, x_noise), np.random.normal(0, 0.1)] for n, d in net.nodes(data=True)}


    # add title to plot
    plt.title('Topic: ' + str(topic) + ' - ' + topic_label[topic])


    nx.draw(net, pos=pos ,node_color=colors, with_labels=False, node_size=size_map, width=0.3, ax=ax)

    return ax


#%%
net1221 =  folder + 'networks/network1221.gml'
net1226 =  folder + 'networks/network1226.gml'

net1221 = nx.read_gml(net1221)
net1226 = nx.read_gml(net1226)

l = {21: net1221, 26: net1226}

res12 = get_polarization_by_layer(l, n_influencers = 10, n = 2)


stl = plot_dip_test(res12, l)

    # get network and df of correspondence analysis of the users 
 

fig, ax = plt.subplots(1, 2, figsize=(15, 5))

ax[0] = draw_network(21,ax[0], l, res12)
ax[0].set_title('COP21')
ax[1] = draw_network(26, ax[1], l, res12)
ax[1].set_title('COP26')

# fig title 
fig.suptitle('Retweet network for topic 12', fontsize=25)


plt.show()

#%%
net121 =  folder + 'networks/network121.gml'
net126 = folder + 'networks/network126.gml'

net121 = nx.read_gml(net121)
net126 = nx.read_gml(net126)

l = {21: net121, 26: net126}

res1 = get_polarization_by_layer(l, n_influencers = 15, n = 2)


stl = plot_dip_test(res1, l)


fig, ax = plt.subplots(1, 2, figsize=(15, 5))

ax[0] = draw_network(21,ax[0], l, res1)
ax[0].set_title('COP21')
ax[1] = draw_network(26, ax[1], l, res1)
ax[1].set_title('COP26')


# fig title
fig.suptitle('Retweet network for topic 1', fontsize=25)



plt.show()











# %%
# Import the libraries
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load your DataFrame
# retweet_df = pd.read_csv('your_data.csv')

# Grouping and Aggregating the Data
cop_topic = retweet_df.groupby(['cop','topic']).count()['author']

# drop topic 0
cop_topic = cop_topic.drop(0, level=1)

cop_topic_df = cop_topic.unstack(level=0)

# Create the heatmap
plt.figure(figsize=(10, 10))  # Customize this size according to your needs
sns.heatmap(cop_topic_df)

# Show the heatmap
plt.show()




#%%
