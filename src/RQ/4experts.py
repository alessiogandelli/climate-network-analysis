
#%%

mono_topic_users = pivot_df[pivot_df['n_topics'] == 1]

poli_topic_users = pivot_df[pivot_df['n_topics'] > 1]
# %%
pivot_df['type'] = pivot_df['n_topics'].apply(lambda x: 'mono' if x == 1 else 'poli')

# visuzlize avg score of mono topic users and poli topic users

sns.distplot(mono_topic_users['avg_score'], label='mono topic users')
sns.distplot(poli_topic_users['avg_score'], label='poli topic users')
plt.legend()
plt.show()

# check if it is statistically significant difference


# %%

# team distribution heatmap percentace 

tt = pivot_df.groupby(['team', 'type']).mean()

# %%
tt['avg_topic'] = tt.drop(columns=['avg_score', 'n_topics', 'std_score']).mean(axis=1, numeric_only=True)
# %%

monomean = mono_topic_users.mean()

# %%
polimean = poli_topic_users.mean()
# %%
