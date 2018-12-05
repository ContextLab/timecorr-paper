import warnings

import numpy as np
import timecorr as tc
from timecorr.helpers import isfc, mean_combine, corrmean_combine
import seaborn as sns
import os
from matplotlib import pyplot as plt
from matplotlib import gridspec
from scipy.stats import wishart
import hypertools as hyp
from scipy.spatial.distance import cdist
from scipy.io import loadmat

import numpy as np
import sys
import os
from config import config
import pandas as pd


LEGEND_SIZE = 12
SMALL_SIZE = 14
MEDIUM_SIZE = 16
BIGGER_SIZE = 18

cond = sys.argv[1]
level = sys.argv[2]
reps = sys.argv[3]
cfun = sys.argv[4]
rfun = sys.argv[5]

plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=LEGEND_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

if not os.path.isdir('figs'):
    os.mkdir('figs')
figdir = 'figs'


results_dir = os.path.join(config['resultsdir'], cfun + '_' + rfun + '_' + reps)

try:
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
except OSError as err:
   print(err)


def plot_ribbon(ts, xs, color='k', ribbon_alpha=0.2, ax=None, xlab=None, ylab=None):
    mean = np.mean(xs, axis=0)
    ci = 1.96 * np.divide(np.std(xs, axis=0), np.sqrt(xs.shape[0]))

    if ax == None:
        ax = plt.gca()
    plt.sca(ax)

    h1 = ax.fill_between(ts, mean - ci, mean + ci, color=color, alpha=ribbon_alpha)
    h2 = ax.plot(ts, mean, color=color)

    if not (xlab == None):
        plt.xlabel(xlab)

    if not (ylab == None):
        plt.ylabel(ylab)

    return h1, h2

width = 10
delta = {'name': '$\delta$', 'weights': tc.eye_weights, 'params': tc.eye_params}
gaussian = {'name': 'Gaussian', 'weights': tc.gaussian_weights, 'params': {'var': width}}
laplace = {'name': 'Laplace', 'weights': tc.laplace_weights, 'params': {'scale': width}}
mexican_hat = {'name': 'Mexican hat', 'weights': tc.mexican_hat_weights, 'params': {'sigma': width}}
kernels = [delta, gaussian, laplace, mexican_hat]

pieman_data = loadmat(os.path.join(config['datadir'], 'pieman_ica100.mat'))
pieman_conds = ['intact', 'paragraph', 'word', 'rest']

data = []
conds = []
for c in pieman_conds:
    next_data = list(map(lambda i: pieman_data[c][:, i][0], np.arange(pieman_data[c].shape[1])))
    data.extend(next_data)
    conds.extend([c]*len(next_data))
del pieman_data


#### tiny data to debug #####

# data = []
# conds = []
# for c in pieman_conds:
#     next_data = list(map(lambda i: pieman_data[c][:, i][0][:30,:10], np.arange(2)))
#     data.extend(next_data)
#     conds.extend([c]*len(next_data))
# del pieman_data

data = np.array(data)
conds = np.array(conds)

append_iter = pd.DataFrame()

for i in range(int(reps)):

    iter_results = tc.timepoint_decoder(data[conds == cond], level=int(level),
                                        combine=corrmean_combine,
                                        cfun=eval(cfun),
                                        rfun=rfun,
                                        weights_params=laplace['params'])
    print(iter_results)

    append_iter = append_iter.append(iter_results)
    append_iter.index.rename('iteration', inplace=True)

save_file = os.path.join(results_dir, cond)

results = append_iter.groupby('level').mean()

results.to_csv(save_file + '.csv')

