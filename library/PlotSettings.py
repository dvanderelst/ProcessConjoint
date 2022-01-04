import os
import numpy
import shutil
import os
from matplotlib import cm
import seaborn
plot_folder = 'output'
paper_plot_folder = '/home/dieter/Dropbox/Apps/Overleaf/RobotsAndNurses/output'


facet_kws=dict(despine=False)


seaborn.set_style("darkgrid")
seaborn.set(font_scale=1.5)

short_order = ["Refuse Dinner","Accept", "No TV","Notify Trusted","Notify Doctor","Repeat"]
black = (0,0,0)
grey = (0.5,0.5,0.5)
colors = ['#EDB200','#FF6600','#8da0cb']#[black, black]
markers = ['s','o']
lines = ['-', '-']
estimator = numpy.mean
ci = 95


wedgeprops={"edgecolor":"k",'linewidth': 1, 'linestyle': 'solid', 'antialiased': True}

def get_colors(n):
    colors = cm.get_cmap('binary', n)
    colors = colors(range(n))
    return colors

def copy_and_overwrite(from_path, to_path):
    if os.path.exists(to_path):
        shutil.rmtree(to_path)
    shutil.copytree(from_path, to_path)


def copy_output():
    copy_and_overwrite(plot_folder, paper_plot_folder)

def output_file(base):
    filename = os.path.join(plot_folder, base)
    return filename


def spine(g):
    for ax in g.axes.flatten():  # Loop directly on the flattened axes
        ax.tick_params(bottom=False)
        for _, spine in ax.spines.items():
            spine.set_visible(True)
            spine.set_color('black')
            spine.set_linewidth(1)


