

from parser.models import reviewRatingProduct, Product

query_set = Product.objects.all()

for obj in query_set:
    if not hasattr(obj, "rating_db"):
        rating = reviewRatingProduct.objects.create(
            product=obj,
        )
        rating.save()

        print("нет райтинга!")


    


# query_set = reviewRatingProduct.objects.filter(reviewRating = None)

# for i in query_set:
#     i.reviewRating = 0.0
#     i.save()

# query_set = reviewRatingProduct.objects.filter(feedbacks = None)

# for i in query_set:
#     i.feedbacks = 0
#     i.save()