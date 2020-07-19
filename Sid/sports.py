import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

import os

plt.style.use('ggplot')

filepath = os.path.abspath('london_sports_participation_cleaned.csv')
sports_df = pd.read_csv(filepath)
#print(sports_df)

years = sports_df['year'].unique().tolist()
ind = np.arange(len(years))

regions = sports_df['area'].unique().tolist()
#non_regions = ['East Midlands', 'East', 'England', 'London', 'North East', 'North West', 'South East', 'South West', 'West Midlands', 'Yorkshire', 'Yorkshire And The Humber']
#[regions.remove(non_region) for non_region in non_regions]

significant_regions = []

for region in regions:
    region_df = sports_df.loc[sports_df['area'] == region]
    zeroes = np.array(region_df[region_df['sports_participation'] == 0]['percentage'].tolist())
    ones = np.array(region_df[region_df['sports_participation'] == 1]['percentage'].tolist())
    threes = np.array(region_df[region_df['sports_participation'] == 2]['percentage'].tolist())
    #ones = ones - threes
    
    plt.bar(ind, zeroes, width=0.8, label='0', color='red')
    plt.bar(ind, ones, width=0.8, label='1-2', color='green', bottom=zeroes)
    plt.bar(ind, threes, width=0.8, label='3+', color='blue', bottom=zeroes+ones)

    plt.xticks(ind, years, rotation=30, fontsize='small')
    plt.ylabel('Percentages')
    plt.xlabel('Years')
    plt.legend(loc='upper right')
    plt.title(region + ' Region Sports Participation')

    plt.savefig(region + '.png')
    plt.show()

    '''
    zeroes_before = zeroes[0:5]
    zeroes_after = zeroes[5:]
    ones_before = ones[0:5]
    ones_after = ones[5:]
    threes_before = threes[0:5]
    threes_after = threes[5:]

    zeroes_ttest = stats.ttest_ind(zeroes_before, zeroes_after)
    ones_ttest = stats.ttest_ind(ones_before, ones_after)
    threes_ttest = stats.ttest_ind(threes_before, threes_after)

    if(zeroes_ttest[1] < 0.05):
        significant_regions.append((region, 'zeroes', ('decrease' if zeroes_ttest[0] < 0 else 'increase', zeroes_ttest[1])))
    if(ones_ttest[1] < 0.05):
        significant_regions.append((region, 'ones', ('decrease' if ones_ttest[0] < 0 else 'increase', ones_ttest[1])))
    if(threes_ttest[1] < 0.05):
        significant_regions.append((region, 'threes', ('decrease' if threes_ttest[0] < 0 else 'increase', threes_ttest[1])))

print(significant_regions)
'''