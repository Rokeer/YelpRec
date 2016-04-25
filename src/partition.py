#coding: utf8

import sys
import json
import pickle
import numpy as np

np.random.seed(477)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print >> sys.stderr, "Usage: %s origin train_file test_file" %(sys.argv[0])
        exit(-1)

    records = []
    with open(sys.argv[1], "r") as fp:
        for line in fp.readlines():
            items = line.split("\t")
            user_id, user_data = json.loads(items[0]), json.loads(items[1])
            review_count, average_stars, ratings, votes, reviews = user_data
            for (business_id, stars, text) in reviews:
                records.append((user_id, business_id, stars))

    np.random.shuffle(records)

    """ generate dataset for cross-validation. """
    batches_num = 10
    batches_size = len(records) / batches_num

    for t in xrange(10):
        userdict = dict()
        fp1 = open("%s.%s" %(sys.argv[2], t), "w")
        fp2 = open("%s.%s" %(sys.argv[3], t), "w")
        for i, (user_id, business_id, stars) in enumerate(records):
            line = "%s\t%s\t%s\n" %(user_id, business_id, stars)
            if i >= t * batches_size and i < (t + 1) * batches_size:
                fp2.write(line)
            else:
                userdict.setdefault(user_id, set()).add(business_id)
                fp1.write(line)
        fp1.close()
        fp2.close()

        with open("%s.%s.history" %(sys.argv[2], t), "wb") as fp:
            pickle.dump(userdict, fp)
