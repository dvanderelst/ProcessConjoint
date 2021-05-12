import pandas
from library import misc
import numpy

def run():
    data = pandas.read_csv('raw_data/DATA_JURGEN.csv',na_values='')
    data['ResponseId'] = data['V1']


    #%% Get the vignettes seen by every person
    _ , selected_variables = misc.select_variables_regex(data, '^A')
    selected_variables = ['ResponseId'] + selected_variables
    subset = data.loc[:, selected_variables]

    names = ['rating_nr','vignette_nr', 'actor', 'disease', 'action']
    vignettes = misc.split_qualtrics_variables(subset, 'ResponseId', split='_', column_names=names)
    vignettes = vignettes.query('value=="1"')
    vignettes = vignettes.replace({'rating_nr': {'A1': 1, 'A2': 2}})
    vignettes = vignettes.iloc[:,[0,1,3,4,5,6,7]]

    #%% Get the attention questions
    selected_variables = ['ResponseId', 'CQ1', 'CQ2', 'CQ3']
    attention = data.loc[:, selected_variables]

    ##% Get the ratings for each of the two vignettes seen
    data = data.replace({'Ethical1_Robot_1': {' ': '0'}}) #
    data = data.replace({'Ethical1_Perscare_1': {' ': '0'}})
    data = data.replace({'Ethical2_Robot_1': {' ': '0'}})
    data = data.replace({'Ethical2_Perscare_1': {' ': '0'}})
    data[1] = data['Ethical1_Robot_1'].astype(float) + data['Ethical1_Perscare_1'].astype(float)
    data[2] = data['Ethical2_Robot_1'].astype(float) + data['Ethical2_Perscare_1'].astype(float)
    selected_variables = ['ResponseId'] + [1,2]
    ratings  = data.loc[:, selected_variables]
    ratings = ratings.melt(id_vars='ResponseId')
    ratings.columns = ['ResponseId', 'rating_nr', 'response']

    #%% merge vignettes an rating
    merged = pandas.merge(vignettes, ratings, on=('ResponseId', 'rating_nr'))
    data_table = pandas.merge(merged, attention, on=('ResponseId'))

    # %% output
    with pandas.ExcelWriter('data/data_table_jurgen.xls') as writer:
        data_table.to_excel(writer, sheet_name='data_table')
