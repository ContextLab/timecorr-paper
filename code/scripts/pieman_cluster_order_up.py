
import timecorr as tc
from timecorr.helpers import isfc, reduce, autofc
from scipy.io import loadmat
import numpy as np
import sys
import os
from config import config


level = sys.argv[1]
cfun = sys.argv[2]
rfun = sys.argv[3]
width = int(sys.argv[4])

laplace = {'name': 'Laplace', 'weights': tc.laplace_weights, 'params': {'scale': width}}
delta = {'name': '$\delta$', 'weights': tc.eye_weights, 'params': tc.eye_params}
gaussian = {'name': 'Gaussian', 'weights': tc.gaussian_weights, 'params': {'var': width}}
mexican_hat = {'name': 'Mexican hat', 'weights': tc.mexican_hat_weights, 'params': {'sigma': width}}

smooth = sys.argv[5]
raw = 'delta'

smooth_parameter = eval(smooth)
raw_parameter = eval(raw)

smooth_fun = smooth_parameter['weights']
smooth_params = smooth_parameter['params']
raw_fun = raw_parameter['weights']
raw_params = raw_parameter['params']

p_cfun = eval('autofc')

result_name = 'corrs_ordered'

corrsdir = os.path.join(config['resultsdir'], result_name, cfun + '_' + rfun + '_' + smooth + '_' + str(width))

try:
    if not os.path.exists(corrsdir):
        os.makedirs(corrsdir)
except OSError as err:
   print(err)

factors = 100

if factors == 100:
    pieman_name = 'pieman_ica100.mat'
else:
    pieman_name = 'pieman_data.mat'

pieman_data = loadmat(os.path.join(config['datadir'], pieman_name))

pieman_conds = ['intact', 'paragraph', 'word', 'rest']

for cond in pieman_conds:

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


    levels = range(int(level))

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

            #corr = tc.helpers.z2r(np.mean(tc.helpers.r2z(np.stack(data, axis=2)), axis=2))

            print(str(lev) + '_corrs calculated')

            np.save(os.path.join(corrsdir, 'lev_' + str(lev) + '_' + cond + '.npy'), data)

            data = np.asarray(tc.timecorr([x for x in lev_data], cfun=p_cfun, rfun=None,
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

### to combine across patients:

# data_dir = '/dartfs/rc/lab/D/DBIC/CDL/f002s72/timecorr_paper/pieman/results'
# corrs_dir = os.path.join(data_dir, 'laplace_50_orderedup_corrs')
#
# levels = np.arange(0,16,1)
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