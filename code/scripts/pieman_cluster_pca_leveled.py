
import timecorr as tc
from timecorr.helpers import isfc, reduce, vec2mat
from scipy.io import loadmat
from sklearn.decomposition import PCA, IncrementalPCA
import numpy as np
import scipy.stats
import pandas as pd
import seaborn as sns
import sys
import os
from config import config

cond = sys.argv[1]
level = sys.argv[2]
cfun = sys.argv[3]
rfun = sys.argv[4]
width = int(sys.argv[5])

laplace = {'name': 'Laplace', 'weights': tc.laplace_weights, 'params': {'scale': width}}
delta = {'name': '$\delta$', 'weights': tc.eye_weights, 'params': tc.eye_params}
gaussian = {'name': 'Gaussian', 'weights': tc.gaussian_weights, 'params': {'var': width}}
mexican_hat = {'name': 'Mexican hat', 'weights': tc.mexican_hat_weights, 'params': {'sigma': width}}

smooth = sys.argv[6]
raw = 'delta'

smooth_parameter = eval(smooth)
raw_parameter = eval(raw)

smooth_fun = smooth_parameter['weights']
smooth_params = smooth_parameter['params']
raw_fun = raw_parameter['weights']
raw_params = raw_parameter['params']


result_name = 'corrs_ordered_up_for_PCA'

corrsdir = os.path.join(config['resultsdir'], result_name, cfun + '_' + rfun + '_' + smooth + '_' + str(width))

pcadir = os.path.join(config['resultsdir'], result_name, 'corrs_results')

try:
    if not os.path.exists(pcadir):
        os.makedirs(pcadir)
except OSError as err:
   print(err)

levels = np.arange(0,4,1)
conditions = ['intact', 'paragraph', 'rest', 'word']

for l in levels:
    con = os.path.join(corrsdir, f'lev_{l}'+ f'_{cond}'+ '.npy')
    save_file = os.path.join(pcadir, f'rfun_{rfun}' + f'lev_{l}'+ f'_{cond}')
    print(save_file)
    corrs = np.load(con)
    stacked = np.vstack(corrs)
    split = np.cumsum([len(xi) for xi in corrs])[:-1]
    pca = IncrementalPCA(n_components=np.shape(stacked)[1])
    x_r = np.vsplit(pca.fit_transform(np.vstack(stacked)), split)
    r = []
    k_samps = np.unique(np.geomspace(3, corrs.shape[2], num=1000, dtype=int))
    corrs_all = pd.DataFrame(index=k_samps, columns=np.arange(corrs.shape[0]))
    for s in np.arange(corrs.shape[0]):
        rs = []
        S = x_r[s]
        s_true = np.corrcoef(S)
        v_true = s_true[np.triu_indices_from(s_true)]
        #for k in np.arange(3, corrs.shape[2], 1):
        for e, k in enumerate(k_samps):
            s_reduced = np.corrcoef(S[:, :k])
            v_reduced = s_reduced[np.triu_indices_from(s_reduced)]
            corrs_all.iloc[e, s] = scipy.stats.pearsonr(v_true, v_reduced)[0]


    corrs_all.to_csv(save_file + '.csv')

