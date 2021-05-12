import pandas
from matplotlib import pyplot

from library import preprocess_simple

actions = ["accept Roberts's decision to not take the medication",
           "notify a trusted person selected by Robert",
           "notify Robert's doctor about his decision",
           "repeat the request to take the medication",
           "refuse to serve dinner until the medication is taken",
           "to not let Robert watch TV,5,2"]

action_nr = ['1', '2', '3', '4', '5', '6']
action_table = pandas.DataFrame({'actions': actions, 'action_nr': action_nr})

preprocess_simple.run()

data_table = pandas.read_excel('data/data_table_simple.xls', sheet_name='data_table', index_col=0)
data_table['binary'] = data_table['value'] == 'Permissible'

grp = data_table.groupby(['actor', 'action_nr'])
mns = grp.binary.mean()
mns = mns.reset_index()

mns = mns.pivot(index='action_nr', columns='actor', values='binary')

pyplot.plot(mns,'o-')
pyplot.legend(['nurse', 'robot'])
pyplot.show()
