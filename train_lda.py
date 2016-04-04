#coding: utf8

import os
import sys
import time
import math
import json
import nltk
import logging
from gensim.models.ldamodel import LdaModel
from gensim.corpora.dictionary import Dictionary

import pdb

def word_tokenize(lines):
    sents = []
    line_id = 0
    for line_id, line in enumerate(lines):
        review = json.loads(line.split("\t")[0])
        tokens = nltk.word_tokenize(" ".join(review.split("\n")))
        if len(tokens) >= 100 and len(tokens) <= 2000:
            sents.append(map(lower, tokens))

        if (line_id + 1) % 1000 == 0:
            logger.debug("scanning file, line_id=%s", 1 + line_id)
    logger.debug("scanning file, line_id=%s", 1 + line_id)
    return sents

def compute_perplexity(model, sents):
    scores = model.score(sents, len(sents))
    perplexity = 0
    for i, s in enumerate(sents):
        perplexity += math.exp(- 1.0 / len(s) * scores[i])
    return perplexity / len(sents)

def build_vocabulary(lines):
    sents = word_tokenize(lines)

    dictionary = Dictionary(sents)
    dictionary.filter_extremes(no_below=5, no_above=0.5, keep_n=100000)

    return dictionary

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print >> sys.stderr, "Usage: %s train_file validation_file test_file" %(sys.argv[0])
        exit(-1)

    # logging
    logger = logging.getLogger("YELP LDA")
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    ch = logging.StreamHandler()
    fh = logging.FileHandler("doc2vec.log")
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    logger.addHandler(ch)
    logger.addHandler(fh)

    # loading data
    logger.info("loading from %s...", sys.argv[1])
    with open(sys.argv[1], "r") as fp:

        # build vocab
        pdb.set_trace()
        dictionary = build_vocabulary(fp.readlines())
        dictionary.save_as_text('lda.dat', False)

        #sents_train = word_tokenize(fp.readlines())
    #sents_train0 = [ LabeledSentence(words=tokens, tags=["SENT_%d" % (i)]) for i, tokens in enumerate(sents_train) ]
    #logger.info("%s lines loaded", len(sents_train))

    #logger.info("loading from %s...", sys.argv[2])
    #with open(sys.argv[2], "r") as fp:
    #    sents_valid = word_tokenize(fp.readlines())
    #logger.info("%s lines loaded", len(sents_valid))

    #logger.info("loading from %s...", sys.argv[3])
    #with open(sys.argv[3], "r") as fp:
    #    sents_test = word_tokenize(fp.readlines())
    #logger.info("%s lines loaded", len(sents_test))

    ## train multiple models
    #for d in xrange(10, 210, 10):
    #    # initialize the model
    #    logger.info("building vocab...")
    #    model = Doc2Vec(size=d, window=8, min_count=2, workers=32, max_vocab_size=100000, alpha=0.025, min_alpha=0.00001)
    #    model.build_vocab(sents_train0)

    #    logger.info("training model...")
    #    model.train(sents_train0)

    #    # compute perplexity on validation and test set
    #    train_perplexity = compute_perplexity(model, sents_train)
    #    valid_perplexity = compute_perplexity(model, sents_valid)
    #    test_perplexity  = compute_perplexity(model, sents_test)

    #    logger.info("dim=%2d, train_perplexity=%.3lf,valid_perplexity=%.3lf, test_perplexity=%.3lf", \
    #        d, train_perplexity, valid_perplexity, test_perplexity)

    #    # saving doc2vec model
    #    logger.info("saving model...")
    #    model.save("model/d2v.dat.d%d" %(d))
    #    logger.info("saved")

    #logger.info("all done")

