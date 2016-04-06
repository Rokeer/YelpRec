#coding: utf8

import sys
import json
import numpy as np

np.random.seed(477)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print >> sys.stderr, "Usage: %s origin train_file test_file" %(sys.argv[0])
        exit(-1)

    lines = []
    with open(sys.argv[1], "r") as fp:
        for line in fp.readlines():
            items = line.split("\t")
            user_id, user_data = json.loads(items[0]), json.loads(items[1])
            review_count, average_stars, ratings, votes, reviews = user_data
            for (business_id, stars, text) in reviews:
                lines.append("%s\t%s\t%s\n" % (user_id, business_id, stars))

    np.random.shuffle(lines)

    """ generate dataset for cross-validation. """
    batches_num = 10
    batches_size = len(lines) / batches_num

    for t in xrange(10):
        fp1 = open("%s.%s" %(sys.argv[2], t), "w")
        fp2 = open("%s.%s" %(sys.argv[3], t), "w")
        for i, line in enumerate(lines):
            if i >= t * batches_size and i < (t + 1) * batches_size:
                fp2.write(line)
            else:
                fp1.write(line)
        fp1.close()
        fp2.close()
