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

    for t in xrange(1):
        file_object = np.load("output/raw_feature.%s" %(t))
        x_train = file_object["x_train"]
        y_train = file_object["y_train"]
        x_test = file_object["x_test"]
        y_test = file_object["y_test"]

        with open("output/libfm.train.%s" %(t), "w") as fp:
            for i in xrange(x_train.shape[0]):
                items = []
                for j in xrange(x_train.shape[1]):
                    items.append("%s:%.8lf" %(j, x_train[i, j]))
                line = "%s %s" %(y_train[i], " ".join(items))
                fp.write(line + "\n")

        with open("output/libfm.test.%s" %(t), "w") as fp:
            for i in xrange(x_test.shape[0]):
                items = []
                for j in xrange(x_test.shape[1]):
                    items.append("%s:%.8lf" %(j, x_test[i, j]))
                line = "%s %s" %(y_train[i], " ".join(items))
                fp.write(line + "\n")
