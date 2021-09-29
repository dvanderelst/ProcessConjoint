import pandas
import seaborn
from matplotlib import pyplot
from library import PlotSettings
from library import preprocess_simple
from pyBat import Statistics

preprocess_simple.run()

data_table = pandas.read_excel('data/data_table_simple.xls', sheet_name='data_table', index_col=0)
data_table = data_table.replace("Not permissible",'Not Permissible')

data_table['binary'] = data_table['value'] == 'Not Permissible'

# Add proper labels for plotting with seaborn
data_table['Actor'] = data_table['actor']
data_table['Action'] = data_table['action_short']
data_table['Rating'] = data_table['binary'] * 1

formula = "Rating ~ Action + Actor"
result = Statistics.regression(formula, data=data_table, typ='log')
summary = result['summary']
f = open(PlotSettings.output_file('LM_simple.txt'), 'w')
f.write(summary.as_text())
f.close()

f = open(PlotSettings.output_file('LM_simple.tex'), 'w')
f.write(result['latex'])
f.close()

PlotSettings.copy_output()


#%% on to the demographics
demo = pandas.read_excel('data/preprocessed_simple.xls', sheet_name='demo_data', index_col=0)
selected_pp = list(data_table.ResponseId)
demo = demo.query('ResponseId in @selected_pp')
demo.to_csv('demographic_data/simple.csv', index=False)


#%%
grp = data_table.groupby(['Action','Actor','value'])
cnt = grp.ResponseId.count()
cnt = cnt.reset_index()

g = seaborn.catplot(x='Action',y='ResponseId',col='value', hue='Actor',
                palette=[PlotSettings.black, PlotSettings.grey],
                facet_kws=PlotSettings.facet_kws,
                kind='bar', data=cnt, order=PlotSettings.short_order)
axes = g.axes.flatten()
g.set_xticklabels(rotation=30)
pyplot.tight_layout()

pyplot.savefig(PlotSettings.output_file('simple.pdf'))
pyplot.show()
PlotSettings.copy_output()

t = cnt.pivot(index='Action',columns=('Actor', 'value'),values='ResponseId')