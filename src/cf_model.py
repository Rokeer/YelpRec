#coding: utf8

import pdb
import sys
import pickle

class cf_model(object):
    def __init__(self):
        self.business_count = dict()
        self.business_business_count = dict()

    def load(self, file_name):
        """ load data. """
        with open(file_name, "r") as fp:
            print >> sys.stderr, "loading history data from %s..." %(file_name)
            user_dict = pickle.load(fp)
            print >> sys.stderr, "succ, %s records loaded" %(len(user_dict))

            """ compute business_count, business_business_count. """
            business_count = self.business_count
            business_business_count = self.business_business_count

            """ business_count. """
            for user_id, business_dict in user_dict.iteritems():
                for business_id in business_dict:
                    business_count.setdefault(business_id, 0)
                    business_count[business_id] += 1

            """ business_business_count. """
            for user_id, business_dict in user_dict.iteritems():
                ids = sorted(business_dict.keys())
                for i in xrange(len(ids)):
                    for j in xrange(i + 1, len(ids)):
                        key = ids[i] + "::" + ids[j]
                        business_business_count.setdefault(key, 0)
                        business_business_count[key] += 1

    def load_pickle(self, file_name):
        """ load data. """
        with open(file_name, "r") as fp:
            self.business_count = pickle.load(fp)
            self.business_business_count = pickle.load(fp)
            print >> sys.stderr, "load done"

    def save_pickle(self, file_name):
        """ save data. """
        with open(file_name, "w") as fp:
            pickle.dump(self.business_count, fp)
            pickle.dump(self.business_business_count, fp)
            print >> sys.stderr, "save done"

if __name__ == "__main__":
    cf = cf_model()
    cf.load("output/rating.train.0.history")
    cf.save_pickle("a.pkl")
    pdb.set_trace()
