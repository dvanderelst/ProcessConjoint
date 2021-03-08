import numpy
import pandas

def select_variables(data, patterns=[]):
    selected_variables = None
    for pattern in patterns:
        found = data.columns.str.contains(pattern)
        if selected_variables is None: selected_variables = found
        selected_variables = numpy.logical_or(found, selected_variables)
    subset = data.iloc[:, selected_variables]
    return subset, data.columns[selected_variables]

def concatenate_columns(data):
    cols = data.columns
    result = data[cols].apply(lambda row: '_'.join(row.values.astype(str)), axis=1)
    return result


def split_qualtrics_variables(data, idvariable, split='_', column_names=[]):
    new_data = pandas.melt(data, id_vars=idvariable)
    split = new_data.variable.str.split(split, expand=True)
    if len(column_names) > 0: split.columns = column_names
    new_data = pandas.concat((new_data, split), axis=1)
    #new_data = new_data.dropna()
    return new_data

