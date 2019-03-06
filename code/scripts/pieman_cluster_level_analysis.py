
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

result_name = 'level_analysis_rand_compare'

if debug:
    results_dir = os.path.join(config['resultsdir'], result_name, cfun + '_' + rfun + '_' + wp + '_' + str(width) + '_debug')
    results_dir_rand = os.path.join(config['resultsdir'], result_name, cfun + '_' + rfun + '_' + wp + '_' + str(width) + '_rand_debug')
    results_dir_last = os.path.join(config['resultsdir'], result_name,
                                    cfun + '_' + rfun + '_' + wp + '_' + str(width) + '_last_debug')


else:
    results_dir = os.path.join(config['resultsdir'], result_name, cfun + '_' + rfun + '_' + wp + '_' + str(width))
    results_dir_rand = os.path.join(config['resultsdir'], result_name,
                               cfun + '_' + rfun + '_' + wp + '_' + str(width) + '_rand')
    results_dir_last = os.path.join(config['resultsdir'], result_name,
                                    cfun + '_' + rfun + '_' + wp + '_' + str(width) + '_last')

try:
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
except OSError as err:
   print(err)

try:
    if not os.path.exists(results_dir_rand):
        os.makedirs(results_dir_rand)
except OSError as err:
   print(err)

try:
    if not os.path.exists(results_dir_last):
        os.makedirs(results_dir_last)
except OSError as err:
   print(err)


laplace = {'name': 'Laplace', 'weights': tc.laplace_weights, 'params': {'scale': width}}
delta = {'name': '$\delta$', 'weights': tc.eye_weights, 'params': tc.eye_params}
gaussian = {'name': 'Gaussian', 'weights': tc.gaussian_weights, 'params': {'var': width}}
mexican_hat = {'name': 'Mexican hat', 'weights': tc.mexican_hat_weights, 'params': {'sigma': width}}

pieman_data = loadmat(os.path.join(config['datadir'], 'pieman_ica100.mat'))
pieman_conds = ['intact', 'paragraph', 'word', 'rest']


weights_paramter = eval(wp)


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
append_iter2 = pd.DataFrame()

iter_results = tc.helpers.weighted_timepoint_decoder(data[conds == cond], nfolds=2, level=int(level),
                                    combine=corrmean_combine,
                                    cfun=eval(cfun),
                                    rfun=rfun,
                                    weights_fun=weights_paramter['weights'],
                                    weights_params=weights_paramter['params'])

iter_results2 = tc.helpers.weighted_timepoint_decoder(data[conds == cond], nfolds=2, level=int(level),
                                    combine=corrmean_combine,
                                    cfun=eval(cfun),
                                    rfun=rfun,
                                    weights_fun=weights_paramter['weights'],
                                    weights_params=weights_paramter['params'], opt_init='random')

iter_results3 = tc.helpers.weighted_timepoint_decoder(data[conds == cond], nfolds=2, level=int(level),
                                    combine=corrmean_combine,
                                    cfun=eval(cfun),
                                    rfun=rfun,
                                    weights_fun=weights_paramter['weights'],
                                    weights_params=weights_paramter['params'], opt_init='last')

print(iter_results)
print(iter_results2)
print(iter_results3)

iter_results['iteration'] = int(reps)
iter_results2['iteration'] = int(reps)
iter_results3['iteration'] = int(reps)

save_file = os.path.join(results_dir, cond)
save_file2 = os.path.join(results_dir_rand, cond)
save_file3 = os.path.join(results_dir_last, cond)

if not os.path.isfile(save_file + '.csv'):
      iter_results.to_csv(save_file + '.csv')
else:
    append_iter = pd.read_csv(save_file + '.csv', index_col=0)
    append_iter = append_iter.append(iter_results)
    append_iter.to_csv(save_file + '.csv')

if not os.path.isfile(save_file2 + '.csv'):
      iter_results2.to_csv(save_file2 + '.csv')
else:
    append_iter2 = pd.read_csv(save_file2 + '.csv', index_col=0)
    append_iter2 = append_iter2.append(iter_results2)
    append_iter2.to_csv(save_file2 + '.csv')

if not os.path.isfile(save_file3 + '.csv'):
      iter_results3.to_csv(save_file3 + '.csv')
else:
    append_iter3 = pd.read_csv(save_file3 + '.csv', index_col=0)
    append_iter3 = append_iter3.append(iter_results3)
    append_iter3.to_csv(save_file3 + '.csv')
