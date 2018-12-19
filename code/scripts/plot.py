
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
    g = sns.factorplot(x=x, y=y, hue=hue, data=df, size=8, kind="bar", estimator=np.mean, ci=95, n_boot=1000,
                       palette="cubehelix", ax=ax, order=['intact', 'paragraph', 'word', 'rest'])

    sns.despine(ax=ax, left=True)
    ax.set_title(title)
    ax.set_ylabel(y)
    ax.set_xlabel(x)
    ax.set_ylim(0, .75)
    l = ax.legend(loc='center right', bbox_to_anchor=(1.25, 0.75), ncol=2)
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

    melted_df = pd.DataFrame()

    for c in np.arange(full_data['level'].max() + 2):
        if c!=full_data['level'].max() + 1:
            melted_temp_df = pd.DataFrame()
            melted_temp_df['weights'] = full_data['level_' + str(c)]
            melted_temp_df['level'] = full_data['level']
            melted_temp_df['level'] = c
            #melted_temp_df['accuracy'] = full_data['accuracy']
            melted_temp_df['cond'] = full_data['cond']

            if melted_df.empty:
                melted_df = melted_temp_df
            else:
                melted_df = melted_df.append(melted_temp_df)
        else:

            melted_temp_df = pd.DataFrame()
            melted_temp_df['weights'] = full_data['accuracy']
            melted_temp_df['level'] = full_data['level']
            melted_temp_df['level'] = 'accuracy'
            melted_temp_df['cond'] = full_data['cond']
            melted_df = melted_df.append(melted_temp_df)
    full_data['error'] = 1-full_data['error']

    p_split = param_name.split('_')

    if debug:
        title = p_split[0] + ' ' + p_split[1] + ' ' + p_split[-3] + ' ' + p_split[-2]
    else:
        title = p_split[0] + ' ' + p_split[1] + ' ' + p_split[-2] + ' ' + p_split[-1]


    outfile = os.path.join(fig_dir, param_name + 'accuracy.png')
    #grouped_barplot(full_data, 'cond', 'accuracy', 'level', title=title, outfile=outfile)
    grouped_barplot(melted_df, 'cond', 'weights', 'level', title=title, outfile=outfile)

    #outfile = os.path.join(fig_dir, param_name + 'error.png')
    #grouped_barplot(full_data, 'cond','error', 'level', title=title, outfile=outfile)

    #outfile = os.path.join(fig_dir, param_name + 'rank.png')
    #grouped_barplot(full_data, 'cond', 'rank', 'level', title=title, outfile=outfile)

    plt.close('all')