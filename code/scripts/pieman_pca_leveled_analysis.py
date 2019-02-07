
import timecorr as tc
from timecorr.helpers import isfc, wisfc, mean_combine, corrmean_combine
from scipy.io import loadmat
import numpy as np
import sys
import os
from config import config
import pandas as pd

cond = sys.argv[1]
level = sys.argv[2]
reps = sys.argv[3]
cfun = sys.argv[4]
rfun = sys.argv[5]
width = int(sys.argv[6])
wp = sys.argv[7]

if len(sys.argv) < 9:
    debug = False
else:
    debug = eval(sys.argv[8])


if debug:
    results_dir = os.path.join(config['resultsdir'], cfun + '_' + rfun + '_' + wp + '_' + str(width) + '_debug', 'level_'+level)

else:
    results_dir = os.path.join(config['resultsdir'], cfun + '_' + rfun + '_' + wp + '_' + str(width), 'level_'+level)

try:
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
except OSError as err:
   print(err)



laplace = {'name': 'Laplace', 'weights': tc.laplace_weights, 'params': {'scale': width}}
delta = {'name': '$\delta$', 'weights': tc.eye_weights, 'params': tc.eye_params}
gaussian = {'name': 'Gaussian', 'weights': tc.gaussian_weights, 'params': {'var': width}}
mexican_hat = {'name': 'Mexican hat', 'weights': tc.mexican_hat_weights, 'params': {'sigma': width}}

pieman_data = loadmat(os.path.join(config['datadir'], 'pieman_ica100.mat'))
pieman_conds = ['intact', 'paragraph', 'word', 'rest']


weights_paramter = eval(wp)

#### tiny data to debug #####

if debug:
    data = []
    conds = []
    for c in pieman_conds:
        next_data = list(map(lambda i: pieman_data[c][:, i][0][:30,:10], np.arange(4)))
        data.extend(next_data)
        conds.extend([c]*len(next_data))
    del pieman_data

else:

    data = []
    conds = []
    for c in pieman_conds:
        next_data = list(map(lambda i: pieman_data[c][:, i][0], np.arange(pieman_data[c].shape[1])))
        data.extend(next_data)
        conds.extend([c]*len(next_data))
    del pieman_data


data = np.array(data)
conds = np.array(conds)

append_iter = pd.DataFrame()

iter_results = tc.helpers.optimize_pca_weighted_timepoint_decoder(data[conds == cond], nfolds=2, level=int(level),
                                    combine=mean_combine,
                                    cfun=eval(cfun),
                                    rfun=rfun,
                                    weights_fun=weights_paramter['weights'],
                                    weights_params=weights_paramter['params'])

print(iter_results)
iter_results['iteration'] = int(reps)


save_file = os.path.join(results_dir, cond)


if not os.path.isfile(save_file + '.csv'):
      iter_results.to_csv(save_file + '.csv')
else:
    append_iter = pd.read_csv(save_file + '.csv', index_col=0)
    append_iter = append_iter.append(iter_results)
    append_iter.to_csv(save_file + '.csv')



