import pandas
import seaborn
from matplotlib import pyplot
import preprocess_within
import preprocess_between

from library import my_kruskal

preprocess_within.run()
preprocess_between.run()

for x in range(2):
    if x == 0: data_table = pandas.read_excel('data/data_table_within.xls', sheet_name='data_table', index_col=0)
    if x == 1: data_table = pandas.read_excel('data/data_table_between.xls', sheet_name='data_table', index_col=0)
    data_table['s7'] = ((data_table.s4 + data_table.s5 + data_table.s6) / 3)
    data_table['impact'] = ((data_table.s1 + data_table.s2 + data_table.s3) / 3)
    if x == 0:
        data_table['Design'] = 'within'
        within = data_table
    if x == 1:
        data_table['Design'] = 'between'
        between = data_table

all_data = pandas.concat((between, within))
all_data['Actor'] = all_data['actor']
all_data['Action'] = all_data['action_rank']
all_data['Rating'] = all_data['s7']
all_data['Malady'] = all_data['condition_rank']
# %% Get impact ratings
impact_ratings = all_data.loc[:, ('ResponseId', 'Design', 'Action', 's1', 's2', 's3')]
impact_ratings = pandas.melt(impact_ratings, id_vars=('ResponseId', 'Design', 'Action'))
seaborn.catplot(x='Action', y='value', hue='variable', kind='point', col='Design', data=impact_ratings)
pyplot.show()

impact_ratings = all_data.loc[:, ('ResponseId', 'Design', 'Action', 'impact')]
impact_ratings = pandas.melt(impact_ratings, id_vars=('ResponseId', 'Design', 'Action'))
seaborn.catplot(x='Action', y='value', hue='variable', kind='point', col='Design', data=impact_ratings)
pyplot.show()

# %%
facet_kws = dict(despine=False)

seaborn.set_style('darkgrid')
seaborn.catplot(x='Action', y='Rating', hue='Actor', kind='point', col='Malady', row='Design', facet_kws=facet_kws, data=all_data)
pyplot.ylim(0, 100)
pyplot.tight_layout()
pyplot.show()

subset = all_data.query('action_rank in [0,4]')
subset = subset.query('condition_rank in [0,2]')
seaborn.set_style('darkgrid')
seaborn.catplot(x='Malady', y='Rating', hue='Actor', kind='point', col='Action', row='Design', facet_kws=facet_kws, data=subset)
pyplot.ylim(0, 100)
pyplot.tight_layout()
pyplot.show()

subset = all_data.query('action_rank in [0, 5]')
subset = subset.query('condition_rank in [2]')
seaborn.catplot(x='Action', y='Rating', hue='Actor', kind='point', col='Malady', row='Design', facet_kws=facet_kws, data=subset)
pyplot.ylim(0, 100)
pyplot.tight_layout()
pyplot.show()


r = my_kruskal(all_data, design='between', actions=[0, 4], conditions=[2])
