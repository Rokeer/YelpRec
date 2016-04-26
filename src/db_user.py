#coding: utf8

import sys
import json
import pickle
import numpy as np
from util import preprocess

import pdb

class UserInst(object):
    def __init__(self, obj):
        """ constructor. """
        self.obj = obj
        self.average_stars = obj["average_stars"]
        self.ratings = obj["ratings"]
        self.reviews = obj["reviews"]
        self.lda_repr = []
        self.history_records = dict()

    def __str__(self):
        """ return str for debug. """
        return json.dumps(self.obj)

    def infer_vectors(self, posDic, posLda, negDic, negLda):
        """ infer the topic vectors. """
        pos = ""
        neg = ""
        for (business_id, ratings, review) in self.reviews:
            if ratings >= 3:
                pos = pos + review
            if ratings < 3:
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

    def mark_history(self, history_records):
        """ mark history records. """
        self.history_records = history_records

class UserDB(object):

    def __init__(self, file_name):
        """ constructor. """
        self.db = dict()
        self.load(file_name)

    def load(self, file_name):
        """ load user db from text file. """
        with open(file_name, "r") as fp:
            print >> sys.stderr, "loading users data from %s..." %(file_name)
            for line in fp.readlines():
                items = line.split("\t")
                user_id, user_data = json.loads(items[0]), json.loads(items[1])

                self.db[user_id] = UserInst({
                    "user_id"   : user_id,
                    "review_count"  : user_data[0],
                    "average_stars" : user_data[1],
                    "ratings"       : user_data[2],
                    "votes"         : user_data[3],
                    "reviews"       : user_data[4]
                })
            print >> sys.stderr, "succ, %s records loaded" %(len(self.db))

    def mark_history(self, file_name):
        """ mark user history from file. """
        with open(file_name, "r") as fp:
            print >> sys.stderr, "loading history data from %s..." %(file_name)
            user_dict = pickle.load(fp)
            print >> sys.stderr, "succ, %s records loaded" %(len(user_dict))

            for user_id, user_inst in self.db.iteritems():
                user_inst.mark_history(user_dict.get(user_id, dict()))

    def keys(self):
        """ return keys. """
        return self.db.keys()
            
    def __getitem__(self, user_id):
        """ get user instance by id. """
        return self.db.get(user_id, None)

if __name__ == "__main__":
    user_db = UserDB("output/user.dat")
    user_db.mark_history("output/rating.train.0.history")
    a = user['V2IdhKBJXcl5t3cSZT6RNg']
    print a
