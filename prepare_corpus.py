#coding: utf8

import os
import sys
import math
import time
import json
import random
import pickle
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from sklearn.externals import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pdb

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
            flags.append((True, (score, p[i][1])))
        else:
            flags.append((False, (score, p[i][1])))
    return flags

def prepare_corpus(fp):
    for line_id, line in enumerate(fp):
        business_id, items = line.split("\t")[0], json.loads(line.split("\t")[1])
        stars, categories, attributes, reviews, tips = items
        for votes, stars, review in reviews[:10]:
            try:
                """ sentence boundary check. """
                review = " ".join(review.split("\n"))
                sentences = sent_tokenize(review)

                """ check sentences. """
                flags = check_sentences(sentences)
                ids = [id for id, flag in enumerate(flags) if flag[0] == True]
                if ids:
                    print "%s\t%s" % (sentences[ids[random.randint(0, len(ids) - 1)]], review)

            except Exception as ex:
                pass
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


    prepare_corpus(sys.stdin)
