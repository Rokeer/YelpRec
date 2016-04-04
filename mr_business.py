#coding: utf8

from mrjob.job import MRJob
from mrjob.protocol import JSONValueProtocol
import heapq

REVIEWS_LIMIT = 40

class MRProcess(MRJob):

    INPUT_PROTOCOL = JSONValueProtocol

    def mapper(self, _, data):
        if data['type'] == 'business':
            yield data['business_id'], ('business', (data['stars'], data['review_count'], data['categories']))
        elif data['type'] == 'review':
            yield data['business_id'], ('review', (data['stars'], data['votes']['useful'], data['text']))

    def reducer(self, business_id, reviews_or_businesses):
        stars = None
        pos_reviews = []
        neg_reviews = []

        for data_type, data in reviews_or_businesses:
            if data_type == 'business':
                stars, review_count, categories = data
            elif data_type == 'review':
                stars, votes, text = data
                if stars >= 3:
                    heapq.heappush(pos_reviews, (int(votes), text))
                    if len(pos_reviews) > REVIEWS_LIMIT: 
                        heapq.heappop(pos_reviews)
                else:
                    heapq.heappush(neg_reviews, ((int(votes), text)))
                    if len(neg_reviews) > REVIEWS_LIMIT: 
                        heapq.heappop(neg_reviews)

        if not stars:
            return

        sorted_pos_reviews = []
        sorted_neg_reviews = []
        while pos_reviews:
            sorted_pos_reviews.append(heapq.heappop(pos_reviews))
        sorted_pos_reviews.reverse()
        while neg_reviews:
            sorted_neg_reviews.append(heapq.heappop(neg_reviews))
        sorted_neg_reviews.reverse()

        yield business_id, (stars, review_count, categories, sorted_pos_reviews, sorted_neg_reviews)

if __name__ == "__main__":
    MRProcess().run()
