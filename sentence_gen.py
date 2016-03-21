#coding: utf8

import os
import sys
import math
import time
import json
import pickle
from sklearn.externals import joblib
from sklearn.feature_extraction.text import CountVectorizer
import pdb

if __name__ == "__main__":
    print >> sys.stderr, "loading from STDIN..."

    """ read from input. """
    with open("output/language_model.train", "r") as fp:
        lines = [ line.strip("\n") for line in fp.readlines() ]

    """ initialize vectorizer. """
    sents = [ line.split("\t")[0] for line in lines ]
    vectorizer = CountVectorizer(min_df=1, stop_words="english")
    X = vectorizer.fit_transform(sents)

    pdb.set_trace()
