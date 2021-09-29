import pandas
import seaborn
import sys, io
from matplotlib import pyplot
from library import PlotSettings
from library import preprocess_simple_amazon, misc
from pyBat import Statistics
import matplotlib.patches as patches
import pingouin as pg

preprocess_simple_amazon.run()

demo = pandas.read_excel('data/preprocessed_simple_amazon.xls', sheet_name='demo_data', index_col=0)


accuracy = pandas.read_excel('data/preprocessed_simple_amazon.xls', sheet_name='accuracy', index_col=0)
pyplot.hist(accuracy.attention_correct)
pyplot.show()

data_table = pandas.read_excel('data/data_table_simple_amazon.xls', sheet_name='data_table', index_col=0)
data_table = data_table.replace("Not permissible",'Not Permissible')
data_table = data_table.merge(demo, on='ResponseId')
data_table['Age'] = 2021 - data_table.BirthYear.astype(float)
data_table['Young'] = data_table['Age'] < 33

data_table['binary'] = (data_table['value'] == 'Permissible') * 1
data_table['invert_binary'] = (data_table['value'] == 'Not Permissible') * 1
#%%
data_table = data_table.query('attention_correct_y > 0.8')

# Add proper labels for plotting with seaborn
data_table['Actor'] = data_table['actor']
data_table['Action'] = data_table['action_short']
data_table['Rating'] = data_table['binary'] * 1

formula = "Rating ~ Action + Actor"
result = Statistics.regression(formula, data=data_table, typ='log')
summary = result['summary']


f = open(PlotSettings.output_file('LM_simple_amazon.txt'), 'w')
f.write(summary.as_text())
f.close()

f = open(PlotSettings.output_file('LM_simple_amazon.tex'), 'w')
f.write(misc.clean_summary(result['latex']))
f.close()


# using pingoiun for within results
result = pg.rm_anova(data=data_table,dv='Rating',within=['Actor','Action'], subject='ResponseId', detailed=True)
old_stdout = sys.stdout
new_stdout = io.StringIO()
sys.stdout = new_stdout
pg.print_table(result, tablefmt='latex')
output = new_stdout.getvalue()
sys.stdout = old_stdout


PlotSettings.copy_output()


#%% on to the demographics
demo = pandas.read_excel('data/preprocessed_simple_amazon.xls', sheet_name='demo_data', index_col=0)
selected_pp = list(data_table.ResponseId)
demo = demo.query('ResponseId in @selected_pp')
demo.to_csv('demographic_data/simple_amazon.csv', index=False)


#%%
grp = data_table.groupby(['Action','Actor','Young','value'])
cnt = grp.ResponseId.count()
cnt = cnt.reset_index()
seaborn.set_style(PlotSettings.style)
seaborn.set(PlotSettings.rc)
g = seaborn.catplot(x='Action',y='ResponseId',col='value', hue='Actor',
                    palette=PlotSettings.colors,
                    facet_kws=PlotSettings.facet_kws,
                    kind='point', data=cnt,
                    markers = PlotSettings.markers,
                    linestyles=PlotSettings.lines,
                    order=PlotSettings.short_order)
axes = g.axes.flatten()
pyplot.sca(axes[1])
rect = patches.Rectangle((-0.25, 3.5), 2.75, 11, linewidth=3, alpha=0.5, edgecolor='r', facecolor='none')
pyplot.gca().add_patch(rect)

g.set_xticklabels(rotation=30)
pyplot.tight_layout()

pyplot.savefig(PlotSettings.output_file('simple_amazon.pdf'))
pyplot.show()
PlotSettings.copy_output()

## SPLITOUT BY AGE
seaborn.set_style(PlotSettings.style)
seaborn.set(PlotSettings.rc)
g = seaborn.catplot(x='Action',y='binary', hue='Actor',col='Young',
                    palette=PlotSettings.colors,
                    facet_kws=PlotSettings.facet_kws,
                    markers = PlotSettings.markers,
                    linestyles=PlotSettings.lines,
                    kind='point', data=data_table, order=PlotSettings.short_order)
axes = g.axes.flatten()
g.set_xticklabels(rotation=30)
pyplot.tight_layout()

pyplot.savefig(PlotSettings.output_file('simple_amazon_age.pdf'))
pyplot.show()
PlotSettings.copy_output()


#%% fit model on not permissible
formula = "invert_binary ~ Action + Actor"
result = Statistics.regression(formula, data=data_table, typ='log')
summary = result['summary']
print(summary)
