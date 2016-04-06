#coding: utf8

import sys
import json
import numpy as np

import pdb

class UserInst(object):
    def __init__(self, obj):
        """ constructor. """
        self.obj = obj

    def __str__(self):
        """ return str for debug. """
        return json.dumps(self.obj)

    def stars(self):
        """ return the stars . """
        return self.obj["average_stars"]

    def ratings(self):
        """ return the ratings. """
        return self.obj["ratings"]

    def infer_vectors(self):
        """ TODO: infer the topic vectors. """
        pass

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

                self.db[user_id] = {
                    "user_id"   : user_id,
                    "review_count"  : user_data[0],
                    "average_stars" : user_data[1],
                    "ratings"       : user_data[2],
                    "votes"         : user_data[3],
                    "reviews"       : user_data[4]
                }
            print >> sys.stderr, "succ, %s records loaded" %(len(self.db))

    def __getitem__(self, user_id):
        """ get user instance by id. """
        obj = self.db.get(user_id, None)
        if obj is None:
            return None
        return UserInst(obj)

if __name__ == "__main__":
    user = UserDB("output/user.dat")
    a = user['V2IdhKBJXcl5t3cSZT6RNg']
    print a.stars()
