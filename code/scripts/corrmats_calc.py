
import os
import numpy as np
from scipy.io import loadmat
import timecorr as tc
import scipy.spatial.distance as sd
from timecorr.helpers import isfc, autofc, mean_combine, corrmean_combine, vec2mat, reduce

figdir = '../figs'
if not os.path.exists(figdir):
    os.mkdir(figdir)

def squareform_timepoints_corr(data, order=0):
    if not order == 0:
        for o in range(order):
            data = np.asarray(tc.timecorr([x for x in data], cfun=autofc, rfun=rfun,
                                          weights_function=weights_fun, weights_params=weights_params))
    sq_corr = np.array([])
    for i in data:
        corr = np.corrcoef(i)
        if sq_corr.size == 0:
            sq_corr = sd.squareform(corr, checks=False)
        else:
            sq_corr = np.vstack((sq_corr, sd.squareform(corr, checks=False)))
    return sq_corr

factors = 700

if factors == 100:
    pieman_name = '../../data/pieman_ica100.mat'
else:
    pieman_name = '../../data/pieman_data.mat'


pieman_data = loadmat(pieman_name)

pieman_conds = ['intact', 'paragraph', 'word', 'rest']

debug = False


data = []
conds = []
for c in pieman_conds:
    if c == 'paragraph':
        if factors == 700:
            next_data = list(map(lambda i: pieman_data[c][:, i][0][:272,:], np.where(np.arange(pieman_data[c].shape[1]) != 3)[0]))
        else:
            next_data = list(map(lambda i: pieman_data[c][:, i][0][:272,:], np.where(np.arange(pieman_data[c].shape[1]) != 0)[0]))
    else:
        next_data = list(map(lambda i: pieman_data[c][:, i][0][:272,:], np.arange(pieman_data[c].shape[1])))
    data.extend(next_data)
    conds.extend([c]*len(next_data))



all_data = np.array(data)
conds = np.array(conds)


cfun = isfc
rfun = 'PCA'
width = 10
wp = 'gaussian'
cond = 'intact'
level = 1

gaussian = {'name': 'Gaussian', 'weights': tc.gaussian_weights, 'params': {'var': width}}

weights_paramter = eval(wp)


weights_fun=weights_paramter['weights']
weights_params=weights_paramter['params']
combine = corrmean_combine

all_stack_2 = np.array([])
factor_list = [0]
factor_list_sum = 0
for c in pieman_conds:
    c_stack = squareform_timepoints_corr(all_data[conds == c], order=2)
    factor_list.append(factor_list[-1] + len(c_stack))
    if all_stack_2.size == 0:
        all_stack_2 = c_stack
    else:
        all_stack_2 = np.vstack((all_stack_2,c_stack))