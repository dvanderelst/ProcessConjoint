import pandas
import seaborn
from matplotlib import pyplot

from pyBat import Statistics

rating_data = pandas.read_excel('data/preprocessed_within.xls', sheet_name='rating_data', index_col=0)


seaborn.catplot(x='renumbered_scale', y='rating', hue='actor', data=rating_data, col='condition_rank', kind='point')
pyplot.show()



# import pandas
# import seaborn
# from matplotlib import pyplot
#
# from pyBat import Statistics
#
# data_table = pandas.read_excel('data_table.xls', sheet_name='data_table', index_col=0)
# data_table['s7'] = ((data_table.s4 + data_table.s5 + data_table.s6) / 300)
#
# grp = data_table.groupby('ResponseId')
# stats = grp.agg({'s1': ['mean', 'std'], 's2': ['mean', 'std'], 's3': ['mean', 'std'], 's7': ['mean', 'std']})
# stats = stats.reset_index()
#
# data_table = data_table.merge(stats, on='ResponseId')
# data_table = data_table.dropna()
#
# data_table['s1z'] = (data_table['s1'] - data_table[('s1', 'mean')]) / data_table[('s1', 'std')]
# data_table['s2z'] = (data_table['s2'] - data_table[('s2', 'mean')]) / data_table[('s2', 'std')]
# data_table['s3z'] = (data_table['s3'] - data_table[('s3', 'mean')]) / data_table[('s3', 'std')]
# data_table['s7z'] = (data_table['s7'] - data_table[('s7', 'mean')]) / data_table[('s7', 'std')]
# data_table = data_table.dropna()
#
# #%%
#
# seaborn.catplot(x='ResponseId', y='s7z', hue='actor', data=data_table, kind='point')
# pyplot.show()
#
# seaborn.catplot(x='action_rank', col='condition_rank', y='s2z', hue='actor', data=data_table, kind='point')
# pyplot.show()
#
# seaborn.catplot(x='action_rank', col='condition_rank', y='s3z', hue='actor', data=data_table, kind='point')
# pyplot.show()
#
