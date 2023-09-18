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

#%%
#load data 
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
#%%

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

def ridge_plot(topics_df, topics, title):
    # get only topic 1,2,3 in the same df
    topics_df = retweet_df[retweet_df['topic'].isin(topics)]

    topics_df['day'] = pd.to_datetime(topics_df['date']).dt.date

    topics_df = topics_df[topics_df['day'] >= pd.to_datetime('2021-10-22').date()]
    topics_df = topics_df[topics_df['day'] <= pd.to_datetime('2021-11-17').date()]

    topics_df['day'] = pd.to_datetime(topics_df['day'])


    # ridge plot 
    # https://seaborn.pydata.org/examples/kde_ridgeplot.html

    # Initialize the FacetGrid object
    pal = sns.cubehelix_palette(10, rot=-.25, light=.7)
    g = sns.FacetGrid(topics_df, row="topic", hue="topic", aspect=8, height=1, palette=pal)

    # set title 
    g.fig.suptitle(title + ' Polarized  over time for cop26', fontsize=25)

    # Draw the densities of the date 
    g.map(sns.kdeplot, "day", clip_on=False, fill=True, alpha=1, lw=1.5, bw_method=.2)
    g.map(sns.kdeplot, "day", clip_on=False, color="w", lw=2, bw_method=.2)
    g.map(plt.axhline, y=0, lw=2, clip_on=False)

    # Define and use a simple function to label the plot in axes coordinates
    def label(x, color, label):
        ax = plt.gca()
        ax.text(0, .2, label, fontweight="bold", color=color,
                ha="left", va="center", transform=ax.transAxes)
        
    g.map(label, "day")

    # Set the subplots to overlap
    g.fig.subplots_adjust(hspace=0.2)

    # Remove axes details that don't play well with overlap
    g.set_titles("")
    g.set(yticks=[])
    g.despine(bottom=True, left=True)

    # hide y label 
    g.set(ylabel='')

    #xlim 
    g.set(xlim=(pd.to_datetime('2021-10-22').date(), pd.to_datetime('2021-11-17').date()))

    # add something to undertline that between 31th october and 12 november there was the cop
    # https://stackoverflow.com/questions/48145929/how-to-add-a-horizontal-line-in-seaborn-ridgeplot

    # add vertical line for cop start for all topics
    for ax in g.axes.flat:
        ax.axvline(x=pd.to_datetime('2021-10-31').date(), color='black', linestyle='--')
        ax.axvline(x=pd.to_datetime('2021-11-12').date(), color='black', linestyle='--')
        ax.tick_params(axis='x', rotation=90)

    

    ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))


    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b-%d'))

    plt.show()

# %%

n_nodes = {k: v.number_of_nodes() for k, v in layers.items()}
print('Number of layers: ', len(n_nodes))

# remove layers with less than 2000 nodes and outliers 
n_nodes = {k: v for k, v in n_nodes.items() if v > 2000 and k != -1}

print('Number of layers after filtering: ', len(n_nodes))
layers = {k: v for k, v in layers.items() if k in n_nodes.keys()}

# %%

res = get_polarization_by_layer(layers, n_influencers = 100, n = 2)

sorted_topic_label= plot_dip_test(res, layers)
# %%
topics_pol = [t[0] for t in sorted_topic_label[:5]]
topics_not_pol = [t[0] for t in sorted_topic_label[-5:]]
topics_not_pol.reverse()

create_plots(topics_pol, 'most polarized topics' + ' - ' + str(n_influencers) + ' influencers')
create_plots(topics_pol,'most polarized topics' + ' - ' + str(n_influencers) + ' influencers',only_influencers=True)
create_plots(topics_not_pol, 'least polarized topics' + ' - ' + str(n_influencers) + ' influencers')
create_plots(topics_not_pol,'least polarized topics'+' - ' + str(n_influencers) + ' influencers', only_influencers=True)



import matplotlib.cbook as cbook
import matplotlib.dates as mdates



# %%


# %%
# get tweets only topic 4 
topic4 = retweet_df[retweet_df['author'] == '164929952']
topic4 =  topic4[topic4['topic'] == 4]


# %%
# t20 analysis 

t20_users = res[20][1]
t20_influencer  = res[20][2]

t20_scores = pd.concat([t20_users, t20_influencer])
t20_scores.rename(columns={'user':'author_name'}, inplace=True)

t20 = retweet_df[retweet_df['topic'] == 20]


# add the score to users 
t20 = t20.merge(t20_scores, on='author_name', how='left')




# %%
#get influencer tweets 
t20_influencer_tweets = t20[t20['author_name'].isin(t20_influencer['source'])]



#%%
influencers, _ = get_influencers(rt_net, n_influencers)





#%% full network 
res = get_polarization_by_layer({1:rt_net}, n_influencers=100, n=4)
create_plots([1,1],'cop26',only_influencers=False )
