import matplotlib.patches as patches
import pandas
import seaborn
from matplotlib import pyplot
from library import PlotSettings
from library import preprocess_simple_amazon, misc
from pyBat import Statistics
import pingouin as pg
import sys, io

preprocess_simple_amazon.run()

demo = pandas.read_excel('data/preprocessed_simple_amazon.xls', sheet_name='demo_data', index_col=0)
accuracy = pandas.read_excel('data/preprocessed_simple_amazon.xls', sheet_name='accuracy', index_col=0)

data_table = pandas.read_excel('data/data_table_simple_amazon.xls', sheet_name='data_table', index_col=0)
data_table = data_table.replace("Not permissible",'Not Permissible')
data_table = data_table.merge(demo, on='ResponseId')
data_table['Age'] = 2021 - data_table.BirthYear.astype(float)
data_table = data_table.query('attention_correct_y > 0.8')

# Add mapping
mapping = {'value': ['Not Permissible', 'Unsure', 'Permissible'], 'Rating': [-1,0,1]}
mapping = pandas.DataFrame(mapping)
data_table = data_table.merge(mapping, on='value', how='left')

# Add proper labels for plotting with seaborn
data_table['Actor'] = data_table['actor']
data_table['Action'] = data_table['action_short']

# Export to CSV for potential processing in R
data_table.to_csv('data/simple_amazon_for_R.csv', index=False)

#%%
data_table['Binary'] = (data_table['Rating'] == 1) * 1.0
formula = "Binary ~ Action + Actor"
result = Statistics.regression(formula, data=data_table, typ='log')
summary = result['summary']

f = open(PlotSettings.output_file('LM_simple_amazon.txt'), 'w')
f.write(summary.as_text())
f.close()

f = open(PlotSettings.output_file('LM_simple_amazon.tex'), 'w')
f.write(misc.clean_summary(result['latex']))
f.close()

## using pingoiun for within results
# result = pg.rm_anova(data=data_table,dv='Rating',within=['Actor','Action'], subject='ResponseId', detailed=False)
# old_stdout = sys.stdout
# new_stdout = io.StringIO()
# sys.stdout = new_stdout
# pg.print_table(result, tablefmt='latex')
# output = new_stdout.getvalue()
# sys.stdout = old_stdout


#%% on to the demographics
demo = pandas.read_excel('data/preprocessed_simple_amazon.xls', sheet_name='demo_data', index_col=0)
selected_pp = list(data_table.ResponseId)
demo = demo.query('ResponseId in @selected_pp')
demo.to_csv('demographic_data/simple_amazon.csv', index=False)

#%% Make graph

#Export data for final figure
data_table.to_csv('data/simple_amazon_for_final.csv', index=False)
n_respondents = len(data_table.ResponseId.unique())

grp = data_table.groupby(['Action','Actor','value'])
cnt = grp.ResponseId.count()
cnt = cnt.reset_index()
cnt['Proportion'] = cnt['ResponseId']/n_respondents


cnt = cnt.assign(Actor=cnt.Actor.map({'nurse': 'Nurse', 'robot': "Robot"}))

g = seaborn.catplot(x='Action',y='Proportion',col='value', hue='Actor',
                    palette=PlotSettings.colors,
                    facet_kws=PlotSettings.facet_kws,
                    kind='point', data=cnt,
                    markers = PlotSettings.markers,
                    linestyles=PlotSettings.lines,
                    order=PlotSettings.short_order,
                    legend=False,
                    col_order=['Not Permissible', 'Unsure', 'Permissible'])

pyplot.legend(loc='lower right')

pyplot.ylim(0,1)
axes = g.axes.flatten()
pyplot.sca(axes[2])
rect = patches.Rectangle((-0.25, 0.1), 2.5, 0.6, linewidth=3, alpha=0.5, edgecolor='r', facecolor='none')
pyplot.gca().add_patch(rect)

g.set_xticklabels(rotation=90)
g.set_titles(template='Response: {col_name}')
PlotSettings.spine(g)
pyplot.tight_layout()

pyplot.savefig(PlotSettings.output_file('simple_amazon.pdf'))
pyplot.show()
PlotSettings.copy_output()