import numpy
import pandas
import seaborn
from matplotlib import pyplot

from library import PlotSettings
from library import preprocess_between
from library import preprocess_within

from pyBat import Statistics

preprocess_between.run()
preprocess_within.run()


# %% Read in and prepare between and within

scenarios = pandas.read_csv('scenarios.csv', sep=',')
scenarios['scenario'] = numpy.arange(36) + 1

for x in range(2):
    if x == 0: data_table = pandas.read_excel('data/data_table_within.xls', sheet_name='data_table', index_col=0)
    if x == 1: data_table = pandas.read_excel('data/data_table_between.xls', sheet_name='data_table', index_col=0)

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

    if x == 0: within = data_table
    if x == 1: between = data_table

# Correlations between the three ratings for each scenario
rating_scales_between = between.loc[:, ['s4', 's5', 's6']]
rating_scales_between = numpy.array(rating_scales_between)
rating_scales_between_correlations = numpy.corrcoef(rating_scales_between.transpose())

rating_scales_within = within.loc[:, ['s4', 's5', 's6']]
rating_scales_within = numpy.array(rating_scales_within)
rating_scales_within_correlations = numpy.corrcoef(rating_scales_within.transpose())

# %%

for x in range(2):
    if x == 0: data = within
    if x == 1: data = between

    seaborn.set_style(PlotSettings.style)
    seaborn.set_context("paper", font_scale=1.5)
    g = seaborn.catplot(x='Action', y='Rating', hue='Actor', col='Malady',
                        kind='point', data=data,
                        palette=[PlotSettings.black, PlotSettings.grey],
                        linestyles= PlotSettings.lines,
                        markers = PlotSettings.markers,
                        estimator = PlotSettings.estimator,
                        facet_kws=PlotSettings.facet_kws,
                        ci = PlotSettings.ci,
                        order=PlotSettings.short_order)
    pyplot.ylim(0, 100)
    g._legend.remove()
    pyplot.legend(loc='upper left')
    pyplot.tight_layout()

    axes = g.axes.flatten()
    axes[0].set_title("Mild Anxiety")
    axes[1].set_title("Migraine")
    axes[2].set_title("Acute Schizophrenia")
    g.set_xticklabels(rotation=30)
    pyplot.tight_layout()
    if x == 0: pyplot.savefig(PlotSettings.output_file('within.pdf'))
    if x == 1: pyplot.savefig(PlotSettings.output_file('between.pdf'))
    pyplot.show()

    formula = "Rating ~ Action + Malady + Actor"
    result = Statistics.regression(formula, data = data)
    summary = result['summary']

    if x == 0: f = open(PlotSettings.output_file('LM_within.txt'), 'w')
    if x == 1: f = open(PlotSettings.output_file('LM_between.txt'), 'w')

    if x == 0: f_tex = open(PlotSettings.output_file('LM_within.tex'), 'w')
    if x == 1: f_tex = open(PlotSettings.output_file('LM_between.tex'), 'w')

    f.write(summary.as_text())
    f.close()

    f_tex.write(result['latex'])
    f_tex.close()

PlotSettings.copy_output()

#%% On to the demographics


for x in range(2):
    if x == 0:
        selected_pp = list(within.ResponseId.unique())
        demo = pandas.read_excel('data/preprocessed_within.xls', sheet_name='demo_data', index_col=0)
    if x == 1:
        selected_pp = list(between.ResponseId.unique())
        demo = pandas.read_excel('data/preprocessed_between.xls', sheet_name='demo_data', index_col=0)

    demo.columns = ['ResponseId', 'question', 'response']
    demo = demo.query('ResponseId in @selected_pp')

    pyplot.figure(figsize=(6,3))
    pyplot.subplot(1,2,1)

    colors = PlotSettings.get_colors(4)
    data = demo.query('question == "Q8"')
    grp = data.groupby('response')
    cnt = grp.count()
    cnt = cnt.reset_index()
    cnt = cnt.replace('Genderqueer/Gender Non-Conforming','Non-Conforming')
    pyplot.pie(cnt.question, labels=cnt.response, autopct='%1.1f%%', colors=colors, wedgeprops=PlotSettings.wedgeprops)

    pyplot.subplot(1,2,2)

    colors = PlotSettings.get_colors(12)
    data = demo.query('question == "Q5"')
    data['response'] = data.response.astype(float)
    data['age'] = 2021 - data.response.astype(int)
    data = data.replace(1, numpy.nan)

    pyplot.hist(data.age,color=PlotSettings.black)
    pyplot.ylabel('Count')
    pyplot.xlabel('Age')
    pyplot.title('Age distribution')
    pyplot.tight_layout()
    if x == 0: pyplot.savefig(PlotSettings.output_file('within_demo.pdf'))
    if x == 1: pyplot.savefig(PlotSettings.output_file('between_demo.pdf'))
    pyplot.show()
    print(data.age.mean())

PlotSettings.copy_output()