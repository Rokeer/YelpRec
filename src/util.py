#coding: utf8

import pdb
import numpy as np
from stop_words import get_stop_words
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer

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
    mse       = compute_mse(labeled_vals, pred_vals)
    rmse      = compute_rmse(labeled_vals, pred_vals)
    r_squared = compute_rsquared(labeled_vals, pred_vals)
    precision = compute_precision(labeled_vals, pred_vals)
    return mse, rmse, r_squared, precision

def preprocess(line):
    """ preprocess line. """
    tokenizer = RegexpTokenizer(r'\w+')
    en_stop = get_stop_words('en')
    p_stemmer = PorterStemmer()
    raw = line.lower()
    tokens = tokenizer.tokenize(raw)
    stopped_tokens = [i for i in tokens if not i in en_stop]
    stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]
    return stemmed_tokens
