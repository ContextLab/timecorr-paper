
import numpy as np
import sys
import os
from config import config
import pandas as pd
import glob as glob
import seaborn as sns
import matplotlib.pyplot as plt
sns.set(style="whitegrid")



reps = sys.argv[1]
cfun = sys.argv[2]
rfun = sys.argv[3]

# data_dir = os.path.join(config['resultsdir'], cfun + '_' + rfun + '_' + reps + '_test')
data_dir = os.path.join(config['resultsdir'], cfun + '_' + rfun + '_' + reps)

conds =glob.glob(os.path.join(data_dir, '*.csv'))

full_data = pd.DataFrame()
for c in conds:
    data = pd.read_csv(c)
    data['cond'] = os.path.basename(os.path.splitext(c)[0])

    if full_data.empty:
        full_data = data
    else:
        full_data = full_data.append(data)

full_data['error'] = 1-full_data['error']

def grouped_barplot(df, x, y, hue, outfile=None):
    fig, ax = plt.subplots()
    g = sns.factorplot(x=x, y=y, hue=hue, data=df, size=6, kind="bar", estimator=np.mean, ci=95, n_boot=1000,
                       palette="cubehelix", ax=ax, order=['intact', 'paragraph', 'word', 'rest'])

    sns.despine(ax=ax, left=True)
    ax.set_ylabel(y)
    ax.set_xlabel(x)
    l = ax.legend(loc='center right', bbox_to_anchor=(1.25, 0.5), ncol=1)
    l.set_title(hue)
    if not outfile:
        fig.show()
    else:
        fig.savefig(outfile, bbox_inches='tight')

outfile = os.path.join(data_dir, 'accuracy.png')
grouped_barplot(full_data, 'cond', 'accuracy', 'level', outfile)

outfile = os.path.join(data_dir, 'error.png')
grouped_barplot(full_data, 'cond','error', 'level', outfile)

outfile = os.path.join(data_dir, 'rank.png')
grouped_barplot(full_data, 'cond', 'rank', 'level', outfile)

# fig, ax = plt.subplots()
# g = sns.factorplot(x="cond", y="accuracy", hue="level", data=full_data,
#                    size=6, kind="bar", estimator=np.mean, ci=95, n_boot=1000, palette="cubehelix", ax=ax, order=['intact', 'paragraph', 'word', 'rest'])
#
# sns.despine(ax=ax, left=True)
# ax.set_ylabel("accuracy")
# ax.set_xlabel("condition")
# l = ax.legend()
# l.set_title('level')
# #plt.show()
#
# fig.savefig(os.path.join(data_dir, 'decoding_accuracy.png'))
#
# plt.clf()
#
# full_data['error'] = 1-full_data['error']
# # Draw a nested barplot to show survival for class and sex
# fig, ax = plt.subplots()
# g = sns.factorplot(x="cond", y="error", hue="level", data=full_data,
#                    size=6, kind="bar",  estimator=np.mean, ci=95, n_boot=1000, palette="muted", ax=ax, order=['intact', 'paragraph', 'word', 'rest'])
#
# sns.despine(ax=ax, left=True)
# ax.set_ylabel("1 - error")
# ax.set_xlabel("condition")
# l = ax.legend()
# l.set_title('level')
# #plt.show()
#
# fig.savefig(os.path.join(data_dir, 'decoding_error.png'))
#
# plt.clf()
# # Draw a nested barplot to show survival for class and sex
# fig, ax = plt.subplots()
# g = sns.factorplot(x="cond", y="rank", hue="level", data=full_data,
#                    size=6, kind="bar",  estimator=np.mean, ci=95, n_boot=1000, palette="muted", ax=ax, order=['intact', 'paragraph', 'word', 'rest'])
#
# sns.despine(ax=ax, left=True)
# ax.set_ylabel("rank")
# ax.set_xlabel("condition")
# l = ax.legend()
# l.set_title('level')
# #plt.show()
#
# fig.savefig(os.path.join(data_dir, 'decoding_rank.png'))