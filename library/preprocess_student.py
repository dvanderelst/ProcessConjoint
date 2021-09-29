import pandas
import numpy
from library import misc


#%% Get ratings
def run():
    data = pandas.read_csv('raw_data/data_student.csv', na_values='')
    data = data.query('Finished=="True"')
    data = data.query('Status == "IP Address"')  # remove previews
    data = data.iloc[2:, :]

    new, variables = misc.select_variables_regex(data, '(Robot[0-9][a,b])|(Human[0-9][a,b])')
    new_variables = []
    for x in variables:
        actor = x[0:-2]
        case = x[-2]
        variation = x[-1]
        new = actor + '_' + case + '_' + variation
        new_variables.append(new)
    variables = ['ResponseId'] + variables
    new_variables = ['ResponseId'] + new_variables

    ratings = data.loc[:, variables]
    ratings.columns = new_variables

    ratings = misc.split_qualtrics_variables(ratings, idvariable='ResponseId', column_names=['actor', 'scenario', 'variation'])
    names = list(ratings.columns)
    names[2] = 'response'
    ratings.columns = names
    ratings = ratings.dropna()

    #%% Create a dataframe with numeric equivalents
    response = ratings.response.value_counts()
    response = list(response.index)
    response.sort()
    numeric_response = [5,1,3,4,2,6,0]
    numeric_values = {'response': response, 'numeric_response': numeric_response}
    numeric_values = pandas.DataFrame(numeric_values)
    ratings = pandas.merge(ratings, numeric_values, on='response')

    #%% Get demographics
    variables = ['ResponseId','Gender','Country','WorkingWithRobots','Occupation', 'BirthYear', 'IPAddress']
    demographics = data.loc[:, variables]
    data_table = pandas.merge(ratings, demographics, on='ResponseId')

    # %% output
    with pandas.ExcelWriter('data/data_table_student.xls') as writer:
        data_table.to_excel(writer, sheet_name='data_table')