
import numpy as np
import sys
import os
from config import config
import pandas as pd
import glob as glob
import seaborn as sns
import matplotlib.pyplot as plt
sns.set(style="whitegrid")

def grouped_barplot(df, x, y, hue, title=None, outfile=None):
    fig, ax = plt.subplots()
    g = sns.factorplot(x=x, y=y, hue=hue, data=df, size=6, kind="bar", estimator=np.mean, ci=95, n_boot=1000,
                       palette="cubehelix", ax=ax, order=['intact', 'paragraph', 'word', 'rest'])

    sns.despine(ax=ax, left=True)
    ax.set_title(title)
    ax.set_ylabel(y)
    ax.set_xlabel(x)
    l = ax.legend(loc='center right', bbox_to_anchor=(1.25, 0.5), ncol=1)
    l.set_title(hue)
    if not outfile:
        fig.show()
    else:
        fig.savefig(outfile, bbox_inches='tight')


if len(sys.argv) < 2:
    debug = False
else:
    debug = True

if debug:
    data_dir = config['resultsdir']+ '_debug'

else:
    data_dir = config['resultsdir']

fig_dir = os.path.join(config['workingdir'], 'figs')

if not os.path.isdir(fig_dir):
    os.mkdir(fig_dir)


params =glob.glob(os.path.join(data_dir, '*'))

for p in params:
    param_name = os.path.basename(os.path.splitext(p)[0])

    conds =glob.glob(os.path.join(p, '*.csv'))

    full_data = pd.DataFrame()
    for c in conds:
        data = pd.read_csv(c)
        data['cond'] = os.path.basename(os.path.splitext(c)[0])

        if full_data.empty:
            full_data = data
        else:
            full_data = full_data.append(data)

    full_data['error'] = 1-full_data['error']

    p_split = param_name.split('_')

    if debug:
        title = p_split[0] + ' ' + p_split[1] + ' ' + p_split[-3] + ' ' + p_split[-2]
    else:
        title = p_split[0] + ' ' + p_split[1] + ' ' + p_split[-2] + ' ' + p_split[-1]


    outfile = os.path.join(fig_dir, param_name + 'accuracy.png')
    grouped_barplot(full_data, 'cond', 'accuracy', 'level', title=title, outfile=outfile)

    outfile = os.path.join(fig_dir, param_name + 'error.png')
    grouped_barplot(full_data, 'cond','error', 'level', title=title, outfile=outfile)

    outfile = os.path.join(fig_dir, param_name + 'rank.png')
    grouped_barplot(full_data, 'cond', 'rank', 'level', title=title, outfile=outfile)

    plt.close('all')