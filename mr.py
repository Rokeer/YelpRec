#coding: utf8

from mrjob.job import MRJob
from mrjob.protocol import JSONValueProtocol
import heapq

TIPS_LIMIT    = 200
REVIEWS_LIMIT = 200

class MRProcess(MRJob):

    INPUT_PROTOCOL = JSONValueProtocol

    def mapper(self, _, data):
        if data['type'] == 'review':
            yield data['business_id'], ('review', (data['votes']['useful'], data['stars'], data['text']))
        elif data['type'] == 'tip':
            yield data['business_id'], ('tip', (data['likes'], data['text']))
        elif data['type'] == 'business':
            yield data['business_id'], ('business', (data['stars'], data['categories'], data['attributes']))

    def reducer(self, business_id, reviews_or_businesses):
        stars = categories = attributes = None
        reviews = []
        tips    = []

        for data_type, data in reviews_or_businesses:
            if data_type == 'review':
                votes, stars, text = data
                heapq.heappush(reviews, (int(votes), int(stars), text))
                if len(reviews) > REVIEWS_LIMIT:
                    heapq.heappop(reviews)
            elif data_type == 'tip':
                votes, text = data
                heapq.heappush(tips, (int(votes), text))
                if len(tips) > TIPS_LIMIT:
                    heapq.heappop(tips)
            else:
                stars, categories, attributes = data

        if not stars or not reviews:
            return

        sorted_tips = []
        while tips:
            sorted_tips.append(heapq.heappop(tips))
        sorted_tips.reverse()

        sorted_reviews = []
        while reviews:
            sorted_reviews.append(heapq.heappop(reviews))
        sorted_reviews.reverse()

        yield business_id, (stars, categories, attributes, sorted_reviews, sorted_tips)

if __name__ == "__main__":
    MRProcess().run()
