import pandas
from library import preprocess_student
import seaborn
from matplotlib import pyplot
preprocess_student.run()

data_table = pandas.read_excel('data/data_table_student.xls', sheet_name='data_table', index_col=0)

seaborn.catplot(x='actor', y='numeric_response', kind='point', data=data_table)
pyplot.ylim(0,6)
pyplot.show()