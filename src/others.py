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
