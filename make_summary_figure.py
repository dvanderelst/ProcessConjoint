import pandas
from library import PlotSettings
import seaborn
from matplotlib import pyplot

amazon = pandas.read_csv('data/simple_amazon_for_final.csv')
jurgen = pandas.read_csv('data/jurgen_for_final.csv')

#%%%%%%%%%%

grp = jurgen.groupby(['Action', 'Actor'])
mns = grp.Rating.mean()
mns = mns.reset_index()
mns = mns.pivot(columns='Actor', index='Action', values='Rating')

mns = (mns + 3) / 6

mns['diff'] = mns.Human - mns.Robot






#%%%%%%%%%%%%%

n = len(amazon.ResponseId.unique())
selected_actions = ['Refuse Dinner', 'Accept', 'No TV']

amazon = amazon.query('value == "Permissible"')
amazon = amazon.query('Action in @selected_actions')

grp = amazon.groupby(['Actor','value'])
cnt = grp.ResponseId.count()
cnt = cnt.reset_index()
cnt['Proportion'] = cnt['ResponseId'] / (n * len(selected_actions))



