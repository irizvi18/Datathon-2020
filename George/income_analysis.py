import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt

df = pd.read_csv('london_taxpayer_income.csv', header=0)
london_boroughs = {'Kensington and Chelsea', 'Lambeth', 'Hammersmith and Fulham',
    'Westminster', 'Richmond-upon-Thames', 'Havering', 'Camden', 'Ealing', 'Brent', 
    'Bexley', 'Waltham Forest', 'Redbridge', 'Sutton', 
    'Kingston-upon-Thames', 'Croydon', 'Lewisham', 'Haringey', 'Merton', 
    'Islington', 'Wandsworth', 'Bromley', 'Southwark', 'Greenwich', 'Hillingdon', 
    'Hackney', 'Newham', 'Enfield', 'Tower Hamlets', 'Hounslow', 
    'Barking and Dagenham', 'Barnet', 'Harrow'}

df = df[(df['area'].isin(london_boroughs)) & (df['year'] == '2011-2012')]
#df = df[(df['area_code'].str.len() == 4) & (df['year'] == '2011-2012')]
df = df.sort_values('median_income').reset_index(drop=True)
df.iloc[24, 2] = 'Kingston upon Thames'
df.iloc[29, 2] = 'Richmond upon Thames'
print(df)

map_df = gpd.read_file('statistical-gis-boundaries-london/statistical-gis-boundaries-london/ESRI/London_Borough_Excluding_MHW.shp')
map_df = map_df.sort_values('NAME').reset_index(drop=True)

#upper_f = lambda x: " ".join([w[0].upper() + w[1:] for w in x.split(" ")])
#map_df['NAME'] = map_df['NAME'].apply(upper_f)

merged = map_df.set_index('NAME').join(df.set_index('area'), how='inner')

vmin, vmax = 0, max(df['median_income'])
merged.plot(column='median_income', cmap='Greens', linewidth=0.8, edgecolor='0.8')
plt.axis('off')
plt.title('2011-2012 Median Individual Income, (£)')
sm = plt.cm.ScalarMappable(cmap='Greens', norm=plt.Normalize(vmin=vmin, vmax=vmax))
sm._A = []
cbar = plt.colorbar(sm)
plt.show()

