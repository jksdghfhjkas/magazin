
# SORT_FIELDS = {
#     "priceup" : "price_db__price",
#     "pricedown": "-price_db__price",
#     "rating": "rating_db__reviewRating",
#     "popular": "-rating_db__feedbacks",
#     "benefit": "-price_db__Sale"
# }

SORT_FIELDS = {
    "priceup": "price",
    "pricedown": "-price",
    "rating": "-reviewRating",
    "popular": "-feedbacks",
    "benefit": "-sale_price"
}


"""
это декоратор для функций get_queryset для представлений товаров
в нем реализована сортировка 
"""

def sort_mixin_decorator(func):
    def wrapper(self):

        product_set = func(self)

        sort = self.request.GET.get("sort")

        if sort and sort in SORT_FIELDS:
            return product_set.order_by(SORT_FIELDS[sort], "id")
        else:
            # базовая сортировка по рейтингу и колличеству отзывов
            return product_set.order_by(SORT_FIELDS["rating"], SORT_FIELDS["popular"], "id")
        
    return wrapper