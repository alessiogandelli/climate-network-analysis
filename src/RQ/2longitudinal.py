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

retweet_df = pd.read_pickle(retweet_df_path)

# drop cop 22
retweet_df = retweet_df[retweet_df['cop'] != 'cop22']

# drop topic -1
retweet_df = retweet_df[retweet_df['topic'] != -1]

# get only topics with more than 1000 tweets
retweet_df = retweet_df.groupby('topic').filter(lambda x: len(x) > 1000)

# %%
cop_topic = retweet_df.groupby(['cop','topic']).count()['author'].reset_index()

# heatmap
cop_topic = cop_topic.pivot(index='cop', columns='topic', values='author')

#normalize columns so the sum of the column is 1
cop_topic = cop_topic.div(cop_topic.sum(axis=0), axis=1)

#%% !!!!!! this is good 
################################################################
# divergin bar plot cop21 one side cop26 the other side
import matplotlib.pyplot as plt
import pandas as pd

# Assuming df is your DataFrame
df_transposed = cop_topic.transpose().sort_values(by='cop26', ascending=False).reset_index()

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
# %%
# Import the libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Grouping and Aggregating the Data
cop_topic = retweet_df.groupby(['cop','topic']).count()['author']

# Unstack
cop_topic_df = cop_topic.unstack(level=0)

# Calculate the difference
cop_topic_df['difference'] = cop_topic_df['cop26'] - cop_topic_df['cop21']
cop_topic_df['percentage_diff'] = (cop_topic_df['difference'] / cop_topic_df['cop21']) * 100
cop_topic_df['percentage_total_cop21'] = (cop_topic_df['cop21'] / cop_topic_df['cop21'].sum()) * 100
cop_topic_df['percentage_total_cop26'] = (cop_topic_df['cop26'] / cop_topic_df['cop26'].sum()) * 100

# Sort the DataFrame
cop_topic_df = cop_topic_df.sort_values(by='percentage_diff')

# Create the diverging bar chart
plt.figure(figsize=(10,8)) # Set the figure size
sns.set_theme(style="whitegrid") # Set the theme
chart = sns.barplot(x=cop_topic_df.index, y=cop_topic_df['percentage_diff'], palette="vlag")
plt.xlabel('Topic') # Set the x-axis label
plt.ylabel('Difference') # Set the y-axis label
plt.title('Difference in author count between COP26 and COP21 by topic') # Set the title
sns.despine(left=True, bottom=True) # Remove the top and right borders

# Show the chart
plt.show()
# %%
# stacked bar chart with percentages


cop_topic_df['percentage_total_cop21'] = (cop_topic_df['cop21'] / cop_topic_df['cop21'].sum()) * 100
cop_topic_df['percentage_total_cop26'] = (cop_topic_df['cop26'] / cop_topic_df['cop26'].sum()) * 100

# one bar for each cop with topics stacked 
plt.figure(figsize=(10,8)) # Set the figure size

# Set the theme


# %%
# diverging bar chart with percentages

# Sort the DataFrame




# %%
# Import the libraries
import pandas as pd
import plotly.graph_objects as go

# Grouping and Aggregating the Data
cop_topic = retweet_df.groupby(['cop','topic']).count()['author']

# Unstack
cop_topic_df = cop_topic.unstack(level=0)

# Calculate the difference
cop_topic_df['difference'] = cop_topic_df['cop26'] - cop_topic_df['cop21']
cop_topic_df['percentage_diff'] = (cop_topic_df['difference'] / cop_topic_df['cop21']) 

# Sort the DataFrame
cop_topic_df = cop_topic_df.sort_values(by='percentage_diff')

# Create the diverging bar chart
fig = go.Figure()

fig.add_trace(go.Bar(
    x=cop_topic_df.index,
    y=cop_topic_df['percentage_diff'],
    marker=dict(
        color=cop_topic_df['percentage_diff'],
        colorscale='Bluered_r'
    ),
    name='Difference'
))

fig.update_layout(
    title_text='Difference in author count between COP26 and COP21 by topic',
    xaxis_title='Topic',
    yaxis_title='Difference',
    bargap=0.2,
    bargroupgap=0.1
)

# Show the chart
fig.show()
# %%



# %%
# violin plot 
# https://plotly.com/python/violin/

# Set the title
# %%
