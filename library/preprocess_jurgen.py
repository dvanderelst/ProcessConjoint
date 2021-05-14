import pandas
from library import misc
import numpy

def run():
    data = pandas.read_csv('raw_data/DATA_JURGEN.csv',na_values='')
    data['ResponseId'] = data['V1']
    data = data.query('V10==1')


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
    #CQ1: who (0) nurse, (1) robot
    #CQ2: action (0) force (1) accept
    #CQ#: (1) anxiety, (2) micgraine, (3) PD, (4) schizo
    selected_variables = ['ResponseId', 'CQ1', 'CQ2', 'CQ3']
    attention = data.loc[:, selected_variables]
    attention = attention.replace({'CQ1': {'0': 'Perca', '1': 'Rob'}})  #
    attention = attention.replace({'CQ2': {'0': 'Force', '1': 'Accept'}})  #
    attention = attention.replace({'CQ3': {'1': 'Anx', '2': 'Mig', '3': 'PD', '4': 'Sciz'}})  #
    attention['rating_nr'] = 1 # only attentions questions for rating 1


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
    #print(ratings.shape, vignettes.shape, attention.shape)
    merged = pandas.merge(vignettes, ratings, on=('ResponseId', 'rating_nr'))
    data_table = pandas.merge(merged, attention, on=('ResponseId', 'rating_nr'), how='outer')
    #print(data_table.shape)

    data_table['CQ1_correct'] = data_table.CQ1 == data_table.actor
    data_table['CQ2_correct'] = data_table.CQ2 == data_table.action
    data_table['CQ3_correct'] = data_table.CQ3 == data_table.disease
    data_table['CQ_correct'] = data_table['CQ1_correct'] * data_table['CQ2_correct'] * data_table['CQ3_correct']

    data_table.CQ_correct[data_table.rating_nr == 2] = True #override for second vignette

    #%% Get demographics
    demographic_variables = ['ResponseId','Gender','BirthYear','occupation','LocationLatitude','LocationLongitude']
    demographics = data.loc[:, demographic_variables]
    data_table = pandas.merge(data_table, demographics, on='ResponseId')

    # %% output
    with pandas.ExcelWriter('data/data_table_jurgen.xls') as writer:
        data_table.to_excel(writer, sheet_name='data_table')
