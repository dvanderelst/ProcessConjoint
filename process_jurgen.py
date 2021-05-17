import numpy
import pandas
from library import preprocess_jurgen
import seaborn
from matplotlib import pyplot
from library import PlotSettings
from pyBat import Statistics
preprocess_jurgen.run()

data_table = pandas.read_excel('data/data_table_jurgen.xls', sheet_name='data_table', index_col=0)

grp = data_table.groupby('ResponseId')
accuracy = grp.CQ_correct.mean()
accuracy = accuracy.reset_index()
accuracy.columns = ['ResponseId', 'accuracy']

data_table = pandas.merge(data_table, accuracy, on='ResponseId')

all_pp = len(data_table.ResponseId.unique())
data_table = data_table.query('accuracy == 1')
selected_pp = len(data_table.ResponseId.unique())
print(all_pp, '-->', selected_pp)


# Add proper labels for plotting with seaborn
data_table['Actor'] = data_table['actor']
data_table['Action'] = data_table['action']
data_table['Rating'] = data_table['response']
data_table['Malady'] = data_table['disease']
data_table['Stage'] = data_table['rating_nr']

seaborn.set_style(PlotSettings.style)
seaborn.set_context("paper", font_scale=1.5)
g = seaborn.catplot(x='Malady', y='Rating',kind='point',
                hue='Actor', row = 'Stage', col='Action',
                data=data_table,
                palette=[PlotSettings.black, PlotSettings.black],
                linestyles=PlotSettings.lines,
                markers=PlotSettings.markers,
                estimator=PlotSettings.estimator,
                facet_kws=PlotSettings.facet_kws)

pyplot.ylim((-3, 3))
g._legend.remove()
pyplot.legend(loc='upper left')
pyplot.tight_layout()
pyplot.tight_layout()
pyplot.savefig(PlotSettings.output_file('jurgen.pdf'))
pyplot.show()

formula = "Rating ~ Action  * Actor + Malady"

stage1 = data_table.query('rating_nr==1')
result1 = Statistics.regression(formula, data=stage1)
summary1 = result1['summary']

stage2 = data_table.query('rating_nr==2')
result2 = Statistics.regression(formula, data=stage2)
summary2 = result2['summary']

f= open(PlotSettings.output_file('LM_jurgen.txt'), 'w')
f.write(summary1.as_text())
f.write(summary2.as_text())
f.close()

f= open(PlotSettings.output_file('LM_jurgen_1.tex'), 'w')
f.write(result1['latex'])
f.close()

f= open(PlotSettings.output_file('LM_jurgen_2.tex'), 'w')
f.write(result2['latex'])
f.close()

PlotSettings.copy_output()

#%% On to demographics

pyplot.figure(figsize=(6, 3))
pyplot.subplot(1, 2, 1)

colors = PlotSettings.get_colors(2)
cnts = data_table.Gender.value_counts()

pyplot.pie(cnts, labels=['Male','Female'], autopct='%1.1f%%',colors=colors, wedgeprops=PlotSettings.wedgeprops)

pyplot.subplot(1, 2, 2)

age = 2021 - data_table.BirthYear
pyplot.hist(age, color=PlotSettings.black)
pyplot.ylabel('Count')
pyplot.xlabel('Age')
pyplot.title('Age distribution')
pyplot.tight_layout()
pyplot.savefig(PlotSettings.output_file('jurgen_demo.pdf'))
pyplot.show()
# print(data.age.mean())

print(numpy.mean(age))