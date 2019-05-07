
import timecorr as tc
from timecorr.helpers import isfc, wisfc, mean_combine, corrmean_combine
from scipy.io import loadmat
import numpy as np
import sys
import os
from config import config
import pandas as pd

cond = sys.argv[1]
chunk = sys.argv[2]
reps = sys.argv[3]
cfun = sys.argv[4]
rfun = sys.argv[5]
width = int(sys.argv[6])
wp = sys.argv[7]
ndims = sys.argv[8]

if len(sys.argv) < 10:
    debug = False
else:
    debug = eval(sys.argv[9])

result_name = 'pca_decode_chunked'

if debug:
    results_dir = os.path.join(config['resultsdir'], result_name, rfun + '_debug', 'ndims_'+ ndims)

else:
    results_dir = os.path.join(config['resultsdir'], result_name, rfun , 'ndims_'+ ndims)

try:
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
except OSError as err:
   print(err)



laplace = {'name': 'Laplace', 'weights': tc.laplace_weights, 'params': {'scale': width}}
delta = {'name': '$\delta$', 'weights': tc.eye_weights, 'params': tc.eye_params}
gaussian = {'name': 'Gaussian', 'weights': tc.gaussian_weights, 'params': {'var': width}}
mexican_hat = {'name': 'Mexican hat', 'weights': tc.mexican_hat_weights, 'params': {'sigma': width}}

factors = 700

if factors == 100:
    pieman_name = 'pieman_ica100.mat'
else:
    pieman_name = 'pieman_data.mat'

pieman_data = loadmat(os.path.join(config['datadir'], pieman_name))
pieman_conds = ['intact', 'paragraph', 'word', 'rest']


weights_paramter = eval(wp)


if debug:
    data_chunks = [0] * 3
    conds_chunks = [0] * 3
    divided = 0
    for third in list(range(3)):
        data = []
        conds = []
        for c in pieman_conds:
            next_data = list(map(lambda i: pieman_data[c][:, i][0][divided:divided+10,:20], np.arange(4)))
            data.extend(next_data)
            conds.extend([c]*len(next_data))

        conds_chunks[third] = conds
        data_chunks[third] = data
        divided += 10

    del pieman_data

else:

    data_chunks = [0] * 3
    conds_chunks = [0] * 3
    divided = 0
    for third in list(range(3)):
        data = []
        conds = []
        for c in pieman_conds:
            if c == 'paragraph':
                if factors == 700:
                    next_data = list(
                        map(lambda i: pieman_data[c][:, i][0][divided:divided+100,:], np.where(np.arange(pieman_data[c].shape[1]) != 3)[0]))
                else:
                    next_data = list(
                        map(lambda i: pieman_data[c][:, i][0][divided:divided+100,:], np.where(np.arange(pieman_data[c].shape[1]) != 0)[0]))
            else:
                next_data = list(map(lambda i: pieman_data[c][:, i][0], np.arange(pieman_data[c].shape[1])))

            data.extend(next_data)
            conds.extend([c]*len(next_data))

        conds_chunks[third] = conds
        data_chunks[third] = data
        divided += 100

    del pieman_data

chunks = 3


for chunk in range(chunks):

    data = np.array(data_chunks[chunk])
    conds = np.array(conds_chunks[chunk])

    append_iter = pd.DataFrame()

    iter_results = tc.helpers.pca_decoder(data[conds == cond], nfolds=2, dims=int(ndims),
                                        combine=mean_combine,
                                        cfun=eval(cfun),
                                        rfun=None,
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


