import pandas
import seaborn
from matplotlib import pyplot
from pyBat import Statistics

rating_data = pandas.read_excel('preprocessed.xlsx', sheet_name='rating_data', index_col=0)
scenarios = pandas.read_excel('preprocessed.xlsx', sheet_name='scenarios', index_col=0)

print('before:', rating_data.shape)
rating_data = rating_data.query('correct == 1')
print('after:', rating_data.shape)

#%%

pivotted = rating_data.pivot(index=('ResponseId', 'scenario'), columns='renumbered_scale', values='rating')
pivotted = pivotted.reset_index()
pivotted['summed'] = pivotted.s4 + pivotted.s5 + pivotted.s6

formula = 'summed ~ s1 + s2 + s3'
result = Statistics.linear_regression(formula, pivotted)
print(result['summary'])

