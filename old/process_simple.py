import pandas
import seaborn
from matplotlib import pyplot
from library import PlotSettings
from library import preprocess_simple
from pyBat import Statistics

preprocess_simple.run()

data_table = pandas.read_excel('data/data_table_simple.xls', sheet_name='data_table', index_col=0)
data_table['binary'] = data_table['value'] == 'Permissible'

# Add proper labels for plotting with seaborn
data_table['Actor'] = data_table['actor']
data_table['Action'] = data_table['action_short']
data_table['Rating'] = data_table['binary'] * 1

seaborn.set_style(PlotSettings.style)
seaborn.set_context("paper", font_scale=1.5)
g = seaborn.catplot(x='Action', y='Rating',kind='point',
                hue='Actor',
                data=data_table,
                palette=[PlotSettings.black, PlotSettings.black],
                linestyles=PlotSettings.lines,
                markers=PlotSettings.markers,
                estimator=PlotSettings.estimator,
                facet_kws=PlotSettings.facet_kws,
                ci=PlotSettings.ci,
                order=PlotSettings.short_order)
pyplot.ylim(-0.2, 1.2)
g._legend.remove()
pyplot.legend(loc='upper left')


axes = g.axes.flatten()
g.set_xticklabels(rotation=30)
pyplot.tight_layout()
pyplot.savefig(PlotSettings.output_file('simple.pdf'))
pyplot.show()

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
