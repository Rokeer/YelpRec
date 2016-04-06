#coding: utf8

import numpy as np
from mrjob.job import MRJob
from mrjob.protocol import JSONValueProtocol

MIN_REVIEWS = 10

np.random.seed(477)

class MRProcess(MRJob):

    INPUT_PROTOCOL = JSONValueProtocol

    def mapper(self, _, data):
        if data['type'] == 'user':
            yield data['user_id'], ('user', (data['review_count'], data['average_stars'], data['votes']))
        elif data['type'] == 'review':
            yield data['user_id'], ('review', (data['business_id'], data['stars'], data['votes'], data['text']))

    def reducer(self, user_id, reviews_or_users):
        review_count = None
        reviews = []

        sum_rating = 0
        num_rating = 0

        for data_type, data in reviews_or_users:
            if data_type == 'user':
                review_count, average_stars, votes = data
            elif data_type == 'review':
                business_id, stars, votes, text = data

                sum_rating += stars
                num_rating += 1

                reviews.append((business_id, stars, text))

        if not review_count:
            return
        if len(reviews) >= MIN_REVIEWS:
            np.random.shuffle(reviews)
            mid = 9 * len(reviews) / 10
            ratings = 1.0 * sum_rating / num_rating if num_rating else 0
            yield user_id, (review_count, average_stars, ratings, votes, reviews[:mid], reviews[mid:])

if __name__ == "__main__":
    MRProcess().run()
