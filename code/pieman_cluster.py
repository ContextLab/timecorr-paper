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


LEGEND_SIZE = 12
SMALL_SIZE = 14
MEDIUM_SIZE = 16
BIGGER_SIZE = 18

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

pieman_data = loadmat('../data/pieman_ica100.mat')
pieman_conds = ['intact', 'paragraph', 'word', 'rest']

data = []
conds = []
for c in pieman_conds:
    next_data = list(map(lambda i: pieman_data[c][:, i][0], np.arange(pieman_data[c].shape[1])))
    data.extend(next_data)
    conds.extend([c]*len(next_data))
del pieman_data

data = np.array(data)
conds = np.array(conds)


## test level 0
#results = tc.timepoint_decoder(data[conds == 'intact'], cfun=None, weights_params=laplace['params'])

#results = tc.timepoint_decoder(data[conds == 'intact'], level=1, combine = [mean_combine, corrmean_combine], cfun=[None, isfc], rfun=[None, 'eigenvector_centrality'], weights_params=laplace['params'])

results_intact = tc.timepoint_decoder(data[conds == 'intact'], level=2, combine = [mean_combine, corrmean_combine, corrmean_combine], cfun=[None, isfc, isfc], rfun=[None, 'eigenvector_centrality', 'eigenvector_centrality'], weights_params=laplace['params'])

results_paragraph = tc.timepoint_decoder(data[conds == 'paragraph'], level=2, combine = [mean_combine, corrmean_combine, corrmean_combine], cfun=[None, isfc, isfc], rfun=[None, 'eigenvector_centrality', 'eigenvector_centrality'], weights_params=laplace['params'])

results_word = tc.timepoint_decoder(data[conds == 'word'], level=2, combine = [mean_combine, corrmean_combine, corrmean_combine], cfun=[None, isfc, isfc], rfun=[None, 'eigenvector_centrality', 'eigenvector_centrality'], weights_params=laplace['params'])

results_rest = tc.timepoint_decoder(data[conds == 'rest'], level=2, combine = [mean_combine, corrmean_combine, corrmean_combine], cfun=[None, isfc, isfc], rfun=[None, 'eigenvector_centrality', 'eigenvector_centrality'], weights_params=laplace['params'])

#results = tc.timepoint_decoder(data[conds == 'intact'], level=0, cfun=None, weights_params=laplace['params'])

pieman_data = loadmat('../data/pieman_ica100.mat')
## test level 1
c = 'intact'
try_data = []
repdata = 10
for i in range(repdata):
    try_data.append(pieman_data[c][:, 1][0])

try_data = np.array(try_data)

results = tc.timepoint_decoder(try_data, cfun=None, weights_params=laplace['params'])

results = tc.timepoint_decoder(try_data, level=1, combine = [mean_combine, corrmean_combine], cfun=[None, isfc], rfun=[None, 'eigenvector_centrality'], weights_params=laplace['params'])

results = tc.timepoint_decoder(try_data, level=2, combine = [mean_combine, corrmean_combine, corrmean_combine], cfun=[None, isfc, isfc], rfun=[None, 'eigenvector_centrality', 'eigenvector_centrality'], weights_params=laplace['params'])


# repdata = 10
# try_data = []
# for i in range(repdata):
#     try_data.extend(data[conds == 'intact'][1][np.newaxis, :, :])
#
# results = tc.timepoint_decoder(try_data, level=2, combine = [mean_combine, corrmean_combine, corrmean_combine], cfun=[None, isfc, isfc], rfun=[None, 'eigenvector_centrality', 'eigenvector_centrality'], weights_params=laplace['params'])

#
# results = tc.timepoint_decoder(data[conds == 'intact'], level=2, combine = [mean_combine, corrmean_combine, corrmean_combine], cfun=[None, isfc, isfc], rfun=[None, 'eigenvector_centrality', 'eigenvector_centrality'], weights_params=laplace['params'])
#
# results = tc.timepoint_decoder(data[conds == 'intact'], weights_params=laplace['params'], rfun='eigenvector_centrality')
#
#
# results
