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
        

        n_train = x_train.shape[0]
        x_train2 = np.zeros((n_train,6))
        n_test = x_test.shape[0]
        x_test2 = np.zeros((n_test,6))

        x_train2[:,0:4] = x_train[:,0:4]
        x_test2[:,0:4] = x_test[:,0:4]
        print "Start cal cos"
        for i in xrange(n_train):
            x_train2[i,4] = cosine_similarity(x_train[i,4:54],x_train[i,104:154])
            x_train2[i,5] = cosine_similarity(x_train[i,54:104],x_train[i,154:204])
        for i in xrange(n_test):
            x_test2[i,4] = cosine_similarity(x_test[i,4:54],x_test[i,104:154])
            x_test2[i,5] = cosine_similarity(x_test[i,54:104],x_test[i,154:204])    
        print "End cal cos"
        #pdb.set_trace()
        x_train = x_train2
        x_test = x_test2

        regr = linear_model.LinearRegression()
        regr.fit(x_train, y_train)

        y_pred = regr.predict(x_test)
        mse[t], rmse[t], r_squared[t], precision[t] = evaluate(y_test, y_pred)
        print >> sys.stderr, "cross validation %s done, r_squared=%.4lf, precision=%.4lf" %(t, r_squared[t], precision[t])

    print "mse:       %.4lf"  % (mse.mean())
    print "rmse:      %.4lf"  % (rmse.mean())
    print "R-squared: %.4lf"  % (r_squared.mean())
    print "Precision: %.4lf"  % (precision.mean())
