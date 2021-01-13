import numpy as np
import pandas as pd
from scipy.linalg import toeplitz
import sys
import os
from config import config
import timecorr as tc
from matplotlib import pyplot as plt

cond= sys.argv[1]
r = sys.argv[2] #reps

F = sys.argv[3] #number of features
T = sys.argv[4] #number of timepoints
K = 2 #order

fname = cond + '_' + str(F) + '_' + str(T) + '_' + str(K)

width = 20

results_dir = os.path.join(config['resultsdir'], 'higher_order_sims_search', cond + '_' + str(T)+ '_' + str(K))

try:
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
except OSError as err:
   print(err)



def expanded_vec2mat(v):
  m = tc.vec2mat(v)
  x = np.zeros([v.shape[0], m.shape[0] ** 2])
  for t in range(m.shape[2]):
    x[t, :] = m[:, :, t].ravel()
  return x


laplace = {'name': 'Laplace', 'weights': tc.laplace_weights, 'params': {'scale': width}}

eye_params = {}

def eye_weights(T, params=eye_params):
    return np.eye(T)

def generate_templates(order=1, **kwargs):
  kwargs['return_corrs'] = True
  _, next_template = tc.simulate_data(**kwargs)

  T = kwargs['T']
  templates = []
  for n in range(order - 1):
    templates.append(next_template)

    expanded_corrmats = tc.vec2mat(next_template)
    K2 = expanded_corrmats.shape[0] ** 2
    next_template = np.zeros([K2, K2, T])
    for t in range(T):
      x = np.atleast_2d(expanded_corrmats[:, :, t].ravel())
      next_template[:, :, t] = x * x.T
    next_template = tc.mat2vec(next_template)
  templates.append(next_template)
  return templates


def generate_data(templates):
    order = len(templates) + 1
    adjusted_templates = [templates[-1]]  # generate adjusted templates in reverse order
    next_corrmats = adjusted_templates[-1]

    for n in range(order - 1, 1, -1):
        corrmats = tc.vec2mat(next_corrmats)
        K = corrmats.shape[0]
        sK = int(np.sqrt(K))
        T = corrmats.shape[2]

        draws = np.zeros([sK, sK, T])
        means = tc.vec2mat(templates[n - 2])

        for t in range(T):
            draws[:, :, t] = np.reshape(np.random.multivariate_normal(means[:, :, t].ravel(), corrmats[:, :, t]),
                                        [sK, sK])

        next_corrmats = tc.mat2vec(draws)
        adjusted_templates.append(next_corrmats)

    corrmats = tc.vec2mat(next_corrmats)
    K = int(corrmats.shape[0])
    T = corrmats.shape[2]
    data = np.zeros([T, K])

    for t in range(T):
        data[t, :] = np.random.multivariate_normal(np.zeros([K]), corrmats[:, :, t])

    adjusted_templates.reverse()
    return data, adjusted_templates


save_file = os.path.join(results_dir, str(r))

if not os.path.exists(save_file):

    recovery_performance_all = pd.DataFrame()

    templates = generate_templates(order=K, S=1, T=T, K=F, datagen=cond)

    data, adjusted_templates = generate_data(templates)

    get_f = lambda y: int((1/2) * (np.sqrt(8*y + 1) - 1)) #solve for x in y = ((x^2 - x)/2) + x


    recovery_performance = pd.DataFrame(index=np.arange(T), columns=np.arange(1, K+1))
    recovery_performance.index.name = 'time'
    recovery_performance.columns.name = 'order'
    next_data = data
    recovered_corrs_raw = []
    recovered_corrs_smooth = []
    for k in np.arange(1, K+1):
      next_recovered_smooth = tc.timecorr(next_data, weights_function=laplace['weights'], weights_params=laplace['params'])
      next_recovered_raw = tc.timecorr(next_data, weights_function=eye_weights, weights_params=eye_params)
      recovered_corrs_smooth.append(next_recovered_smooth)
      F_new = get_f(next_recovered_smooth.shape[1])
      for t in np.arange(T):
        recovery_performance.loc[t, k] = np.corrcoef(templates[k-1][t, F_new:], next_recovered_smooth[t, F_new:])[0, 1]

      next_data = expanded_vec2mat(next_recovered_raw)

    # recovery_performance.columns = [str(x + 1) for x in np.arange(K)]
    #
    # recovery_performance['iteration'] = int(r)

    #recovery_performance_all = recovery_performance_all.append(recovery_performance)

    print(recovery_performance)

    recovery_performance.to_csv(save_file + '.csv')

# if not os.path.isfile(save_file + '.csv'):
#     recovery_performance.to_csv(save_file + '.csv')
# else:
#     append_iter = pd.read_csv(save_file + '.csv', index_col=0)
#     append_iter = append_iter.append(recovery_performance)
#     append_iter.to_csv(save_file + '.csv')

