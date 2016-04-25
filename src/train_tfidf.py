#coding: utf8

import os
import sys
import json
from sklearn.externals import joblib
from sklearn.feature_extraction.text import TfidfVectorizer

def load_data(filename):
    """ create corpus from the file. """
    sents = []

    with open(filename, "r") as fp:
        for line_id, line in enumerate(fp):
            review = json.loads(line.split("\t")[0])
            sents.append(" ".join(review.split("\n")) )
            if (1 + line_id) % 1000 == 0:
                print >> sys.stderr, "scanning file, line_id=%s\r" %(1 + line_id),
        print >> sys.stderr, "scanning file, line_id=%s" %(1 + line_id)
    return sents

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print >> sys.stderr, "Usage: %s train_file" %(sys.argv[0])
        exit(-1)

    # create tf-idf model
    x_train = load_data(sys.argv[1])
    vectorizer = TfidfVectorizer(min_df=1, stop_words="english")
    x_train = vectorizer.fit_transform(x_train)
    joblib.dump(vectorizer, "model/tfidf.pkl")
    print >> sys.stderr, "saved to model/tfidf.pkl"
