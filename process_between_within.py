import numpy
import pandas
import seaborn
from matplotlib import pyplot
from library import PlotSettings
from library import preprocess_between
from library import preprocess_within, misc
import pingouin as pg

from pyBat import Statistics

preprocess_between.run()
preprocess_within.run()


# %% Read in and prepare between and within

scenarios = pandas.read_csv('scenarios.csv', sep=',')
scenarios['scenario'] = numpy.arange(36) + 1

for data_nr in range(2):
    if data_nr == 0: data_table = pandas.read_excel('data/data_table_within.xls', sheet_name='data_table', index_col=0)
    if data_nr == 1: data_table = pandas.read_excel('data/data_table_between.xls', sheet_name='data_table', index_col=0)

    all_pp = len(data_table.ResponseId.unique())
    data_table = data_table.query('correct == 1')
    selected_pp = len(data_table.ResponseId.unique())
    print(all_pp, '-->', selected_pp)

    data_table = data_table.pivot(index=('ResponseId', 'scenario'), columns='renumbered_scale', values='rating')
    data_table = data_table.reset_index()
    data_table['summed'] = data_table.s4 + data_table.s5 + data_table.s6
    data_table = pandas.merge(data_table, scenarios, on='scenario')

    data_table['s7'] = ((data_table.s4 + data_table.s5 + data_table.s6) / 3)
    data_table['impact'] = ((data_table.s1 + data_table.s2 + data_table.s3) / 3)

    # Add proper labels for plotting with seaborn
    data_table['Actor'] = data_table['actor']
    data_table['Action'] = data_table['short_action']
    data_table['Rating'] = data_table['s7']
    data_table['Malady'] = data_table['condition_rank']

    # Rescale rating from -50 to 50
    data_table['Rating'] = data_table['Rating'] - 50

    if data_nr == 0: within = data_table
    if data_nr == 1: between = data_table

# Correlations between the three ratings for each scenario
rating_scales_between = between.loc[:, ['s4', 's5', 's6']]
rating_scales_between_alpha = pg.cronbach_alpha(data=rating_scales_between)
rating_scales_between = numpy.array(rating_scales_between)
rating_scales_between_correlations = numpy.corrcoef(rating_scales_between.transpose())

rating_scales_within = within.loc[:, ['s4', 's5', 's6']]
rating_scales_within_alpha = pg.cronbach_alpha(data=rating_scales_within)
rating_scales_within = numpy.array(rating_scales_within)
rating_scales_within_correlations = numpy.corrcoef(rating_scales_within.transpose())

# %%

for data_nr in [0, 1]:
    if data_nr == 0: data = within
    if data_nr == 1: data = between
    data = data.assign(Actor=data.Actor.map({'nurse': 'Nurse', 'robot': "Robot"}))

    g = seaborn.catplot(x='Action', y='Rating', hue='Actor', col='Malady',
                        kind='point', data=data,
                        palette= PlotSettings.colors,
                        linestyles= PlotSettings.lines,
                        markers = PlotSettings.markers,
                        estimator = PlotSettings.estimator,
                        facet_kws=PlotSettings.facet_kws,
                        ci = PlotSettings.ci,
                        order=PlotSettings.short_order)
    pyplot.ylim(-50, 50)
    g._legend.remove()
    pyplot.legend(loc='upper left')
    pyplot.tight_layout()

    axes = g.axes.flatten()
    axes[0].set_title("Mild Anxiety")
    axes[1].set_title("Migraine")
    axes[2].set_title("Acute Schizophrenia")
    g.set_xticklabels(rotation=90)
    PlotSettings.spine(g)
    pyplot.tight_layout()
    if data_nr == 0: pyplot.savefig(PlotSettings.output_file('within.pdf'))
    if data_nr == 1: pyplot.savefig(PlotSettings.output_file('between.pdf'))
    pyplot.show()

    formula = "Rating ~ Action + Malady + Actor"
    result = Statistics.regression(formula, data = data)
    summary = result['summary']

    if data_nr == 0: output_file = open(PlotSettings.output_file('LM_within.txt'), 'w')
    if data_nr == 1: output_file = open(PlotSettings.output_file('LM_between.txt'), 'w')

    if data_nr == 0: output_file_tex = open(PlotSettings.output_file('LM_within.tex'), 'w')
    if data_nr == 1: output_file_tex = open(PlotSettings.output_file('LM_between.tex'), 'w')

    output_file.write(misc.clean_summary(summary.as_text()))
    output_file.close()

    output_file_tex.write(misc.clean_summary(result['latex']))
    output_file_tex.close()

PlotSettings.copy_output()

# Export within data for potential processing with R

pvt = pandas.pivot(within, index=('ResponseId','Action','Malady'),columns='Actor',values='Rating')
pvt = pvt.reset_index()
pvt = pandas.melt(pvt, id_vars=('ResponseId','Action','Malady'), value_vars=['nurse','robot'])
pvt = pvt.dropna()
pvt.columns = ['ResponseId','Action','Malady', 'Actor', 'Rating']
pvt.to_csv('data/within_for_R.csv', index=False)

#%% save the demographics
demo = None
for data_nr in range(2):
    if data_nr == 0:
        selected_pp = list(within.ResponseId.unique())
        demo = pandas.read_excel('data/preprocessed_within.xls', sheet_name='demo_data', index_col=0)
    if data_nr == 1:
        selected_pp = list(between.ResponseId.unique())
        demo = pandas.read_excel('data/preprocessed_between.xls', sheet_name='demo_data', index_col=0)

    demo = demo.query('ResponseId in @selected_pp')
    if data_nr == 0: demo.to_csv('demographic_data/within.csv', index=False)
    if data_nr == 1: demo.to_csv('demographic_data/between.csv', index=False)




