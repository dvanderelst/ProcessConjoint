import pandas
from library import misc


def run():
    actions = ["accept Roberts's decision to not take the medication",
               "notify a trusted person selected by Robert",
               "notify Robert's doctor about his decision",
               "repeat the request to take the medication",
               "refuse to serve dinner until the medication is taken",
               "to not let Robert watch TV"]

    action_short = ["Accept",
                    "Notify Trusted",
                    "Notify Doctor",
                    "Repeat",
                    "Refuse Dinner",
                    "No TV"]

    action_nr = ['1', '2', '3', '4', '5', '6']

    actions = pandas.DataFrame({'actions': actions, 'action_nr': action_nr, 'action_short': action_short})

    data = pandas.read_csv('raw_data/Nurses_And_Robots_AmazonTurk_May+17,+2021_07.34.csv')
    data = data.query('Finished=="True"')
    data = data.query('Status == "IP Address"')  # remove previews
    data = data.iloc[2:, :]

    # Merge different options for ethnicity into a single variable
    subset, _ = misc.select_variables(data, ['Q10_'])
    data['ethnicity'] = misc.concatenate_columns(subset)
    for x in range(10): data['ethnicity'] = data['ethnicity'].str.replace('_nan', '')
    for x in range(10): data['ethnicity'] = data['ethnicity'].str.replace('nan_', '')

    # Merge different options for gender into a single variable
    subset, selected_variables = misc.select_variables(data, ['Q9_'])
    data['gender'] = misc.concatenate_columns(subset)
    for x in range(10): data['gender'] = data['gender'].str.replace('_nan', '')
    for x in range(10): data['gender'] = data['gender'].str.replace('nan_', '')

    # Get rating data
    rating_variables = ['ResponseId', 'Q3', 'Q14']
    subset, _ = misc.select_variables(data, rating_variables)
    names = ['picture_order', 'side', 'action_nr']
    rating_data = misc.split_qualtrics_variables(subset, 'ResponseId', split='_#', column_names=names)
    rating_data = rating_data.dropna() # only retain the actions presented to the participants

    # Get attention questions
    attention_variables = ['ResponseId', 'Q16#', 'Q17#']
    subset, _ = misc.select_variables(data, attention_variables)
    names = ['picture_order', 'side', 'action_nr']
    attention_data = misc.split_qualtrics_variables(subset, 'ResponseId', split='_#', column_names=names)
    attention_data = attention_data.dropna() # only retain the actions presented to the participants

    #%%
    # Get the actor for the ratings
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

    # Get the actor for the attention questions
    attention_data['actor'] = 0
    n = attention_data.shape[0]
    for i in range(n):
        order = attention_data['picture_order'].iloc[i]
        side = attention_data['side'].iloc[i]
        # this recoding order is a bit weird. But it matches the headers
        # in the raw data csv file
        if order == 'Q16' and side == '1': actor = 'nurse'
        if order == 'Q16' and side == '2': actor = 'robot'
        if order == 'Q17' and side == '1': actor = 'nurse'
        if order == 'Q17' and side == '2': actor = 'robot'
        attention_data['actor'].iloc[i] = actor

    rating_data = rating_data.merge(actions, on='action_nr')
    attention_data = attention_data.merge(actions, on='action_nr')
    attention_data = attention_data.iloc[:,[0, 2, 5, 6]]
    attention_data.columns = ['ResponseId', 'attention_response', 'action_nr', 'actor']

    rating_data = pandas.merge(rating_data, attention_data, on=('ResponseId','action_nr', 'actor'), how='left')
    rating_data['attention_correct'] = rating_data.value == rating_data.attention_response

    # Get correctness per pp
    accuracy = rating_data.dropna()
    grp = accuracy.groupby('ResponseId')
    mns = grp.attention_correct.mean()
    accuracy = mns.reset_index()

    rating_data = pandas.merge(rating_data, accuracy, on='ResponseId')


    # %% Get demographic data
    demographics_variables = ['ResponseId', 'Q6', 'gender', 'ethnicity']
    demo_data, selected_variables = misc.select_variables(data, demographics_variables)
    names = ['ResponseId', 'BirthYear', 'Ethnicity','Gender']
    demo_data.columns = names
    #demo_data = misc.split_qualtrics_variables(subset, 'ResponseId', column_names=names)
    #demo_data = demo_data.loc[:, ('ResponseId', 'question', 'value')]
    #demo_data = demo_data.dropna()

    # %%
    with pandas.ExcelWriter('data/preprocessed_simple_amazon.xls') as writer:
        demo_data.to_excel(writer, sheet_name='demo_data')
        accuracy.to_excel(writer, sheet_name='accuracy')

    # %% output
    data_table = rating_data
    with pandas.ExcelWriter('data/data_table_simple_amazon.xls') as writer:
        data_table.to_excel(writer, sheet_name='data_table')

