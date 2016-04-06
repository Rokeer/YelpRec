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
    train_data, train_labels = load_data("output/rating.train")
    test_data,  test_labels  = load_data("output/rating.test")

    db_business = BusinessDB("output/business.dat")
    db_user     = UserDB("output/user.dat")

    print

    # using business' stars provided by yelp
    print "using business' stars provided by yelp:"
    pred_vals = predict_using_business_stars(test_data)
    evaluate(test_labels, pred_vals)
    print

    # using business' ratings
    print "using business' ratings:"
    pred_vals = predict_using_business_ratings(test_data)
    evaluate(test_labels, pred_vals)
    print

    # using user' stars provided by yelp
    print "using user's stars provided by yelp:"
    pred_vals = predict_using_user_stars(test_data)
    evaluate(test_labels, pred_vals)
    print

    # using user's ratings
    print "using user's ratings:"
    pred_vals = predict_using_user_ratings(test_data)
    evaluate(test_labels, pred_vals)
    print
