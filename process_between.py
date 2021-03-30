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

# seaborn.catplot(x='action_rank', y='s7', hue='actor', col='experiment', data=all, kind='point')
# pyplot.show()
#
# seaborn.catplot(x='condition_rank', y='s7', hue='actor', col='experiment', data=all, kind='point')
# pyplot.show()
# estimator=numpy.mean, ci=Non
#seaborn.catplot(x='actor', y='s7', col='action_rank', hue='experiment', data=all, kind='point')
#pyplot.show()
for x in range(2):
    if x == 0: selected_data = within
    if x == 1: selected_data = between
    grp = selected_data.groupby(['action_rank','condition_rank', 'actor'])
    med = grp.mean()
    med = med['s7']
    med = med.reset_index()
    robot = med.query('actor=="robot"')
    nurse = med.query('actor=="nurse"')

    nurse = nurse.pivot(index='action_rank',columns='condition_rank', values='s7')
    robot = robot.pivot(index='action_rank',columns='condition_rank', values='s7')

    if x==0:
        nurse_within = nurse
        robot_within = robot


    if x==1:
        nurse_between = nurse
        robot_between = robot


pyplot.subplot(2,2,1)
pyplot.imshow(nurse_within)
pyplot.title('nurse_within')
pyplot.clim(20,100)

pyplot.subplot(2,2,2)
pyplot.imshow(robot_within)
pyplot.title('robot_within')
pyplot.clim(20,100)

pyplot.subplot(2,2,3)
pyplot.imshow(nurse_between)
pyplot.title('nurse_between')
pyplot.clim(20,100)

pyplot.subplot(2,2,4)
pyplot.imshow(robot_between)
pyplot.title('robot_between')
pyplot.clim(20,100)

pyplot.show()

d1 = nurse_within-robot_within
d2 = nurse_between-robot_between
r = 40
pyplot.imshow(d1, cmap='bwr')
pyplot.colorbar()
pyplot.clim(-r,r)
pyplot.show()


pyplot.imshow(d2, cmap='bwr')
pyplot.colorbar()
pyplot.clim(-r,r)
pyplot.show()

#%%

# seaborn.catplot(x='condition_rank',y='s7',hue='actor', kind='point',row='action_rank',col='experiment',estimator=numpy.median,ci=None, data=all_data)
# pyplot.ylim(0,100)
# pyplot.show()
#
# seaborn.catplot(x='action_rank',y='s7',data=all_data, kind='point')
# pyplot.ylim(0,100)
# pyplot.show()

seaborn.catplot(x='action_rank',y='s7',hue='actor', kind='point',col='condition_rank',row='experiment', data=all_data)
pyplot.ylim(0,100)
pyplot.show()

