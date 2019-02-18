
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

result_name = 'level_analysis_chunked'

if debug:
    results_dir = os.path.join(config['resultsdir'], result_name, cfun + '_' + rfun + '_' + wp + '_' + str(width) + '_debug')

else:
    results_dir = os.path.join(config['resultsdir'], result_name, cfun + '_' + rfun + '_' + wp + '_' + str(width))

try:
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
except OSError as err:
   print(err)


laplace = {'name': 'Laplace', 'weights': tc.laplace_weights, 'params': {'scale': width}}
delta = {'name': '$\delta$', 'weights': tc.eye_weights, 'params': tc.eye_params}
gaussian = {'name': 'Gaussian', 'weights': tc.gaussian_weights, 'params': {'var': width}}
mexican_hat = {'name': 'Mexican hat', 'weights': tc.mexican_hat_weights, 'params': {'sigma': width}}

pieman_data = loadmat(os.path.join(config['datadir'], 'pieman_data.mat'))
pieman_conds = ['intact', 'paragraph', 'word', 'rest']


weights_paramter = eval(wp)


if debug:
    data_thirds = [0] * 3
    conds_thirds = [0] * 3
    divided = 0
    for third in list(range(3)):
        data = []
        conds = []
        for c in pieman_conds:
            next_data = list(map(lambda i: pieman_data[c][:, i][0][divided:divided+10,:20], np.arange(4)))
            data.extend(next_data)
            conds.extend([c]*len(next_data))

        conds_thirds[third] = conds
        data_thirds[third] = data
        divided += 10

    del pieman_data

else:

    data_thirds = [0] * 3
    conds_thirds = [0] * 3
    divided = 0
    for third in list(range(3)):
        data = []
        conds = []
        for c in pieman_conds:
            next_data = list(map(lambda i: pieman_data[c][:, i][0][divided:divided+100,:], np.arange(pieman_data[c].shape[1])))
            data.extend(next_data)
            conds.extend([c]*len(next_data))

        conds_thirds[third] = conds
        data_thirds[third] = data
        divided += 100

    del pieman_data

chunks = 3


for chunk in range(chunks):


    data = np.array(data_thirds[chunk])
    conds = np.array(conds_thirds[chunk])

    append_iter = pd.DataFrame()

    iter_results = tc.helpers.weighted_timepoint_decoder(data[conds == cond], nfolds=2, level=int(level),
                                        combine=corrmean_combine,
                                        cfun=eval(cfun),
                                        rfun=rfun,
                                        weights_fun=weights_paramter['weights'],
                                        weights_params=weights_paramter['params'])

    print(iter_results)
    iter_results['iteration'] = int(reps)
    iter_results['third'] = int(chunk)

    save_file = os.path.join(results_dir, cond)


    if not os.path.isfile(save_file + '.csv'):
          iter_results.to_csv(save_file + '.csv')
    else:
        append_iter = pd.read_csv(save_file + '.csv', index_col=0)
        append_iter = append_iter.append(iter_results)
        append_iter.to_csv(save_file + '.csv')



