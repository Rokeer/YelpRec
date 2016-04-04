#coding: utf8

from mrjob.job import MRJob
from mrjob.protocol import JSONValueProtocol

MIN_REVIEWS = 10

class MRProcess(MRJob):

    INPUT_PROTOCOL = JSONValueProtocol

    def mapper(self, _, data):
        if data['type'] == 'user':
            yield data['user_id'], ('user', (data['review_count'], data['average_stars'], data['votes']))
        elif data['type'] == 'review':
            yield data['user_id'], ('review', (data['stars'], data['votes'], data['text']))

    def reducer(self, user_id, reviews_or_users):
        review_count = None
        reviews = []

        for data_type, data in reviews_or_users:
            if data_type == 'user':
                review_count, average_stars, votes = data
            elif data_type == 'review':
                stars, votes, text = data
                reviews.append((stars, text))

        if not review_count:
            return
        if len(reviews) >= MIN_REVIEWS:
            yield user_id, (review_count, average_stars, votes, len(reviews), reviews)

if __name__ == "__main__":
    MRProcess().run()
