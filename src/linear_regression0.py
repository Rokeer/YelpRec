#coding: utf8

import pdb
import json
import sys
import numpy as np
from util import *
from sklearn import linear_model

if __name__ == "__main__":
    mse = np.zeros((10, 1))
    rmse = np.zeros((10, 1))
    r_squared = np.zeros((10, 1))
    precision = np.zeros((10, 1))

    for t in xrange(10):
        file_object = np.load("output/raw_feature.%s" %(t))
        x_train = file_object["x_train"][:, :4]
        y_train = file_object["y_train"]
        x_test = file_object["x_test"][:, :4]
        y_test = file_object["y_test"]

        regr = linear_model.LinearRegression()
        regr.fit(x_train, y_train)

        y_pred = regr.predict(x_test)
        mse[t], rmse[t], r_squared[t], precision[t] = evaluate(y_test, y_pred)
        print >> sys.stderr, "cross validation %s done, r_squared=%.4lf, precision=%.4lf" %(t, r_squared[t], precision[t])

    print "mse:       %.4lf"  % (mse.mean())
    print "rmse:      %.4lf"  % (rmse.mean())
    print "R-squared: %.4lf"  % (r_squared.mean())
    print "Precision: %.4lf"  % (precision.mean())
