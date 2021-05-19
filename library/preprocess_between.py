import pandas
from library import misc
import numpy


def run():
    data = pandas.read_csv('raw_data/Ethics+in+patient+care_March+27,+2021_15.51.csv')
    data = data.query('Finished=="True"')
    data = data.query('Status == "IP Address"')  # remove previews
    data = data.iloc[2:, :]

    # Who saw what?
    x = data.loc[:, ('ResponseId', 'actor_condition')]
    print(x)

    # Merge different options for ethnicity into a single variable
    subset, selected_variables = misc.select_variables(data, ['Q9_'])
    data['ethnicity'] = misc.concatenate_columns(subset)
    for x in range(10): data['ethnicity'] = data['ethnicity'].str.replace('_nan', '')
    for x in range(10): data['ethnicity'] = data['ethnicity'].str.replace('nan_', '')

    # Merge different options for gender into a single variable
    subset, selected_variables = misc.select_variables(data, ['Q8_'])
    data['gender'] = misc.concatenate_columns(subset)
    for x in range(10): data['gender'] = data['gender'].str.replace('_nan', '')
    for x in range(10): data['gender'] = data['gender'].str.replace('nan_', '')

    # Get rating data
    rating_variables = ['ResponseId', '_Q18_', '_Q19_', '_Q29_', '_Q30_']
    subset, selected_variables = misc.select_variables(data, rating_variables)
    names = ['scenario', 'question', 'scale']
    rating_data = misc.split_qualtrics_variables(subset, 'ResponseId', column_names=names)
    rating_data = rating_data.dropna()
    rating_data = rating_data.iloc[:, [0, 2, 3, 4, 5]]

    rating_data.rename(columns={'value': 'rating'}, inplace=True)
    rating_data['scenario'] = rating_data['scenario'].astype(int)
    rating_data['rating'] = rating_data['rating'].astype(int)
    rating_data['scale'] = rating_data['scale'].astype(int)
    rating_data = rating_data.replace('Q29', 'Q18')
    rating_data = rating_data.replace('Q30', 'Q19')

    # Get scenarios
    scenarios = pandas.read_csv('scenarios.csv', sep=',')
    scenarios['scenario'] = numpy.arange(36) + 1

    # Merge ratings and scenarios
    rating_data = pandas.merge(rating_data, scenarios, on='scenario')

    # Double check: each participant should only have one kind of actor
    grp = rating_data.groupby(['ResponseId', 'actor'])
    cnts = grp.count()
    print(cnts['rating'])

    # %% Get validation data
    validation_variables = ['ResponseId', '_Q22', '_Q23', '_Q33_', '_Q34']
    subset, selected_variables = misc.select_variables(data, validation_variables)
    names = ['scenario', 'question']
    validation_data = misc.split_qualtrics_variables(subset, 'ResponseId', column_names=names)
    validation_data.rename(columns={'value': 'selection'}, inplace=True)
    validation_data = validation_data.dropna()
    validation_data = validation_data.iloc[:, [0, 2, 3, 4]]

    validation_data['scenario'] = validation_data['scenario'].astype(int)
    validation_data.selection = validation_data.selection.str.lower()
    validation_data = validation_data.replace('Q33', 'Q22')
    validation_data = validation_data.replace('Q34', 'Q23')

    # Merge validation data and scenarios
    validation_data = pandas.merge(validation_data, scenarios, on='scenario')
    validation_data['relevant'] = False

    selection = validation_data.question == 'Q22'
    validation_data.relevant[selection] = validation_data.condition[selection]

    selection = validation_data.question == 'Q23'
    validation_data.relevant[selection] = validation_data.action[selection]

    validation_data['correct'] = validation_data.selection.str[0] == validation_data.relevant.str[0]
    validation_data = validation_data.iloc[:, [0, 1, 2, 3, 13]]

    grp = validation_data.groupby(['ResponseId'])
    mns = grp.correct.mean()
    mns = mns.reset_index()

    # Add validation data to ratings
    rating_data = rating_data.merge(mns, on=['ResponseId'])

    # Renumber scales
    grp = rating_data.groupby(['question', 'scale'])
    cnt = grp.count()
    cnt = cnt.reset_index()
    cnt = cnt.iloc[:, [0, 1]]
    cnt['renumbered_scale'] = ['s1', 's2', 's3', 's4', 's5', 's6']
    rating_data = pandas.merge(rating_data, cnt, on=['question', 'scale'])

    # %% Get demographic data
    demographics_variables = ['ResponseId', 'Q5', 'Q6', 'Q7', 'gender', 'ethnicity']
    demo_data, selected_variables = misc.select_variables(data, demographics_variables)
    names = ['ResponseId', 'BirthYear', 'Major', 'Politics', 'Ethnicity', 'Gender']
    demo_data.columns = names
    #demo_data = misc.split_qualtrics_variables(subset, 'ResponseId', column_names=names)
    #demo_data = demo_data.loc[:, ('ResponseId', 'question', 'value')]
    #demo_data = demo_data.dropna()

    # %%
    with pandas.ExcelWriter('data/preprocessed_between.xls') as writer:
        rating_data.to_excel(writer, sheet_name='rating_data')
        demo_data.to_excel(writer, sheet_name='demo_data')
        validation_data.to_excel(writer, sheet_name='validation_data')
        scenarios.to_excel(writer, sheet_name='scenarios')

    # %%
    #print('before:', rating_data.shape)
    #rating_data_subset = rating_data.query('correct == 1')
    #print('after:', rating_data_subset.shape)

    #data_table = rating_data.pivot(index=('ResponseId', 'scenario'), columns='renumbered_scale', values='rating')
    #data_table = data_table.reset_index()
    #data_table['summed'] = data_table.s4 + data_table.s5 + data_table.s6
    #data_table = pandas.merge(data_table, scenarios, on='scenario')

    with pandas.ExcelWriter('data/data_table_between.xls') as writer:
        rating_data.to_excel(writer, sheet_name='data_table')

