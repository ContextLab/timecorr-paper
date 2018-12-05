
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

#data_dir = os.path.join(config['resultsdir'], cfun + '_' + rfun + '_' + reps + '_test')
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

# Draw a nested barplot to show survival for class and sex
fig, ax = plt.subplots()
g = sns.factorplot(x="cond", y="accuracy", hue="level", data=full_data,
                   size=6, kind="bar", palette="muted", ax=ax, order=['intact', 'paragraph', 'word', 'rest'])

sns.despine(ax=ax, left=True)
ax.set_ylabel("decoding accuracy")
ax.set_xlabel("condition")
l = ax.legend()
l.set_title('level')
#plt.show()

fig.savefig(os.path.join(data_dir, 'decoding_accuracy.png'))

plt.clf()
# Draw a nested barplot to show survival for class and sex
fig, ax = plt.subplots()
g = sns.factorplot(x="cond", y="error", hue="level", data=full_data,
                   size=6, kind="bar", palette="muted", ax=ax, order=['intact', 'paragraph', 'word', 'rest'])

sns.despine(ax=ax, left=True)
ax.set_ylabel("decoding error")
ax.set_xlabel("condition")
l = ax.legend()
l.set_title('level')
#plt.show()

fig.savefig(os.path.join(data_dir, 'decoding_error.png'))

plt.clf()
# Draw a nested barplot to show survival for class and sex
fig, ax = plt.subplots()
g = sns.factorplot(x="cond", y="rank", hue="level", data=full_data,
                   size=6, kind="bar", palette="muted", ax=ax, order=['intact', 'paragraph', 'word', 'rest'])

sns.despine(ax=ax, left=True)
ax.set_ylabel("decoding rank")
ax.set_xlabel("condition")
l = ax.legend()
l.set_title('level')
#plt.show()

fig.savefig(os.path.join(data_dir, 'decoding_rank.png'))