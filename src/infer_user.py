#coding: utf8

from util import *
import numpy as np
import gensim
from gensim import corpora
from db_business import *
from db_user import *
import json
import pdb

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print >> sys.stderr, "usage: %s file_name" %(sys.argv[0])
        exit(-1)
    
    file_name = sys.argv[1]

    lda_pos_dict  = corpora.Dictionary.load_from_text("model/train_pos_lda_dic.dat")
    lda_neg_dict  = corpora.Dictionary.load_from_text("model/train_neg_lda_dic.dat")
    lda_pos_model = gensim.models.ldamodel.LdaModel.load("model/train_pos_lda_model")
    lda_neg_model = gensim.models.ldamodel.LdaModel.load("model/train_neg_lda_model")

    db_user = UserDB("output/user.dat")

    with open(file_name, "w") as fp:
        for i, user_id in enumerate(db_user.keys()):
            inst = db_user[user_id]
            vec = inst.infer_vectors(lda_pos_dict, lda_pos_model, lda_neg_dict, lda_neg_model)

            line = "%s\t%.2lf\t%.2lf\t%s" %(user_id, inst.average_stars, inst.ratings, json.dumps(vec))
            fp.write(line + "\n")
            if i % 100 == 0:
                print >> sys.stderr, "inferring user vector, %s" %(i)
