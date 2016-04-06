#coding: utf8

import sys
import json
import numpy as np

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print >> sys.stderr, "Usage: %s origin train_file test_file" %(sys.argv[0])
        exit(-1)

    fp_train = open(sys.argv[2], "w")
    fp_test  = open(sys.argv[3], "w")

    lines_train = []
    lines_test  = []
    with open(sys.argv[1], "r") as fp:
        for line in fp.readlines():
            items = line.split("\t")
            user_id, user_data = json.loads(items[0]), json.loads(items[1])
            review_count, average_stars, ratings, votes, reviews_train, reviews_test = user_data
            for (business_id, stars, text) in reviews_train:
                lines_train.append("%s\t%s\t%s\n" % (user_id, business_id, stars))
            for (business_id, stars, text) in reviews_test:
                lines_test.append("%s\t%s\t%s\n" % (user_id, business_id, stars))

    np.random.shuffle(lines_train)
    np.random.shuffle(lines_test)

    with open(sys.argv[2], "w") as fp:
        for line in lines_train:
            fp.write(line)
    with open(sys.argv[3], "w") as fp:
        for line in lines_test:
            fp.write(line)
