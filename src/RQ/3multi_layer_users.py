
#%%

import pandas as pd
import seaborn as sns 
import matplotlib.pyplot as plt

# %%
users_df = pd.DataFrame(columns=['target'])
influencers_df = pd.DataFrame(columns=['source'])
res = get_polarization_by_layer(layers, n_influencers = 100, n = 2)

#res = {}
#%%
for topic, r in res.items():
    r[1]['topic'] = topic
    r[2]['topic'] = topic
    users_df = pd.concat([users_df, r[1]], ignore_index=True)
    influencers_df = pd.concat([influencers_df, r[2]], ignore_index=True)


pivot_df = users_df.pivot(index='target', columns='topic', values='score')
inf_df = influencers_df.pivot(index='source', columns='topic', values='score')


#users
pivot_df['avg_score'] = pivot_df.mean(axis=1, numeric_only=True)
pivot_df['n_topics'] = pivot_df.count(axis=1) -1 # exclude avg score
pivot_df['std_score'] = pivot_df.drop(columns=['n_topics', 'avg_score']).std(axis=1)
pivot_df['team'] = pivot_df['avg_score'].apply(lambda x: 1 if x > 0 else -1)

global_avg = pivot_df['avg_score'].mean()



#influencers 
inf_df['avg_score'] = inf_df.mean(axis=1, numeric_only=True)
inf_df['n_topics'] = inf_df.count(axis=1) -1 # exclude avg score
inf_df['std_score'] = inf_df.drop(columns=['n_topics', 'avg_score']).std(axis=1)
inf_df['team'] = inf_df['avg_score'].apply(lambda x: 1 if x > 0 else -1)

# %%
print('sample size', len(inf_df))
print('user present in only one topic', len(inf_df[inf_df['n_topics'] == 1]))
print('user present in more than 10 topics', len(inf_df[inf_df['n_topics'] > 10]))
print('average n of topics', inf_df['n_topics'].mean())

print('average score', inf_df['avg_score'].mean())
print('average std', inf_df['std_score'].mean())






# %% drop except avg_score
# %%


print('sample size', len(pivot_df))
print('user present in only one topic', len(pivot_df[pivot_df['n_topics'] == 1]))
print('user present in more than 10 topics', len(pivot_df[pivot_df['n_topics'] > 10]))
print('average n of topics', pivot_df['n_topics'].mean())

print('average score', pivot_df['avg_score'].mean())
print('average std', pivot_df['std_score'].mean())

# avg std by team 


print('average score for team 1', pivot_df[pivot_df['team'] == 1]['avg_score'].mean())
print('average score for team -1', pivot_df[pivot_df['team'] == -1]['avg_score'].mean())

print('average std for team 1', pivot_df[pivot_df['team'] == 1]['std_score'].mean())
print('average std for team -1', pivot_df[pivot_df['team'] == -1]['std_score'].mean())






# %%


def histogram(df, column, title):

    if column == 'avg_score':
        color = 'blue'
    else:
        color = 'green'

    #histogram
    ax = sns.histplot(df[column], bins=100, kde=True, color=color, alpha=0.5)

    #figsize
    fig = ax.get_figure()
    fig.set_size_inches(7, 3)

    # add title 
    ax.set_title('Distribution of ' + title)


    # save figure
    plt.savefig(title+'.png', dpi=300)

# %%

histogram(pivot_df, 'avg_score', 'average score')
histogram(pivot_df, 'std_score', 'std score')

histogram(inf_df, 'avg_score', 'average score influencers')
histogram(inf_df, 'std_score', 'std score influencers')
# %%
