#coding: utf8

import numpy as np
import pdb

def load_data(file_name):
    """ load data set <user_id, business_id> -> rating from file. """
    data  = []
    label = []

    with open(file_name, "r") as fp:
        for line in fp.readlines():
            items = line.split("\t")
            data.append((items[0], items[1]))
            label.append(int(items[2]))

    return data, np.array(label).reshape((len(label), 1))

def compute_mse(labeled_vals, pred_vals):
    """ compute mse. """
    return ((pred_vals - labeled_vals) ** 2).mean()

def compute_rmse(labeled_vals, pred_vals):
    """ compute rmse. """
    return np.sqrt(((pred_vals - labeled_vals) ** 2).mean())

def compute_rsquared(labeled_vals, pred_vals):
    """ compute rsquared. """
    ss_tot = np.sum((labeled_vals - labeled_vals.mean()) ** 2)
    ss_res = np.sum((labeled_vals - pred_vals) ** 2)
    return 1.0 - ss_res / ss_tot

def compute_precision(labeled_vals, pred_vals):
    """ compute precision. """
    return 1.0 * np.sum(np.abs(labeled_vals - pred_vals) < 0.5) / labeled_vals.shape[0]

def evaluate(labeled_vals, pred_vals):
    """ evaluate results. """
    #print "mse:       %.4lf"  % (compute_mse(labeled_vals, pred_vals))
    #print "rmse:      %.4lf"  % (compute_rmse(labeled_vals, pred_vals))
    #print "R-squared: %.4lf"  % (compute_rsquared(labeled_vals, pred_vals))
    mse       = compute_mse(labeled_vals, pred_vals)
    rmse      = compute_rmse(labeled_vals, pred_vals)
    r_squared = compute_rsquared(labeled_vals, pred_vals)
    precision = compute_precision(labeled_vals, pred_vals)
    return mse, rmse, r_squared, precision
