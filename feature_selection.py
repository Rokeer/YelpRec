#coding: utf8

import os
import sys
import json
import heapq
import pickle
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
import pdb

DIM = 20000

def feature_selection(fp):
    sents = []
    labels = [[], []]

    """ build the corpus from the file. """
    for line_id, line in enumerate(fp):
        items = json.loads(line.split("\t")[1])
        stars, categories, attributes, reviews, tips = items

        if categories:
            category = categories[random.randint(0, len(categories) - 1)]
            for review_id, (votes, stars, review) in enumerate(reviews):
                sent = " ".join(review.split("\n"))
                sents.append(sent)
                labels[0].append(stars)
                labels[1].append(category)
        if line_id % 97 == 0:
            print >> sys.stderr, "scanning file, line_id=%s\r" %(1 + line_id),
    print >> sys.stderr, "scanning file, line_id=%s" %(1 + line_id)

    """ extract text feature from the corpus. """
    vectorizer = TfidfVectorizer(min_df=1, stop_words="english")
    X = vectorizer.fit_transform(sents)

    """ feature selection, """
    """ I did not use SelectKBest because I want to know the chi2 value for each feature. """
    # model1 = SelectKBest(chi2, k=DIM)
    # model1.fit(X, labels[0])
    # print model1.get_support(True)

    # model2 = SelectKBest(chi2, k=DIM)
    # model2.fit(X, labels[1])
    # print model2.get_support(True)

    sorted_ids = [[], []]
    for i in xrange(2):
        ids = []
        chi2_val = chi2(X, labels[i])[0]
        for id, v in enumerate(chi2_val.tolist()):
            heapq.heappush(ids, (v, id))
            if len(ids) > DIM:
                heapq.heappop(ids)
        while ids:
            sorted_ids[i].append(heapq.heappop(ids))
        sorted_ids[i].reverse()

    """ save the features. """
    names = vectorizer.get_feature_names()
    with open("model/feature.pkl", "w") as fp:
        for i in xrange(2):
            names_fin = [names[id] for v, id in sorted_ids[i]]
            pickle.dump(names_fin, fp)

if __name__ == "__main__":
    print >> sys.stderr, "loading from STDIN..."
    with open("output/review.merge.train", "r") as fp:
        feature_selection(fp)
