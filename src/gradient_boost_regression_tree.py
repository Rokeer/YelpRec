#coding: utf8

import pdb
import json
import sys
import numpy as np
from util import *
from sklearn.ensemble import GradientBoostingRegressor

def load_users(file_name):
    """ load users' feature. """
    dct = dict()
    with open(file_name, "r") as fp:
        items = [ line.strip("\n").split("\t") for line in fp.readlines() ]
        for item in items:
            dct[item[0]] = (float(item[1]), float(item[2]), json.loads(item[3]))
    print >> sys.stderr, "users loaded"
    return dct

def load_businesses(file_name):
    """ load businesses' feature. """
    dct = dict()
    with open(file_name, "r") as fp:
        items = [ line.strip("\n").split("\t") for line in fp.readlines() ]
        for item in items:
            dct[item[0]] = (float(item[1]), float(item[2]), json.loads(item[3]))
    print >> sys.stderr, "businesses loaded"
    return dct

def load_data(file_name):
    with open(file_name, "r") as fp:
        items = [ line.strip("\n").split("\t") for line in fp.readlines() ]
        items = map(lambda x: (x[0], x[1], float(x[2])), items)

        vecs = []
        y = []
        for item in items:
            u = users.get(item[0])
            b = businesses.get(item[1])
            if u and b:
                u_star1, u_star2, u_lda = u
                b_star1, b_star2, b_lda = b
                vec = [u_star1, u_star2, b_star1, b_star2] + u_lda + b_lda
                vecs.append(vec)
                y.append(item[2])

        x = np.zeros((len(vecs), len(vecs[0])))
        for i, vec in enumerate(vecs):
            x[i, :] = np.array(vec)
        y = np.array(y)
    return x, y

if __name__ == "__main__":
    users = load_users("output/user.lda")
    businesses = load_businesses("output/business.lda")

    mse = np.zeros((10, 1))
    rmse = np.zeros((10, 1))
    r_squared = np.zeros((10, 1))
    precision = np.zeros((10, 1))

    for t in xrange(10):
        x_train, y_train = load_data("output/rating.train.%s" %(t))
        x_test, y_test = load_data("output/rating.test.%s" %(t))

        regr = GradientBoostingRegressor(n_estimators=40, learning_rate=0.1, max_depth=2, random_state=0, loss='ls')
        regr.fit(x_train, y_train)

        y_pred = regr.predict(x_test)
        mse[t], rmse[t], r_squared[t], precision[t] = evaluate(y_test, y_pred)
        print >> sys.stderr, "cross validation", t, "done"

    print "mse:       %.4lf"  % (mse.mean())
    print "rmse:      %.4lf"  % (rmse.mean())
    print "R-squared: %.4lf"  % (r_squared.mean())
    print "Precision: %.4lf"  % (precision.mean())
