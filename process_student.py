import pandas
from library import preprocess_student
import seaborn
from matplotlib import pyplot
from pyBat import Statistics
from library import PlotSettings
preprocess_student.run()

data_table = pandas.read_excel('data/data_table_student.xls', sheet_name='data_table', index_col=0)

# Add proper labels for plotting with seaborn
data_table['Actor'] = data_table['actor']
data_table['Scenario'] = data_table['scenario']
data_table['Rating'] = data_table['numeric_response']

seaborn.set_style(PlotSettings.style)
g = seaborn.catplot(x='Scenario', y='Rating', kind='bar',
                hue='Actor', data=data_table,
                palette=[PlotSettings.black, PlotSettings.grey],
                estimator=PlotSettings.estimator,
                facet_kws=PlotSettings.facet_kws,
                ci=PlotSettings.ci)

pyplot.ylim(0,6)
g._legend.remove()
pyplot.legend(loc='upper left')
pyplot.tight_layout()
pyplot.savefig(PlotSettings.output_file('student.pdf'))
pyplot.show()

formula = "Rating ~ C(Scenario) + Actor"
result = Statistics.regression(formula, data=data_table)
summary = result['summary']
f= open(PlotSettings.output_file('LM_student.txt'), 'w')
f.write(summary.as_text())
f.close()

f= open(PlotSettings.output_file('LM_student.tex'), 'w')
f.write(result['latex'])
f.close()

PlotSettings.copy_output()