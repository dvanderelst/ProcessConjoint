import pandas
from library import misc
import numpy

def run():
    data = pandas.read_csv('raw_data/Nurses_And_Robots_April+30,+2021_19.17.csv')
    data = data.query('Finished=="True"')
    data = data.query('Status == "IP Address"')  # remove previews
    data = data.iloc[2:, :]

    # Merge different options for ethnicity into a single variable
    subset, selected_variables = misc.select_variables(data, ['Q10_'])
    data['ethnicity'] = misc.concatenate_columns(subset)
    for x in range(10): data['ethnicity'] = data['ethnicity'].str.replace('_nan', '')
    for x in range(10): data['ethnicity'] = data['ethnicity'].str.replace('nan_', '')

    # Get rating data
    rating_variables = ['ResponseId', 'Q3', 'Q14']
    subset, selected_variables = misc.select_variables(data, rating_variables)
    names = ['picture_order', 'side', 'action_nr']
    rating_data = misc.split_qualtrics_variables(subset, 'ResponseId', split='_#', column_names=names)
    rating_data = rating_data.dropna() # only retain the actions presented to the participants

    rating_data['actor'] = 0
    n = rating_data.shape[0]
    for i in range(n):
        order = rating_data['picture_order'].iloc[i]
        side = rating_data['side'].iloc[i]

        # this recoding order is a bit weird. But it matches the headers
        # in the raw data csv file
        if order == 'Q3' and side == '1': actor = 'nurse'
        if order == 'Q3' and side == '2': actor = 'robot'
        if order == 'Q14' and side == '1': actor = 'nurse'
        if order == 'Q14' and side == '2': actor = 'robot'

        rating_data['actor'].iloc[i] = actor


    actions = ["accept Roberts's decision to not take the medication",
    "notify a trusted person selected by Robert",
    "notify Robert's doctor about his decision",
    "repeat the request to take the medication",
    "refuse to serve dinner until the medication is taken",
    "to not let Robert watch TV,5,2"]

    action_nr = ['1','2','3', '4', '5', '6']

    actions = pandas.DataFrame({'actions': actions, 'action_nr': action_nr})

    rating_data = rating_data.merge(actions, on='action_nr')


    # %% Get demographic data
    demographics_variables = ['ResponseId', 'Q6', 'Q7', 'Q8', 'Q9', 'ethnicity']
    subset, selected_variables = misc.select_variables(data, demographics_variables)
    names = ['question', 'option', 'dummy']
    demo_data = misc.split_qualtrics_variables(subset, 'ResponseId', column_names=names)
    demo_data = demo_data.loc[:, ('ResponseId', 'question', 'value')]
    demo_data = demo_data.dropna()

    #%% output
    data_table = rating_data
    with pandas.ExcelWriter('data/data_table_simple.xls') as writer:
        data_table.to_excel(writer, sheet_name='data_table')
