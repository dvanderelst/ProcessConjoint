import pandas
import seaborn
from matplotlib import pyplot
import numpy
from pyBat import Statistics

# rating_data = pandas.read_excel('data/preprocessed_between.xls', sheet_name='rating_data', index_col=0)
#
#
# seaborn.catplot(x='renumbered_scale', y='rating', hue='actor', data=rating_data, col='condition_rank', kind='point')
# pyplot.show()

for x in range(2):
    if x == 0: data_table = pandas.read_excel('data/data_table_within.xls', sheet_name='data_table', index_col=0)
    if x == 1: data_table = pandas.read_excel('data/data_table_between.xls', sheet_name='data_table', index_col=0)
    data_table['s7'] = ((data_table.s4 + data_table.s5 + data_table.s6) / 3)
    if x == 0:
        data_table['experiment'] = 'within'
        within = data_table
    if x == 1:
        data_table['experiment'] = 'between'
        between = data_table

all_data = pandas.concat((between, within))

formula = 's7 ~ s1 + s2 + s3 + C(actor)'
result = Statistics.regression(formula, between)
print(result['summary'])