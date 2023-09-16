#%%
import pandas as pd 
import matplotlib.pyplot as plt

#ignore first row
greta_df = pd.read_csv('/Users/alessiogandelli/dev/uni/climate-network-analysis/greta.csv', skiprows=1)
# rename columns to month and value 
greta_df.columns = ['month', 'value']
# convert month to datetime
greta_df['month'] = pd.to_datetime(greta_df['month'])

# convert <1 to 0
greta_df['value'] = greta_df['value'].replace('< 1', 0)

#value to int
greta_df['value'] = greta_df['value'].astype(int)


climate_crisis_df = pd.read_csv('/Users/alessiogandelli/dev/uni/climate-network-analysis/climate_crisis.csv', skiprows=1)
# rename columns to month and value
climate_crisis_df.columns = ['month', 'value']
# convert month to datetime
climate_crisis_df['month'] = pd.to_datetime(climate_crisis_df['month'])

# convert <1 to 0
climate_crisis_df['value'] = climate_crisis_df['value'].replace('< 1', 0)

#value to int
climate_crisis_df['value'] = climate_crisis_df['value'].astype(int)



# %%
#plot 
plt.figure(figsize=(10, 5))
plt.title('Greta Thunberg popularity on Google')
plt.plot(greta_df['month'], greta_df['value'])

#make the plot more sceintific
plt.xlabel('Time')
plt.ylabel('Popularity')
plt.grid()

# add a note in november 21 with cop26 x is a datetime
plt.axvline(x=pd.to_datetime('2021-11-01'), color='r', linestyle='--')
plt.text(pd.to_datetime('2021-04-01'), 50, 'COP26', rotation=0)

# march 2019 first climate strike 
plt.axvline(x=pd.to_datetime('2019-03-01'), color='r', linestyle='--')
plt.text(pd.to_datetime('2017-11-01'), 50, 'First climate strike', rotation=0)

#sep 19 UN speech
plt.axvline(x=pd.to_datetime('2019-09-01'), color='r', linestyle='--')
plt.text(pd.to_datetime('2019-10-01'), 80, 'UN speech', rotation=0)


plt.legend()
plt.show()
# %%

# climate crisis plot 
plt.figure(figsize=(10, 5))
plt.title('Climate crisis popularity on Google')
plt.plot(climate_crisis_df['month'], climate_crisis_df['value'])

#make the plot more sceintific
plt.xlabel('Time')
plt.ylabel('Popularity')
plt.grid()

# add a note in november 21 with cop26 x is a datetime


plt.show()
# %%
#put the two plot together
plt.figure(figsize=(10, 5))
plt.title('Greta Thunberg and climate crisis popularity on Google')
plt.plot(greta_df['month'], greta_df['value'], label='Greta Thunberg')
plt.plot(climate_crisis_df['month'], climate_crisis_df['value'], label='Climate crisis')

#make the plot more sceintific
plt.xlabel('Time')
plt.ylabel('Popularity')
plt.grid()

# add a note in november 21 with cop26 x is a datetime
plt.axvline(x=pd.to_datetime('2021-11-01'), color='r', linestyle='--')
plt.text(pd.to_datetime('2021-04-01'), 50, 'COP26', rotation=0)

# march 2019 first climate strike
plt.axvline(x=pd.to_datetime('2019-03-01'), color='r', linestyle='--')
plt.text(pd.to_datetime('2017-11-01'), 50, 'First climate strike', rotation=0)

#sep 19 UN speech
plt.axvline(x=pd.to_datetime('2019-09-01'), color='r', linestyle='--')
plt.text(pd.to_datetime('2019-10-01'), 80, 'UN speech', rotation=0)

plt.legend()

plt.savefig('greta_climate_crisis.png', dpi=300)

# save the plot in a latex friendly way  
plt.savefig('greta_climate_crisis.pdf', dpi=300)
# %%
