
#%%
from latent_ideology.latent_ideology_class import latent_ideology as li
import pandas as pd
import networkx as nx

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import uunet.multinet as ml
import json
import matplotlib.pyplot as plt
import diptest
import numpy as np
import matplotlib.colors as mcolors



# %% prepare data 
n_cop = 26

folder = '/Users/alessiogandelli/data/cop' + str(n_cop) + '/'
projected_path = folder + 'networks/cop' + str(n_cop) +'_retweet_network_ml.gml'
topic_label = json.load(open(folder + 'cache/labels_cop'+str(n_cop)+'.json'))
topic_label = {int(k): v for k, v in topic_label.items()}# key float to int

mln = ml.read(projected_path)   # multilayer network

layers = ml.to_nx_dict(mln) # dictionary where we have a networkx graph for each layer
layers = {int(float(k)): v for k, v in layers.items()} # key float to int

#%%

# get number of nodes for each layer
n_nodes = {k: v.number_of_nodes() for k, v in layers.items()}
# plot number of nodes for each layer
plt.figure(figsize=(12,4))
plt.bar([str(k) for k in n_nodes.keys()], n_nodes.values())
plt.xlabel('Layer')
plt.ylabel('Number of nodes')
plt.title('Number of nodes by layer for COP' + str(n_cop))
plt.show()

# %%


def get_influencers(net, n_influencers):
    degree = net.degree()
    sorted_degree = sorted(degree, key=lambda x: x[1], reverse=True)
    influencers = [s[0] for s in sorted_degree[:n_influencers]]
    users = [s[0] for s in sorted_degree[n_influencers:]]
    

    return influencers, users


def get_polarization_by_layer(n_influencers = 30, n = 2):
    res = {}

    for l in layers:
        net = layers[l]

        # number of edges and nodes 
        print('Layer: ', l)
        print('Number of nodes: ', net.number_of_nodes())
        print('Number of edges: ', net.number_of_edges())


        # get n influencers with highest degree 
        influencers, _ = get_influencers(net, n_influencers)


        # create connection df between influencers and users 
        connection_df = pd.DataFrame(columns=['influencer','user'])
        for i in influencers:
            # get all in edges of node i
            edges = net.in_edges(i)

            for e in edges:
                connection_df = pd.concat([connection_df, pd.DataFrame({'influencer':i, 'user':e[0]}, index=[0])], ignore_index=True)


        # create matrix and apply latent ideology
        try:
            li_matrix = li(connection_df)
            df1, df2 = li_matrix.apply_method(n=n,targets='user', sources='influencer')
        except:
            print('Layer ', l, ' has too few data to be analyzed with latent ideology')
            continue


        # perform dip test on scores
        test = df1['score'].to_numpy()

        dip_res = diptest.diptest(test)
        
        if dip_res[1] < 0.05 and l != -1:
            res[l] = (dip_res, df1, df2)
            res = {int(float(k)): v for k, v in res.items()}
        else:
            print('Layer ', l, ' has too few data to be analyzed with dip test')

    
    return res

def plot_dip_test(res, cop_name='COP'+str(n_cop)):

    # keys float to int

    #sort the result of the diptest 
    diptest = [(r[0], r[1][0][0]) for r in res.items()]
    diptest_s = sorted(diptest, key=lambda x: x[1], reverse=True)

    # add to diptest the number of nodes in each layer
    diptest_s = [(d[0], d[1], layers[d[0]].number_of_nodes()) for d in diptest_s]

    n_nodes = [layers[k].number_of_nodes() for k, v in res.items()]



    # grpuped bar chart witu n_nodes and diptest_s
    fig, ax = plt.subplots(figsize=(12,4))

    plt.title('Dip test and number of users by layer for ' + cop_name)

    bars1 = ax.bar([str(d[0]) for d in diptest_s], [d[1] for d in diptest_s], label='Dip test')


    ax.set_ylabel('Dip test')
    ax.set_xlabel('Layer')
    plt.axhline(y=np.mean([d[1] for d in diptest_s]), color='r', linestyle='-', label='Mean dip test')

    ax2 = ax.twinx()
    ax2.bar([str(d[0]) for d in diptest_s], [d[2] for d in diptest_s], color='orange', label='Number of users')
    # broken axes between 80000 and 140000
    ax2.set_ylim(0, 80000)
    ax2.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax2.xaxis.tick_bottom()
    ax.tick_params(labeltop=False)  # don't put tick labels at the top
    ax2.xaxis.set_ticks_position('none')  # don't put tick labels at the top
    ax2.yaxis.set_ticks_position('left')
    ax2.set_ylim(80000, 140000)
    ax2.spines['bottom'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax2.xaxis.tick_top()
    ax.tick_params(labelbottom=False)  # don't put tick labels at the top
    
    ax2.set_ylabel('Number of nodes')
    ax.legend(loc='upper left')
    ax2.legend(loc='upper right')

    #bar widht 
    # i want tonly half of the xtiks
    plt.xticks([str(d[0]) for d in diptest_s], [str(d[0]) for d in diptest_s])
    



    #plt.figure(figsize=(12,4))
    #plt.bar([str(d[0]) for d in diptest_s], [d[1] for d in diptest_s])


    # write xticks on top of the bar 
    plt.xticks([str(d[0]) for d in diptest_s], [str(d[0]) for d in diptest_s])
    plt.xticks(rotation=90)     

    # add mean line to left axes 



    #plt.axhline(y=np.mean([d[1] for d in diptest_s]), color='r', linestyle='-')
    # add x label
    #plt.xlabel('Layer')
    # add y label
    #plt.ylabel('Dip test')
    plt.show()


    # print the most and least polarized topics according to this test 

    # sort topic label according to diptest_s mantain keys
    sorted_topic_label = [(k[0], topic_label[k[0]]) for k  in diptest_s]

    # print 10 most and least polarized topics one per line
    print('Most polarized topics:')
    for i in range(10):
        print(sorted_topic_label[i][0], sorted_topic_label[i][1])
    print('')
    print('Least polarized topics:')

    for i in range(1,9):
        print(sorted_topic_label[-i][0], sorted_topic_label[-i][1])

    return sorted_topic_label
    # plot sorted topic label

def draw_network(topic, ax, only_influencers=False):
    # get network and df of correspondence analysis of the users 
    net = layers[topic]
    df1 = res[topic][1]
    df2 = res[topic][2]

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

def create_plots(topics, title,only_influencers=False):
    fig, axs = plt.subplots(len(topics), figsize=(10, 10))
    # add title 
    fig.suptitle(title, fontsize=25)


    for i, topic in enumerate(topics):
        ax = axs[i]
        ax.set_title('Topic: ' + str(topic) + ' - ' + topic_label[topic])
        draw_network(topic, ax, only_influencers=only_influencers)
    plt.tight_layout()
    plt.show()

plot_dip_test(res)
# %%



n_influencers = 30

res = get_polarization_by_layer(n_influencers = n_influencers, n=3)
sorted_topic_label = plot_dip_test(res)

#%%
# Example usage
topics_pol = [t[0] for t in sorted_topic_label[:5]]
topics_not_pol = [t[0] for t in sorted_topic_label[-5:]]
topics_not_pol.reverse()

create_plots(topics_pol, 'most polarized topics' + ' - ' + str(n_influencers) + ' influencers')
create_plots(topics_pol,'most polarized topics' + ' - ' + str(n_influencers) + ' influencers',only_influencers=True)
create_plots(topics_not_pol, 'least polarized topics' + ' - ' + str(n_influencers) + ' influencers')
create_plots(topics_not_pol,'least polarized topics'+' - ' + str(n_influencers) + ' influencers', only_influencers=True)

# %%

# first and last 5 of sorted_topic_label to latex table 


df_topics_label = pd.DataFrame(sorted_topic_label, columns=['topic', 'label'], index=range(1, len(sorted_topic_label)+1))
df_topics_label.head(10)

#%%

# %%
create_plots([0,1,2,3], 'most polarized topics' + ' - ' + str(n_influencers) + ' influencers')



# %%
