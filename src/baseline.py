#coding: utf8

from util import *
import numpy as np
from db_business import *
from db_user import *
import pdb

def predict_using_business_stars(test_data):
    """ using business stars to predict. """
    pred_vals = np.zeros((len(test_data), 1))
    for i, (user_id, business_id) in enumerate(test_data):
        pred_vals[i] = db_business[business_id].stars()
    return pred_vals

def predict_using_business_ratings(test_data):
    """ using business ratings to predict. """
    pred_vals = np.zeros((len(test_data), 1))
    for i, (user_id, business_id) in enumerate(test_data):
        pred_vals[i] = db_business[business_id].ratings()
    return pred_vals

def predict_using_user_stars(test_data):
    """ using user stars to predict. """
    pred_vals = np.zeros((len(test_data), 1))
    for i, (user_id, business_id) in enumerate(test_data):
        pred_vals[i] = db_user[user_id].stars()
    return pred_vals

def predict_using_user_ratings(test_data):
    """ using user ratings to predict. """
    pred_vals = np.zeros((len(test_data), 1))
    for i, (user_id, business_id) in enumerate(test_data):
        pred_vals[i] = db_user[user_id].ratings()
    return pred_vals

if __name__ == "__main__":
    db_business = BusinessDB("output/business.dat")
    db_user     = UserDB("output/user.dat")

    pred_funcs = [
        ("using business' stars provided by yelp",  predict_using_business_stars),
        ("using business' ratings:",                predict_using_business_ratings),
        ("using user's stars provided by yelp",     predict_using_user_stars),
        ("using user's ratings",                    predict_using_user_ratings)
    ]

    for desc, func in pred_funcs:
        mse  = np.zeros((10, 1))
        rmse = np.zeros((10, 1))
        r_squared = np.zeros((10, 1))
        precision = np.zeros((10, 1))

        for t in xrange(10):
            train_data, train_labels = load_data("output/rating.train.%s" %(t))
            test_data,  test_labels  = load_data("output/rating.test.%s" %(t))

            pred_vals = func(test_data)
            mse[t], rmse[t], r_squared[t], precision[t] = evaluate(test_labels, pred_vals)

        print desc
        print "mse:       %.4lf"  % (mse.mean())
        print "rmse:      %.4lf"  % (rmse.mean())
        print "R-squared: %.4lf"  % (r_squared.mean())
        print "Precision: %.4lf"  % (precision.mean())
