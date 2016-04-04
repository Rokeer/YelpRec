#coding: utf8

from mrjob.job import MRJob
from mrjob.protocol import JSONValueProtocol
from mrjob.protocol import TextValueProtocol
import heapq

REVIEWS_LIMIT = 100

class MRProcess(MRJob):

    INPUT_PROTOCOL = JSONValueProtocol

    def mapper(self, _, data):
        if data['type'] == 'review':
            if data['votes']['useful'] > 1:
                yield data['business_id'], ('review', (data['stars'], data['text']))
        elif data['type'] == 'business':
            yield data['business_id'], ('business', data['categories'])

    def reducer(self, business_id, reviews_or_businesses):
        categories = []
        reviews = []
        for data_type, data in reviews_or_businesses:
            if data_type == 'review':
                reviews.append(data)
            else:
                categories = data

        for cat in categories:
            for stars, text in reviews:
                yield text, (stars, cat)

if __name__ == "__main__":
    MRProcess().run()
