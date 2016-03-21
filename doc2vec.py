#coding: utf8

import os
import sys
import time
import math
import json
import nltk
from gensim.models.doc2vec import Doc2Vec
from gensim.models.doc2vec import LabeledSentence

def word_tokenize(fp):
    sents = []
    for line_id, line in enumerate(fp.readlines()):
        reviews = json.loads(line.split("\t")[1])[3]
        for review_id, (votes, stars, review) in enumerate(reviews):
            sent = " ".join(review.split("\n"))
            tokens = nltk.word_tokenize(sent)
            if len(tokens) >= 100 and len(tokens) <= 1000:
                sents.append(tokens)
        if line_id % 97 == 0:
            print >> sys.stderr, "scanning file, line_id=%s\r" %(1 + line_id),
    print >> sys.stderr, "scanning file, line_id=%s" %(1 + line_id)
    return sents

def compute_perplexity(model, sents):
    scores = model.score(sents, len(sents))
    perplexity = 0
    for i, s in enumerate(sents):
        perplexity += math.exp(- 1.0 / len(s) * scores[i])
    return perplexity / len(sents)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print >> sys.stderr, "Usage: %s train_file validation_file test_file" %(sys.argv[0])
        exit(-1)

    # loading data
    print >> sys.stderr, "loading from %s..." %(sys.argv[1])
    with open(sys.argv[1], "r") as fp:
        sents_train = word_tokenize(fp)
    sents_train0 = [ LabeledSentence(words=tokens, tags=["SENT_%d" % (i)]) for i, tokens in enumerate(sents_train) ]

    print >> sys.stderr, "loading from %s..." %(sys.argv[2])
    with open(sys.argv[2], "r") as fp:
        sents_valid = word_tokenize(fp)

    print >> sys.stderr, "loading from %s..." %(sys.argv[3])
    with open(sys.argv[3], "r") as fp:
        sents_test = word_tokenize(fp)

    # initialize the model
    continue_train = False

    if continue_train:
        model = Doc2Vec.load("model/doc2vec.dat")
    else:
        print >> sys.stderr, "building vocab..."
        model = Doc2Vec(size=200, window=8, min_count=2, workers=32, max_vocab_size=100000, alpha=0.025, min_alpha=0.00001)
        model.build_vocab(sents_train0)

    print >> sys.stderr, "training model..."
    model.train(sents_train0)

    # compute perplexity on validation and test set
    train_perplexity = compute_perplexity(model, sents_train)
    valid_perplexity = compute_perplexity(model, sents_valid)
    test_perplexity  = compute_perplexity(model, sents_test)

    print >> sys.stderr, "validation, train_perplexity=%.3lf,valid_perplexity=%.3lf, test_perplexity=%.3lf" \
        %(train_perplexity, valid_perplexity, test_perplexity)

    # saving doc2vec model
    print >> sys.stderr, "saving model..."
    model.save("model/doc2vec.dat")

    print "all done"
