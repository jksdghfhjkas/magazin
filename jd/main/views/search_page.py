from django.views.generic import ListView
from parser.models import Product
from main.utils import sort_mixin_decorator # декоратор фильтров
from django.db.models import Q
from django.http import Http404

from functools import reduce
import operator

"""
страница товаров поисковой строки
"""

class SearchView(ListView):

    model = Product
    template_name="main/first_page.html"
    context_object_name="products"
    paginate_by=500

    @sort_mixin_decorator
    def get_queryset(self):

        product_set = Product.objects.all()

        search = self.request.GET.get("search")
        
        if search:

            # создаем список с Q параметрами, дальше их комбинируем через reduce и передаем в filter
            search_list_Q = [Q(name__icontains=term) for term in search.split()]
            combined_search = reduce(operator.and_, search_list_Q)
            product_set = product_set.filter(combined_search)

            if not product_set.exists():
                raise Http404("Товары не найдены.")
            
        return product_set
    

