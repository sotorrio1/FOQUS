from operator import lt, gt
import numpy as np

def criterion(cand,    # candidates
              include, # columns to include in distance computation
              scl,     # scaling factors for included columns
              nr,      # number of restarts (e.g., random combinations of <nd> points)
              nd,      # design size <= len(candidates)
              mode='maximin', hist=[]):

    best_cand = []
    best_rand_sample = []
    mode = mode.lower()
    assert mode in ['maximin', 'minimax'], 'MODE %s not recognized.' % mode
    if mode == 'maximin':
        best_val = -1
        fcn = np.mean
        cond = gt
    elif mode == 'minimax':
        best_val = 99999
        fcn = np.max
        cond = lt

    if hist:
        hist = hist[include].values

    assert(nd <= len(cand))  # this should have been checked in GUI

    for i in range(nr):

        rand_index = np.random.choice(len(cand), nd, replace=False)
        rand_cand = cand.iloc[rand_index]
        dist_mat = compute_dist(rand_cand[include].values, scl, hist=hist)
        min_dist = np.min(dist_mat, axis=0)
        dist = fcn(min_dist)

        if cond(dist, best_val):
            best_cand = rand_cand    
            best_index = rand_index  # for debugging
            best_val = dist          # for debugging
            best_dmat = dist_mat     # used for ranking candidates

    return best_cand, best_index, best_val, best_dmat