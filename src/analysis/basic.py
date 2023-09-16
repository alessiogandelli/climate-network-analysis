#%%
import networkx as nx
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import uunet.multinet as ml
import json
import plotly.express as px


def get_basic_stats(cop):

        #paths
    folder = '/Users/alessiogandelli/data/cop' + str(cop) + '/'

    retweet_network_path = folder + 'networks/cop'+str(cop)+'_retweet_network.gml'
    retweet_df_path = folder + 'cache/retweets_labeled_cop'+str(cop)+'.pkl'
    # load networks and df 
    #tweets_df = pd.read_pickle(tweets_df_path)
    rt_net = nx.read_gml(retweet_network_path)
    retweets_df = pd.read_pickle(retweet_df_path)




    indegree = dict(rt_net.in_degree())

    #get top 1000 influencers
    sorted_indegree = sorted(indegree.items(), key=lambda x: x[1], reverse=True)
    influencers = [s[0] for s in sorted_indegree[:1000]]
    users = [s[0] for s in sorted_indegree[1000:]]

    retweets_df['indegree'] = retweets_df['author'].map(indegree)



    #number of tweets per user 

    n_of_tweets_by_user(retweets_df, cop)


    tweet_user_stats(retweets_df, cop)


    plot_tweets_by_date(retweets_df, cop)



def plot_tweets_by_date(retweets_df, cop):

    retweets_df['date'] = pd.to_datetime(retweets_df['date'])
    retweets_df['day'] = retweets_df['date'].dt.date
    retweets_df['month-year'] = retweets_df['date'].dt.to_period('M')

    gr = retweets_df.groupby('month-year').count()['author']
    min_date = retweets_df['date'].min()
    max_date = retweets_df['date'].max()

    print('Min date: ', min_date)
    print('Max date: ', max_date)

    plt.figure(figsize=(10,3))
    #barplot
    # index to string 
    gr.index = gr.index.astype(str)
    plt.bar(gr.index, gr.values)

    plt.xlabel('Month')
    plt.ylabel('Number of tweets')
    plt.title('Number of tweets by date for COP' + str(cop))

    #write all xticks 
    plt.xticks(gr.index, rotation=90, fontsize=8)

    plt.grid()
    # add % of tweets
    for i in range(len(gr)):
        plt.annotate(str(round(gr.values[i]/gr.sum()*100,2)) + '%', xy=(i, gr.values[i]), ha='center', va='bottom', fontsize=8)
    plt.show()


def n_of_tweets_by_user(retweets_df, cop):
    tweets_per_user = retweets_df.groupby('author').count()['text'].value_counts().head(50)

    print(sum(tweets_per_user[:5]) / sum(tweets_per_user), ' of users have less than 5 tweets')
    print(retweets_df.groupby('author').count()['text'].describe().round(2))

    plt.figure(figsize=(12,4))
    plt.bar(tweets_per_user.index, tweets_per_user.values)
    plt.xlabel('Number of tweets')
    plt.ylabel('Number of users')
    plt.title('Number of tweets by user for COP' + str(cop))
    plt.grid()
    plt.yscale('log')
    plt.show()


def tweet_user_stats(retweets_df, cop):

    n_tweets = len(retweets_df)
    n_users = len(retweets_df['author'].unique())
    n_original_tweets = len(retweets_df[retweets_df['referenced_type'].isna()])
    n_retweets = len(retweets_df[retweets_df['referenced_type'] == 'retweeted'])
    n_original_with_retweets = len(retweets_df[retweets_df['referenced_type'] == 'retweeted'].groupby('referenced_id').count())
    n_original_without_retweets = n_original_tweets - n_original_with_retweets

        #referenced df 
    rdf = retweets_df[retweets_df['referenced_type'].isna()]
    rdf = rdf[rdf['indegree'] > 0]

    n_original_users = len(retweets_df[retweets_df['referenced_type'].isna()]['author'].unique())
    n_original_users_with_retweets = len(rdf.groupby('author').count())

    print('Number of tweets: ', n_tweets)
    print('Number of original tweets: ', n_original_tweets)
    print('Number of original tweets with retweets: ', n_original_with_retweets)
    print('Number of retweets: ', n_retweets)
    print()
    print('Number of users: ', n_users)
    print('Number of users that posted original tweets: ', n_original_users)
    print('Number of users that posted original tweets with retweets: ', n_original_users_with_retweets)



    fig = px.treemap(
    names = ["Tweets", "Retweets", "Original", "with retweet", "without retweets"],
    parents = ["", "Tweets", "Tweets", "Original", "Original"],
    values = [n_tweets, n_retweets, n_original_tweets, n_original_with_retweets, n_original_without_retweets],
    branchvalues = "total",
    title = "Number of tweets"

    )
    # add textinfo 
    fig.update_traces(textinfo="label+value+percent parent")


    fig.update_traces(root_color="lightgrey")
    fig.update_layout(margin = dict(t=0, l=0, r=0, b=0))
    fig.show()


    fig = px.treemap(
        names = ["Users", "Original", "with retweet", "without retweets"],
        parents = ["", "Users", "Original", "Original"],
        values = [n_users, n_original_users, n_original_users_with_retweets, n_original_users - n_original_users_with_retweets],
        branchvalues = "total"
    )
    fig.update_traces(root_color="lightgrey")
    fig.update_layout(margin = dict(t=0, l=0, r=0, b=0))
    fig.show()

#%%

get_basic_stats(26)
# %%
