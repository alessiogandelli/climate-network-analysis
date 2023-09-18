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

def get_influencers(net, n_influencers):
    degree = net.degree()
    sorted_degree = sorted(degree, key=lambda x: x[1], reverse=True)
    influencers = [s[0] for s in sorted_degree[:n_influencers]]
    users = [s[0] for s in sorted_degree[n_influencers:]]
    

    return influencers, users

def get_polarization_by_layer(layers, n_influencers = 30, n = 3):
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

        print(len(connection_df['influencer'].unique()), ' influencers')
        print(len(connection_df['user'].unique()), ' users connected to influencers')
        # create matrix and apply latent ideology
        try:
            li_matrix = li(connection_df)
            df1, df2 = li_matrix.apply_method(n=n,targets='user', sources='influencer')
            # perform dip test on scores
            test = df1['score'].to_numpy()

            dip_res = diptest.diptest(test)
            
            if dip_res[1] < 0.05 and l != -1:
                res[l] = (dip_res, df1, df2)
                res = {int(float(k)): v for k, v in res.items()}
            else:
                print('Layer ', l, ' has too few data to be analyzed with dip test')
        except:
            print('Layer ', l, ' has too few data to be analyzed with latent ideology')
            continue

    
    return res

def plot_dip_test(res, layers ,cop_name='COP'+str(n_cop)):

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
    ax2.bar([str(d[0]) for d in diptest_s], [d[2] for d in diptest_s], color='orange', label='Number of users', alpha=0.7)

    ax2.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    # break ax 2 between 50000 and 90000
 
  # don't put tick labels at the top



    ax2.grid(False)
    # ax 2 opacity
    ax2.patch.set_alpha(0.5)
    
    ax2.set_ylabel('Number of nodes')
    ax.legend(loc='upper left')
    ax2.legend(loc='upper right')

    #bar widht 
    # i want tonly half of the xtiks
    plt.xticks([str(d[0]) for d in diptest_s], [str(d[0]) for d in diptest_s])
    

    plt.xticks([str(d[0]) for d in diptest_s], [str(d[0]) for d in diptest_s])
    plt.xticks(rotation=90)     

    # add mean line to left axes 

    plt.show()


    # print the most and least polarized topics according to this test 

    # sort topic label according to diptest_s mantain keys
    sorted_topic_label = [(k[0], topic_label[k[0]]) for k  in diptest_s]

    print(sorted_topic_label)

    # print 10 most and least polarized topics one per line
    print('Most polarized topics:')
    for i in range(min(10, len(sorted_topic_label))):
        print(sorted_topic_label[i][0], sorted_topic_label[i][1])
    print('')
    print('Least polarized topics:')
    for i in range(min(10, len(sorted_topic_label))):
        print(sorted_topic_label[-i-1][0], sorted_topic_label[-i-1][1])


    return sorted_topic_label



# load data 
n_cop = 26
n_influencers = 100

folder = '/Users/alessiogandelli/data/cop' + str(n_cop) + '/'
projected_path = folder + 'networks/cop' + str(n_cop) +'_retweet_network_ml.gml'
topic_label = json.load(open(folder + 'cache/labels_cop'+str(n_cop)+'.json'))
topic_label = {int(k): v for k, v in topic_label.items()}# key float to int

retweet_df_path = folder + 'cache/retweets_labeled_cop'+str(n_cop)+'.pkl'
tweet_cop26_path = folder + 'cache/tweets_cop26.pkl'

retweet_df = pd.read_pickle(retweet_df_path)
tweet_cop26 = pd.read_pickle(tweet_cop26_path)

mln = ml.read(projected_path)   # multilayer network

layers = ml.to_nx_dict(mln) # dictionary where we have a networkx graph for each layer
layers = {int(float(k)): v for k, v in layers.items()} # key float to int


rt_net_path = folder + 'networks/cop'+str(n_cop)+'_retweet_network.gml' 
rt_net = nx.read_gml(rt_net_path)



#%% filter layers with less then 2000 nodes 

n_nodes = {k: v.number_of_nodes() for k, v in layers.items()}
print('Number of layers: ', len(n_nodes))

# remove layers with less than 2000 nodes and outliers 
n_nodes = {k: v for k, v in n_nodes.items() if v > 2000 and k != -1}

print('Number of layers after filtering: ', len(n_nodes))
layers = {k: v for k, v in layers.items() if k in n_nodes.keys()}

# %%

res = get_polarization_by_layer(layers, n_influencers = 100, n = 2)
sorted_topic_label= plot_dip_test(res, layers)

