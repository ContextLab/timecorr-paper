
import timecorr as tc
from timecorr.helpers import isfc, reduce, autofc
from scipy.io import loadmat
import numpy as np
import sys
import os
import subprocess
from config import config

delta = {'name': '$\delta$', 'weights': tc.eye_weights, 'params': tc.eye_params}

cond = sys.argv[1]
level = 10
cfun = 'autofc'
rfun = 'eigenvector_centrality'
raw = 'delta'

raw_parameter = eval(raw)

raw_fun = raw_parameter['weights']
raw_params = raw_parameter['params']

p_cfun = eval(cfun)

result_name = 'corrs_ordered_ec'

corrsdir = os.path.join(config['resultsdir'], result_name, cfun + '_' + rfun)

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
        subprocess.run(['rm', os.path.join(corrsdir, 'd_' + str(lev) + '_' + cond + '.npy')])

        print(str(lev) + '_data loaded')
    else:

        if lev == 0:
            lev_data = all_data[conds == cond]
        else:
            #assert data_r, 'data_r not defined'
            lev_data = data_r

        print('lev_data: ' + str(lev_data[0][0]))


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
        subprocess.run(['rm', os.path.join(corrsdir, 'd_' + str(lev) + '_' + cond + '.npy')])
        print('data_r: ' + str(data_r[0][0]))
    del data
