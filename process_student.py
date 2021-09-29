import pandas
from library import preprocess_student
import seaborn
from matplotlib import pyplot
from pyBat import Statistics
from library import PlotSettings, misc
preprocess_student.run()

data_table = pandas.read_excel('data/data_table_student.xls', sheet_name='data_table', index_col=0)


# I think that, even though particpants completed the surevey
# some of them did not answer all questions. Perhaps,
# responding was not enforced.
# Here, I only retain the people with 9 answers

grp = data_table.groupby(['ResponseId', 'IPAddress'])
cnt = grp.count()
cnt = cnt.reset_index()
cnt = cnt.query('variable==9')
selected_ids = cnt.ResponseId.values
print(len(selected_ids))
data_table = data_table.query('ResponseId in @selected_ids')

# Add proper labels for plotting with seaborn
data_table['Actor'] = data_table['actor']
data_table['Scenario'] = data_table['scenario']
data_table['Rating'] = data_table['numeric_response']
data_table['Variation'] = data_table['variation']

seaborn.set_style(PlotSettings.style)
seaborn.set(PlotSettings.rc)
seaborn.set_context("paper", font_scale=3)

g = seaborn.catplot(x='Scenario', y='Rating', kind='point',
                hue='Actor', data=data_table, row='Variation',
                palette=PlotSettings.colors,
                estimator=PlotSettings.estimator,
                facet_kws=PlotSettings.facet_kws,
                markers = PlotSettings.markers,
                linestyles=PlotSettings.lines,
                ci=PlotSettings.ci,
                aspect=2)

pyplot.ylim(0,6)
g._legend.remove()
pyplot.legend(loc='upper left')
pyplot.tight_layout()
pyplot.savefig(PlotSettings.output_file('student.pdf'))
pyplot.show()

formula = "Rating ~ C(Scenario) + Actor + Variation"
result = Statistics.regression(formula, data=data_table)
summary = result['summary']
f= open(PlotSettings.output_file('LM_student.txt'), 'w')
f.write(summary.as_text())
f.close()

f= open(PlotSettings.output_file('LM_student.tex'), 'w')
f.write(misc.clean_summary(result['latex']))
f.close()

PlotSettings.copy_output()

demo = data_table.loc[:,['ResponseId','Gender','Occupation','BirthYear','Country','IPAddress']]
demo = demo.drop_duplicates()
demo.to_csv('demographic_data/student.csv', index=False)

country_counts = demo.Country.value_counts()
line = ''
for i in range(4):
    a = country_counts.index[i]
    a = a.rstrip(' ')
    a = a.lstrip(' ')
    b = country_counts[i]
    s = "%s, (%s)" % (a,b)
    line = line + s + ', '
line = line.strip(',')
print(line)

#%%
selected_countries = ['Germany ','Colombia ','Argentina ']
selected_countries = data_table.query('Country in @selected_countries')
g = seaborn.catplot(x='Scenario', y='Rating', kind='point', col='Variation',
                hue='Actor', data=selected_countries, row='Country',
                palette=PlotSettings.colors,
                estimator=PlotSettings.estimator,
                facet_kws=PlotSettings.facet_kws,
                markers = PlotSettings.markers,
                linestyles=PlotSettings.lines,
                ci=PlotSettings.ci,
                aspect=2)
pyplot.ylim(0,6)
g._legend.remove()
pyplot.legend(loc='upper left')
pyplot.tight_layout()
pyplot.savefig(PlotSettings.output_file('student_country.pdf'))
pyplot.show()

PlotSettings.copy_output()

formula = "Rating ~ C(Scenario) + Actor + Variation + Country"
result = Statistics.regression(formula, data=selected_countries)
summary = result['summary']
print(summary)