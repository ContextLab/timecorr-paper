
import timecorr as tc
from timecorr.helpers import isfc, reduce, vec2mat
from scipy.io import loadmat
from sklearn.decomposition import PCA, IncrementalPCA
import numpy as np
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

levels = np.arange(0,4,1)
conditions = ['intact', 'paragraph', 'rest', 'word']

for l in levels:
    for c in conditions:
        con = os.path.join(corrsdir, f'lev_{l}'+ f'_{c}'+ '.npy')
        try:
            corrs = np.load(con)
            for s in np.arange(corrs.shape[0]):
                mat_corrs = tc.helpers.vec2mat(corrs[s])
                x = mat_corrs
                split = np.cumsum([len(xi) for xi in x])[:-1]
                pca = IncrementalPCA(n_components=np.shape(x)[2])
                x_r = np.vsplit(pca.fit_transform(np.vstack(x)), split)

            #next_corrdir = os.path.join(data_dir, 'mean_corrs', f'level_{l}')
            # if not os.path.exists(next_corrdir):
            #     os.makedirs(next_corrdir)
            # mean_corrs = mat_corrs.mean(axis=2)
            # np.save(os.path.join(next_corrdir, f'{c}.npy'), mean_corrs)
        except:
            print('issue loading: ' + con)
            pass


### to combine across patients:

# data_dir = '/dartfs/rc/lab/D/DBIC/CDL/f002s72/timecorr_paper/pieman/results'
# corrs_dir = os.path.join(data_dir, 'laplace_50_orderedup_corrs')
#
# levels = np.arange(0,4,1)
# conditions = ['intact', 'paragraph', 'rest', 'word']
#
# for l in levels:
#     for c in conditions:
#         con = os.path.join(corrs_dir, f'lev_{l}'+ f'_{c}'+ '.npy')
#         try:
#             corrs = np.load(con)
#             mat_corrs = tc.helpers.vec2mat(corrs)
#             next_corrdir = os.path.join(data_dir, 'mean_corrs', f'level_{l}')
#             if not os.path.exists(next_corrdir):
#                 os.makedirs(next_corrdir)
#             mean_corrs = mat_corrs.mean(axis=2)
#             np.save(os.path.join(next_corrdir, f'{c}.npy'), mean_corrs)
#         except:
#             print('issue loading: ' + con)
#             pass