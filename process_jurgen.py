import numpy
import pandas
from library import preprocess_jurgen
import seaborn
from matplotlib import pyplot
from library import PlotSettings, misc
from pyBat import Statistics
from scipy.stats import ttest_1samp
from statsmodels.stats.anova import AnovaRM

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

data_table['Stage'] = data_table['Stage'].replace(1,'Rating 1')
data_table['Stage'] = data_table['Stage'].replace(2,'Rating 2')

data_table['Actor'] = data_table['Actor'].replace('Rob','Robot')
data_table['Actor'] = data_table['Actor'].replace('Perca','Human')


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
pyplot.savefig(PlotSettings.output_file('jurgen.pdf'))
pyplot.show()

formula = "Rating ~ Action  * Actor + Malady"
stage1 = data_table.query('rating_nr==1')
result1 = Statistics.regression(formula, data=stage1)
summary1 = result1['summary']
f = open(PlotSettings.output_file('LM_jurgen_1.tex'), 'w')
f.write(misc.clean_summary(result1['latex']))
f.close()

#%% Prepare data for within subject analysis

within_data = pandas.pivot(data_table, index=['ResponseId','Malady','Actor','Action'], columns='Stage', values='Rating')
within_data = within_data.reset_index()
within_data = pandas.melt(within_data, id_vars=['ResponseId','Malady','Action','Actor'])
within_data = within_data.dropna()
within_data.columns = ['ResponseId','Malady','Action','Actor','Stage','Rating']
within_data.to_csv('data/jurgen_within_data.csv')

first_actors = ['Human', 'Robot']
actions = ['Accept', 'Force']
maladies = ['Sciz', 'Anx']

tables = []
for first_actor in first_actors:
    for action in actions:
        for malady in maladies:
            selected = within_data.query('Actor == @first_actor and Action == @action and Malady == @malady and Stage == "Rating 1"')
            selected_subjects = selected.ResponseId.values
            selected_table = within_data.query("ResponseId in @selected_subjects")
            selected_table = selected_table.pivot(index='ResponseId',columns='Actor', values='Rating')
            selected_table['First_actor'] = first_actor
            selected_table['Action'] = action
            selected_table['Malady'] = malady
            selected_table['Difference'] = selected_table.Human - selected_table.Robot
            tables.append(selected_table)


within_data_for_analysis = pandas.concat(tables)
difference =  within_data_for_analysis.Difference.values
test = ttest_1samp(difference, popmean=0)
t = test[0]
p = test[1]
df = within_data_for_analysis.shape[0] - 1
mn = numpy.mean(difference)
text = '$\\Delta \\bar{\\mu}$ = %.2f, (%i) = %.2f, $p$ = %.2f' % (mn, df, t, p)
f = open(PlotSettings.output_file('LM_jurgen_2.tex'), 'w')
f.write(text)
f.close()

# within_data_for_analysis['Difference'] =
#
# grp = within_data_for_analysis.groupby(['First_actor', 'Action'])
# mns = grp.Difference.mean()
# mns = mns.reset_index()
#
# formula = "Difference ~ First_actor * Action"
# result2 = Statistics.regression(formula, data=within_data_for_analysis)
# summary2 = result2['summary']

#
PlotSettings.copy_output()

#%% On to demographics
demo = data_table.loc[:,['ResponseId', 'Gender','BirthYear', 'occupation','IPAddress']]
demo.columns = ['ResponseId', 'Gender','BirthYear', 'Occupation','IPAddress']
demo.to_csv('demographic_data/jurgen.csv', index=False)


#%%%
seaborn.set_style(PlotSettings.style)
seaborn.set(PlotSettings.rc)



g = seaborn.catplot(x='Action', y='Rating',kind='point',
                hue='Actor', row='Malady',
                data=stage1,
                palette=PlotSettings.colors,
                linestyles=PlotSettings.lines,
                markers=PlotSettings.markers,
                facet_kws=PlotSettings.facet_kws)

pyplot.ylim((-3, 3))
g._legend.remove()
pyplot.legend(loc='upper left')
pyplot.tight_layout()
pyplot.savefig(PlotSettings.output_file('jurgen_between.pdf'))
pyplot.show()
PlotSettings.copy_output()

#%%




g = seaborn.catplot(x='Action', y='Rating',kind='point',
                hue='Actor', row='Malady',
                data=within_data,
                palette=PlotSettings.colors,
                linestyles=PlotSettings.lines,
                markers=PlotSettings.markers,
                facet_kws=PlotSettings.facet_kws)

pyplot.ylim((-3, 3))
g._legend.remove()
pyplot.legend(loc='upper left')
pyplot.tight_layout()
pyplot.savefig(PlotSettings.output_file('jurgen_within.pdf'))
pyplot.show()
PlotSettings.copy_output()