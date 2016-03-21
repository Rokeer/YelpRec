#!/bin/sh

set -x

# init env
test -d output || mkdir output
test -d model || mkdir model

# map-red the yelp data
test -f output/review.merge
if [ $? -ne 0 ]; then
    cat data/*.json | python mr.py > output/review.merge
    lines=`wc -l output/review.merge | awk '{print $1}'`
    if [ $? -ne 0 ]; then
        echo "execute mr.py error"
        exit -1
    fi

    ntrain=$((lines*9/10))
    nvalid=$(((lines-ntrain)/2))
    ntest=$((lines-ntrain-nvalid))
    head -$ntrain output/review.merge > output/review.merge.train
    tail -$((nvalid+ntest)) output/review.merge | head -$nvalid > output/review.merge.valid
    tail -$((nvalid+ntest)) output/review.merge | tail -$ntest > output/review.merge.test
fi

# train the doc2vec model from the corpus
# perplexity: train=322.469,valid=331.492, test=345.631
nohup python doc2vec.py output/review.merge.train output/review.merge.valid output/review.merge.test > train.log 2>&1 &
if [ $? -ne 0 ]; then
    echo "execute doc2vec.py error"
    exit -1
fi

exit 0
