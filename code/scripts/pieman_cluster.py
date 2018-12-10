
import timecorr as tc
from timecorr.helpers import isfc, mean_combine, corrmean_combine
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

if len(sys.argv) < 7:
    debug = False
else:
    debug = eval(sys.argv[6])


if debug:
    results_dir = os.path.join(config['resultsdir'], cfun + '_' + rfun + '_' + reps + '_debug')

else:
    results_dir = os.path.join(config['resultsdir'], cfun + '_' + rfun + '_' + reps)

try:
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
except OSError as err:
   print(err)


width = 10
laplace = {'name': 'Laplace', 'weights': tc.laplace_weights, 'params': {'scale': width}}
# delta = {'name': '$\delta$', 'weights': tc.eye_weights, 'params': tc.eye_params}
# gaussian = {'name': 'Gaussian', 'weights': tc.gaussian_weights, 'params': {'var': width}}
# mexican_hat = {'name': 'Mexican hat', 'weights': tc.mexican_hat_weights, 'params': {'sigma': width}}
# kernels = [delta, gaussian, laplace, mexican_hat]

pieman_data = loadmat(os.path.join(config['datadir'], 'pieman_ica100.mat'))
pieman_conds = ['intact', 'paragraph', 'word', 'rest']


#### tiny data to debug #####

if debug:
    data = []
    conds = []
    for c in pieman_conds:
        next_data = list(map(lambda i: pieman_data[c][:, i][0][:30,:10], np.arange(2)))
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

for i in range(int(reps)):

    iter_results = tc.timepoint_decoder(data[conds == cond], level=np.arange(int(level) + 1),
                                        combine=corrmean_combine,
                                        cfun=eval(cfun),
                                        rfun=rfun,
                                        weights_params=laplace['params'])
    print(iter_results)
    iter_results['iteration'] = i
    append_iter = append_iter.append(iter_results)

save_file = os.path.join(results_dir, cond)

results = append_iter

results.to_csv(save_file + '.csv')

