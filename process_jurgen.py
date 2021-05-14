import pandas
from library import preprocess_jurgen
import seaborn
from matplotlib import pyplot
preprocess_jurgen.run()

data_table = pandas.read_excel('data/data_table_jurgen.xls', sheet_name='data_table', index_col=0)

grp = data_table.groupby('ResponseId')
accuracy = grp.CQ_correct.mean()
accuracy = accuracy.reset_index()
accuracy.columns = ['ResponseId', 'accuracy']

data_table = pandas.merge(data_table, accuracy, on='ResponseId')
data = data_table.query('accuracy == 1')

seaborn.catplot(x='disease', y='response', col='action', hue='actor', kind='box', data=data_table)

pyplot.ylim((-3, 3))
pyplot.show()