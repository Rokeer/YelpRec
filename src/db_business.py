#coding: utf8

import sys
import json
import numpy as np
from util import preprocess

import pdb

class BusinessInst(object):
    def __init__(self, obj):
        """ constructor. """
        self.obj = obj
        self.stars = obj["stars"]
        self.ratings = obj["ratings"]
        self.pos_reviews = obj["pos_reviews"]
        self.neg_reviews = obj["neg_reviews"]

    def __str__(self):
        """ return str for debug. """
        return json.dumps(self.obj)

    def infer_vectors(self, posDic, posLda, negDic, negLda):
        """ infer the topic vectors. """
        pos = ""
        neg = ""
        for (ratings, review) in self.pos_reviews:
            pos = pos + review
        for (ratings, review) in self.neg_reviews:
            neg = neg + review

        pos_tuple = posLda[posDic.doc2bow(preprocess(pos))]
        neg_tuple = negLda[negDic.doc2bow(preprocess(neg))]

        pos_repr = [0] * posLda.num_topics
        neg_repr = [0] * negLda.num_topics
        for k, v in pos_tuple:
            pos_repr[k] = v
        for k, v in neg_tuple:
            neg_repr[k] = v
        self.lda_repr = pos_repr + neg_repr
        return self.lda_repr

class BusinessDB(object):

    def __init__(self, file_name):
        """ constructor. """
        self.db = dict()
        self.load(file_name)

    def load(self, file_name):
        """ load business db from text file. """
        with open(file_name, "r") as fp:
            print >> sys.stderr, "loading businesses data from %s..." %(file_name)
            for line in fp.readlines():
                items = line.split("\t")
                business_id, business_data = json.loads(items[0]), json.loads(items[1])

                self.db[business_id] = BusinessInst({
                    "business_id"   : business_id,
                    "stars"         : business_data[0], # this average score is provided by yelp
                    "ratings"       : business_data[1], # this average score is computed by ourselves
                    "review_count"  : business_data[2],
                    "categories"    : business_data[3],
                    "pos_reviews"   : business_data[4],
                    "neg_reviews"   : business_data[5]
                })
            print >> sys.stderr, "succ, %s records loaded" %(len(self.db))

    def __getitem__(self, business_id):
        """ get business instance by id. """
        return self.db.get(business_id, None)

    def keys(self):
        """ retur keys. """
        return self.db.keys()

if __name__ == "__main__":
    business = BusinessDB()
    business.load("output/business.dat")
    a = business['UrM01YK5HirPueJKQX147A']
    pdb.set_trace()
    print a.stars()
