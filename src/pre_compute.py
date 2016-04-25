#coding: utf8

import sys
import json
import pickle
import numpy as np
from cf_model import cf_model

if __name__ == "__main__":
    t = int(sys.argv[1])
    cf = cf_model()
    cf.load("output/rating.train.%s.history" %(t))
    cf.save_pickle("output/cf.%s" %(t))
