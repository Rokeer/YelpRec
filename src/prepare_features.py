#coding: utf8

from util import *
import numpy as np
import gensim
from gensim import corpora
from db_business import *
from db_user import *
import pdb

if __name__ == "__main__":
    lda_pos_dict  = corpora.Dictionary.load_from_text("model/train_pos_lda_dic.dat")
    lda_neg_dict  = corpora.Dictionary.load_from_text("model/train_neg_lda_dic.dat")
    lda_pos_model = gensim.models.ldamodel.LdaModel.load("model/train_pos_lda_model")
    lda_neg_model = gensim.models.ldamodel.LdaModel.load("model/train_neg_lda_model")

    db_business = BusinessDB("output/business.dat")
    db_user     = UserDB("output/user.dat")

    for business_id in db_business.keys():
        db_business[business_id].infer_vectors(lda_pos_dict, lda_pos_model, lda_neg_dict, lda_neg_model)

    for user_id in db_user.keys():
        db_user[user_id].infer_vectors(lda_pos_dict, lda_pos_model, lda_neg_dict, lda_neg_model)

    exit(0)

    for t in xrange(10):
        db_user.mark_history("output/rating.train.%s.history" %(t))
        train_data, train_labels = load_data("output/rating.train.%s" %(t))
        test_data,  test_labels  = load_data("output/rating.test.%s" %(t))

        pred_vals = func(test_data)
        mse[t], rmse[t], r_squared[t], precision[t] = evaluate(test_labels, pred_vals)
