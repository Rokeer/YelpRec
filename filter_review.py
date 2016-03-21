#coding: utf8

import os
import sys
import math
import time
import json
import pickle
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from sklearn.externals import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pdb

ccbegin="\033[0;31m"
ccend="\033[0m"

def check_sentences(sentences):
    x = vectorizer.transform(sentences)
    x = filter.transform(x)
    p = lr_model.predict_proba(x) # tuple of <p(y=0|x), p(y=1|x)>

    flags = []
    for i, sentence in enumerate(sentences):

        """ feature selection strategy. """
        ws = word_tokenize(sentence)
        ws1 = [w for w in ws if w in fwords1]
        ws2 = [w for w in ws if w in fwords2]
        score = min(len(ws1), len(ws2))

        if len(ws) < 16 and score >= 2 and (p[i][0] > 0.8 or p[i][1] > 0.8):
            flags.append((True, score, p[i][1]))
        else:
            flags.append((False, score, p[i][1]))
    return flags

def filter_review(filename):
    with open(filename, "r") as fp:
        for line_id, line in enumerate(fp):
            business_id, items = line.split("\t")[0], json.loads(line.split("\t")[1])
            stars, categories, attributes, reviews, tips = items
            for votes, stars, review in reviews[:20]:
                try:
                    """ sentence boundary check. """
                    review = " ".join(review.split("\n"))
                    sentences = sent_tokenize(review)

                    """ check sentences. """
                    print 
                    print "################################"
                    flags = check_sentences(sentences)
                    for i, sentence in enumerate(sentences):
                        flag, score, proba = flags[i]
                        if flag:
                            print ccbegin, sentence, ccend,
                        else:
                            print sentence,
                        print "(%s, %.2lf)" %(score, proba),
                    print 
                    raw_input()

                except Exception as ex:
                    print ex
            if line_id % 97 == 0:
                print >> sys.stderr, "scanning file, line_id=%s\r" %(1 + line_id),
        print >> sys.stderr, "scanning file, line_id=%s" %(1 + line_id)

if __name__ == "__main__":
    print >> sys.stderr, "loading from STDIN..."

    with open("model/feature.pkl", "r") as fp:
        fwords1 = set(pickle.load(fp)[:100])
        fwords2 = set(pickle.load(fp)[:10000])

    vectorizer = joblib.load("model/tfidf.pkl")
    filter = joblib.load("model/chi2.pkl")
    lr_model = joblib.load("model/logisticregression.pkl")

    filter_review("output/review.merge.valid")
