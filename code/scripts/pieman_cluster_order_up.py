
import timecorr as tc
from timecorr.helpers import isfc, corrmean_combine, reduce
from scipy.io import loadmat
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


result_name = 'corrs_ordered_up'

results_dir = os.path.join(config['resultsdir'], result_name, cfun + '_' + rfun + '_' + smooth + '_' + str(width))

try:
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
except OSError as err:
   print(err)

factors = 100

if factors == 100:
    pieman_name = 'pieman_ica100.mat'
else:
    pieman_name = 'pieman_data.mat'

pieman_data = loadmat(os.path.join(config['datadir'], pieman_name))

data = []
conds = []

if cond == 'paragraph':
    if factors == 700:
        next_data = list(
            map(lambda i: pieman_data[cond][:, i][0], np.where(np.arange(pieman_data[cond].shape[1]) != 3)[0]))
    else:
        next_data = list(
            map(lambda i: pieman_data[cond][:, i][0], np.where(np.arange(pieman_data[cond].shape[1]) != 0)[0]))
else:
    next_data = list(map(lambda i: pieman_data[cond][:, i][0], np.arange(pieman_data[cond].shape[1])))

data.extend(next_data)
conds.extend([cond] * len(next_data))

all_data = np.array(data)
conds = np.array(conds)

corrsdir = os.path.join(results_dir, smooth + '_' + str(50) + '_orderedup_corrs')

if not os.path.exists(corrsdir):
    os.makedirs(corrsdir)


combine = corrmean_combine

levels = range(3)

print(levels)

for lev in levels:

    if os.path.exists(os.path.join(corrsdir, 'd_' + str(lev) + '_' + cond + '.npy')):
        data = np.load(os.path.join(corrsdir, 'd_' + str(lev) + '_' + cond + '.npy'))
        print(str(lev) + '_data loaded')
    else:

        if lev == 0:
            lev_data = all_data[conds == cond]
        else:
            #assert data_r, 'data_r not defined'
            lev_data = data_r

        print('lev_data: ' + str(lev_data[0][0]))

        data = np.asarray(tc.timecorr([x for x in lev_data], cfun=isfc, rfun=None,
                                      weights_function=smooth_fun, weights_params=smooth_params))

        print('data: ' + str(data[0][0]))
        print(str(lev) + '_smooth data calculated')

        corr = tc.helpers.z2r(np.mean(tc.helpers.r2z(np.stack(data, axis=2)), axis=2))

        print(str(lev) + '_corrs calculated')

        np.save(os.path.join(corrsdir, 'lev_' + str(lev) + '_' + cond + '.npy'), corr)

        data = np.asarray(tc.timecorr([x for x in lev_data], cfun=isfc, rfun=None,
                                      weights_function=raw_fun, weights_params=raw_params))

        print(str(lev) + '_raw data calculated')

        np.save(os.path.join(corrsdir, 'd_' + str(lev) + '_' + cond + '.npy'), data)

    if os.path.exists(os.path.join(corrsdir, 'd_' + str(lev) + '_r_' + cond + '.npy')):
        data_r = np.load(os.path.join(corrsdir, 'd_' + str(lev) + '_r_' + cond + '.npy'))
        print(str(lev) + '_reduced data loaded')
    else:
        data_r = np.asarray(reduce([x for x in data], rfun=rfun))
        print(str(lev) + '_reduced data calculated')
        np.save(os.path.join(corrsdir, 'd_' + str(lev) + '_r_' + cond + '.npy'), data_r)

        print('data_r: ' + str(data_r[0][0]))
    del data