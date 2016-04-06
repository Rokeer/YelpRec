output data format:
1. business.dat
    line -> business_id, (stars, review_count, categories, sorted_pos_reviews, sorted_neg_reviews)
2. user.dat
    line -> user_id, (review_count, average_stars, votes, reviews_train, reviews_test)
    review->(business_id, stars, text)
3. review.dat, review.train, review.valid, review.test
    line -> text, (stars, cat)
