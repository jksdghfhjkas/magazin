from rest_framework.generics import ListAPIView
from parser.models import Product
from test_api.serializers import ProductSerializer
from rest_framework.pagination import CursorPagination
from django_filters import rest_framework as filters
from test_api.filters import CategoryFilter
from main.utils import SORT_FIELDS


"""
шаблон для представления продуктов
"""
SORT_FIELDS = {
    "priceup": "price",
    "pricedown": "-price",
    "rating": "-reviewRating",
    "popular": "-feedbacks",
    "benefit": "-sale_price"
}



class CustomCursorPagination(CursorPagination):
    page_size = 20
    ordering = (SORT_FIELDS["rating"], SORT_FIELDS["popular"], "id")

    def get_ordering(self, request, queryset, view):
        """
        Определяем сортировку на основе параметров запроса.
        """
        sort = request.GET.get("sort", None)
        
        if sort and sort in SORT_FIELDS:
            return (SORT_FIELDS[sort], "id")
        else:
            return self.ordering




class ProductAPIview(ListAPIView):
    queryset = Product.objects.all().order_by("id")
    serializer_class = ProductSerializer
    pagination_class = CustomCursorPagination
    http_method_names = ['get']
    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = CategoryFilter

