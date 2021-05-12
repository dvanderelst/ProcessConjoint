import pandas
from library import preprocess_jurgen
import seaborn
from matplotlib import pyplot
preprocess_jurgen.run()

data_table = pandas.read_excel('data/data_table_jurgen.xls', sheet_name='data_table', index_col=0)

seaborn.catplot(x='disease', y='response', col='action', hue='actor', kind='point', data=data_table)
pyplot.ylim((-3, 3))
pyplot.show()