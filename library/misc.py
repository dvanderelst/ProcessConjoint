import copy

import numpy
import pandas
from scipy.stats import kruskal


def select_variables(data, patterns=[]):
    selected_variables = None
    for pattern in patterns:
        found = data.columns.str.contains(pattern)
        if selected_variables is None: selected_variables = found
        selected_variables = numpy.logical_or(found, selected_variables)
    subset = data.iloc[:, selected_variables]
    return subset, data.columns[selected_variables]

def select_variables_regex(data, pattern):
    new = data.filter(regex=pattern, axis=1)
    subset = new.columns
    subset = list(subset)
    return new, subset


def concatenate_columns(data):
    cols = data.columns
    result = data[cols].apply(lambda row: '_'.join(row.values.astype(str)), axis=1)
    return result


def split_qualtrics_variables(data, idvariable, split='_', column_names=[]):
    new_data = pandas.melt(data, id_vars=idvariable)
    for x in split: new_data.variable = new_data.variable.str.replace(x, '_')
    split = new_data.variable.str.split('_', expand=True)
    if len(column_names) > 0: split.columns = column_names
    new_data = pandas.concat((new_data, split), axis=1)
    #new_data = new_data.dropna()
    return new_data


def my_kruskal(data, design=None, conditions=None, actions=None, print_queries=False):
    data = copy.copy(data)
    data['Actor'] = data['actor']
    data['Action'] = data['action_rank']
    data['Rating'] = data['s7']
    data['Malady'] = data['condition_rank']

    query = ''
    if design is not None: query += 'Design == "%s" and ' % design
    if conditions is not None: query += 'Malady in %s and ' % conditions
    if actions is not None: query += 'Action in %s and ' % actions
    q1 = query + 'Actor == "robot"'
    q2 = query + 'Actor == "nurse"'
    if print_queries: print('Q1: ', q1, '\nQ2: ', q2)
    s1 = data.query(q1)
    s2 = data.query(q2)
    result = kruskal(s1.Rating, s2.Rating)
    result = result + (s1.Rating, s2.Rating)
    return result