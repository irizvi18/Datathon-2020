import itertools
from pprint import pprint
import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt

sports_df = pd.read_csv('london_sports_participation.csv', header=0)
london_boroughs = {'Kensington And Chelsea', 'Lambeth', 'Hammersmith And Fulham',
    'Westminster', 'Richmond Upon Thames', 'Havering', 'Camden', 'Ealing', 'Brent', 
    'Bexley', 'Waltham Forest', 'City Of London', 'Redbridge', 'Sutton', 
    'Kingston Upon Thames', 'Croydon', 'Lewisham', 'Haringey', 'Merton', 
    'Islington', 'Wandsworth', 'Bromley', 'Southwark', 'Greenwich', 'Hillingdon', 
    'Hackney', 'Newham', 'Enfield', 'Tower Hamlets', 'Hounslow', 
    'Barking And Dagenham', 'Barnet', 'Harrow'}
#london_boroughs.add('London')

sports_df = sports_df[sports_df['area'].isin(london_boroughs)].reset_index(drop=True)

sports_df['sports_participation'].replace({
    "zero": 0,
    "one+": 1,
    "three+": 2}, inplace=True)

sports_df['year'] = sports_df['year'].apply(lambda x: int(x[:4]))
sports_df = sports_df.dropna()
sports_df = sports_df.sort_values(['area', 'year', 'sports_participation'])

mod_df = pd.DataFrame(columns=['area', 'year', 'area_code', 'sports_participation', 'percentage'])

for name, group in sports_df.groupby(['area', 'year']):
    if len(group) == 3:
        group = group.loc[:, ['area', 'year', 'area_code', 'sports_participation', 'percentage']].reset_index(drop=True)
        group.loc[1, 'percentage'] -= group.loc[2, 'percentage']
        response_rate = group['percentage'].sum()
        group['percentage'] /= response_rate
        mod_df = mod_df.append(group)
mod_df = mod_df.reset_index(drop=True)

sports_wm = lambda x: np.average(x, weights=[0, 0.5, 1])
modd_df = mod_df.loc[::3, ['area', 'year', 'area_code']].reset_index(drop=True)
modd_df['sports_index'] = mod_df.groupby(['area', 'year'], as_index=False).agg(sports_index=('percentage', sports_wm)) * 1.5

# london_sports = modd_df[modd_df['area'] == 'London']['sports_index'].to_list()
# plt.plot(np.arange(2006, 2016), london_sports)
# plt.xlabel('Year')
# plt.ylabel('Sports Participation Index (SPI)')
# plt.title('London SPI Over Time')
# plt.ylim((0, 0.5))
# plt.xticks((range(2006, 2016)))
# plt.show()
# exit()

p_vals = {}

def do_perm_test(year_low, year_high, data):
    data = data.set_index('year')
    n_years = year_high - year_low + 1
    n_years_comp = len(data) - n_years
    test_stat = sum(data.loc[year_low:year_high, 'sports_index']) / n_years \
        - sum(data.drop(index=np.arange(year_low, year_high+1))['sports_index']) / n_years_comp
    all_stats = []
    for comb in itertools.combinations([2005, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015], n_years):
        stat = sum(data.loc[comb, 'sports_index']) / n_years \
            - sum(data.drop(index=list(comb))['sports_index']) / n_years_comp
        all_stats.append(stat)
    all_stats = np.array(all_stats)
    return np.sum(all_stats >= test_stat) / len(all_stats)

def do_t_test(year, data):
    pass

for name, group in modd_df.groupby('area'):
    p_vals[name] = do_perm_test(2011, 2015, group)

sig = [(x, y) for x,y in p_vals.items() if y < 0.05]
print(sig)

p_df = pd.DataFrame(list(p_vals.items()), columns=['NAME', 'p_vals'])

map_df = gpd.read_file('statistical-gis-boundaries-london/statistical-gis-boundaries-london/ESRI/London_Borough_Excluding_MHW.shp')
map_df = map_df.sort_values('NAME').reset_index(drop=True)
upper_f = lambda x: " ".join([w[0].upper() + w[1:] for w in x.split(" ")])
map_df['NAME'] = map_df['NAME'].apply(upper_f)

merged = map_df.set_index('NAME').join(p_df.set_index('NAME'), how='inner')

vmin, vmax = 0, 1
merged.plot(column='p_vals', cmap='Blues', linewidth=0.8, edgecolor='0.8')
plt.axis('off')
plt.title('p-values for Sig Increase in Sports Participation')
sm = plt.cm.ScalarMappable(cmap='Blues', norm=plt.Normalize(vmin=vmin, vmax=vmax))
sm._A = []
cbar = plt.colorbar(sm)
plt.show()
