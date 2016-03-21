#coding: utf8

import os
import sys
import json
from sklearn.externals import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import chi2
from sklearn.feature_selection import SelectKBest
from sklearn.linear_model import LogisticRegression
import pdb

def load_data(filename):
    """ build the corpus from the file. """

    sents = []
    labels = []

    with open(filename, "r") as fp:
        for line_id, line in enumerate(fp):
            items = json.loads(line.split("\t")[1])
            stars, categories, attributes, reviews, tips = items

            for review_id, (votes, stars, review) in enumerate(reviews):
                sent = " ".join(review.split("\n"))

                if stars in [1, 5]:
                    sents.append(sent)
                    labels.append(1 if stars in [5] else 0)
            if line_id % 97 == 0:
                print >> sys.stderr, "scanning file, line_id=%s\r" %(1 + line_id),
        print >> sys.stderr, "scanning file, line_id=%s" %(1 + line_id)
    return sents, labels

if __name__ == "__main__":
    x_train, y_train = load_data("output/review.merge.train")
    x_valid, y_valid = load_data("output/review.merge.valid")

    # create tf-idf model
    vectorizer = TfidfVectorizer(min_df=1)
    x_train = vectorizer.fit_transform(x_train)
    x_valid = vectorizer.transform(x_valid)
    joblib.dump(vectorizer, "model/tfidf.pkl")

    # feature selection
    filter = SelectKBest(chi2, k=200)
    x_train = filter.fit_transform(x_train, y_train)
    x_valid = filter.transform(x_valid)
    joblib.dump(filter, "model/chi2.pkl")

    # train logistic regression model
    lr_model = LogisticRegression()
    lr_model.fit_transform(x_train, y_train)
    joblib.dump(lr_model, "model/logisticregression.pkl")

    print "train accuracy:", lr_model.score(x_train, y_train)
    print "valid accuracy:", lr_model.score(x_valid, y_valid)
