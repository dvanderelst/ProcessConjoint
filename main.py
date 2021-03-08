import pandas
import library
import numpy

data = pandas.read_csv('ConjointV03_March+7,+2021_11.40.csv')
line1 = data.iloc[0, :]
line2 = data.iloc[1, :]
data = data.iloc[2:, :]

# Merge different options for ethnicity into a single variable
subset, selected_variables = library.select_variables(data, ['Q9_'])
data['ethnicity'] = library.concatenate_columns(subset)
for x in range(10): data['ethnicity'] = data['ethnicity'].str.replace('_nan', '')
for x in range(10): data['ethnicity'] = data['ethnicity'].str.replace('nan_', '')

# Get rating data
rating_variables = ['ResponseId', '_Q18_', '_Q19_']
subset, selected_variables = library.select_variables(data, rating_variables)
names = ['scenario', 'question', 'scale']
rating_data = library.split_qualtrics_variables(subset, 'ResponseId', column_names=names)
rating_data = rating_data.dropna()
#rating_data = rating_data.iloc[:, [0, 2, 3, 4, 5]]
#rating_data['scenario'] = rating_data['scenario'].astype(int)
rating_data['trial'] = rating_data['trial'].astype(int)

# Get scenarios
scenarios = pandas.read_csv('scenarios.csv', sep='\t')
scenarios['scenario'] = numpy.arange(36) + 1

# Merge ratings and scenarios
rating_data = pandas.merge(rating_data, scenarios, on='scenario')

# %% Get validation data
validation_variables = ['ResponseId', '_Q21', '_Q22', '_Q23']
subset, selected_variables = library.select_variables(data, validation_variables)
names = ['scenario', 'question']
validation_data = library.split_qualtrics_variables(subset, 'ResponseId', column_names=names)
validation_data = validation_data.dropna()
validation_data = validation_data.iloc[:, [0, 2, 3, 4]]
validation_data['scenario'] = validation_data['scenario'].astype(int)

# Merge validation data and scenarios
validation_data = pandas.merge(validation_data, scenarios, on='scenario')
validation_data['relevant'] = False

selection = validation_data.question == 'Q21'
validation_data.relevant[selection] = validation_data.actor[selection]

selection = validation_data.question == 'Q22'
validation_data.relevant[selection] = validation_data.condition[selection]

selection = validation_data.question == 'Q23'
validation_data.relevant[selection] = validation_data.action[selection]

validation_data = validation_data.iloc[:, [0, 1, 2, 3, 7]]
validation_data.value = validation_data.value.str.lower()
validation_data['correct'] = validation_data.value.str[0] == validation_data.relevant.str[0]


# %% add trial order to validation data (this is not encoded in the variable names - bastards)
trial_order = rating_data.iloc[:, [0,2, 4]]
validation_data = pandas.merge(validation_data, trial_order , on=['ResponseId', 'scenario'])

# %% Get demographic data
demographics_variables = ['ResponseId', 'Q5', 'Q6', 'Q7', 'Q8', 'ethnicity']
subset, selected_variables = library.select_variables(data, demographics_variables)
names = ['question', 'option', 'dummy']
demo_data = library.split_qualtrics_variables(subset, 'ResponseId', column_names=names)
demo_data = demo_data.loc[:, ('ResponseId', 'question', 'value')]
demo_data = demo_data.dropna()

# %%
with pandas.ExcelWriter('output.xlsx') as writer:
    rating_data.to_excel(writer, sheet_name='rating_data')
    demo_data.to_excel(writer, sheet_name='demo_data')
    validation_data.to_excel(writer, sheet_name='validation_data')
