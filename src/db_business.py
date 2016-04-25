#coding: utf8

import sys
import json
import numpy as np

import pdb

class BusinessInst(object):
    def __init__(self, obj):
        """ constructor. """
        self.obj = obj

    def __str__(self):
        """ return str for debug. """
        return json.dumps(self.obj)

    def stars(self):
        """ return the stars. """
        return self.obj["stars"]

    def ratings(self):
        """ return the ratings. """
        return self.obj["ratings"]

    def infer_vectors(self):
        """ TODO: infer the topic vectors. """
        pass

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

                self.db[business_id] = {
                    "business_id"   : business_id,
                    "stars"         : business_data[0], # this average score is provided by yelp
                    "ratings"       : business_data[1], # this average score is computed by ourselves
                    "review_count"  : business_data[2],
                    "categories"    : business_data[3],
                    "pos_reviews"   : business_data[4],
                    "neg_reviews"   : business_data[5]
                }
            print >> sys.stderr, "succ, %s records loaded" %(len(self.db))

    def __getitem__(self, business_id):
        """ get business instance by id. """
        obj = self.db.get(business_id, None)
        if obj is None:
            return None
        return BusinessInst(obj)

if __name__ == "__main__":
    business = BusinessDB()
    business.load("output/business.dat")
    a = business['UrM01YK5HirPueJKQX147A']
    pdb.set_trace()
    print a.stars()
