#!/bin/sh

set -x

# init env
test -d marker || mkdir marker
test -d output || mkdir output
test -d model || mkdir model

datasets=(train valid test)

####################################################################################################
# preprocess the yelp data set, transform to self-defined format.
####################################################################################################

# map-red the yelp data

echo "running map-reduce for the yelp review..."
test -f marker/mr_review.mk
if [ $? -ne 0 ]; then
    cat data/*.json | python src/mr_review.py > output/review.dat
    if [ $? -ne 0 ]; then
        echo "execute mr_review.py error"
        exit -1
    fi

    lines=`wc -l output/review.dat | awk '{print $1}'`

    ntrain=$((lines*9/10))
    nvalid=$(((lines-ntrain)/2))
    ntest=$((lines-ntrain-nvalid))

    head -$ntrain output/review.dat > output/review.train
    tail -$((nvalid+ntest)) output/review.dat | head -$nvalid > output/review.valid
    tail -$((nvalid+ntest)) output/review.dat | tail -$ntest > output/review.test

    touch marker/mr_review.mk
fi
echo "done"

echo "running map-reduce for the yelp user..."
test -f marker/mr_user.mk
if [ $? -ne 0 ]; then
    cat data/*.json | python src/mr_user.py > output/user.dat
    if [ $? -ne 0 ]; then
        echo "execute mr_user.py error"
        exit -1
    fi
    touch marker/mr_user.mk
fi
echo "done"

echo "running map-reduce for the yelp business..."
test -f marker/mr_business.mk
if [ $? -ne 0 ]; then
    cat data/*.json | python src/mr_business.py > output/business.dat
    if [ $? -ne 0 ]; then
        echo "execute mr_business.py error"
        exit -1
    fi
    touch marker/mr_business.mk
fi
echo "done"

echo "partitioning the dataset..."
test -f marker/partition.mk
if [ $? -ne 0 ]; then
    python src/partition.py output/user.dat output/rating.train output/rating.test
    if [ $? -ne 0 ]; then
        echo "execute partition.py error"
        exit -1
    fi
    touch marker/partition.mk
fi
echo "done"

####################################################################################################
# infer business and user lda vector
####################################################################################################
if [ ! -f "marker/infer_business.mk" ]; then
    python src/infer_business.py "output/business.lda"
    if [ $? -ne 0 ]; then
        echo "execute infer_business.py error"
        exit -1
    fi
    touch marker/infer_business.mk
fi

if [ ! -f "marker/infer_user.mk" ]; then
    python src/infer_user.py "output/user.lda"
    if [ $? -ne 0 ]; then
        echo "execute infer_user.py error"
        exit -1
    fi
    touch marker/infer_user.mk
fi


######################################################################################################
### train the cf model
######################################################################################################
#test -f marker/pre_compute.mk
#if [ $? -ne 0 ]; then
#    for ((i=0;i<10;++i)); do
#        nohup python src/pre_compute.py "$i" &
#        if [ $? -ne 0 ]; then
#            echo "execute pre_compute.py error"
#            exit -1
#        fi
#    done
#    wait
#    touch marker/pre_compute.mk
#fi
#echo "done"



exit 0
