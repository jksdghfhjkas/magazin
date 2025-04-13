from django.views.generic import ListView
from parser.models import Product
from django.db.models import F, Q
from django.http import Http404
from main.utils import sort_mixin_decorator # декоратор фильтров
from functools import reduce
import operator


"""
страница с таварами
"""


class Main(ListView):

    model=Product
    template_name="main/first_page.html"
    context_object_name="products"
    paginate_by = 500


    @sort_mixin_decorator
    def get_queryset(self):

        product_set = Product.objects.order_by("id")
        
        # получаем слаг категорий
        global_slug = self.kwargs.get("global_slug")
        cat_slug = self.kwargs.get("cat_slug")

        
        if global_slug:
            # фильтруем по категорий
            # подгружаем category__parent_category чтобы уменьшить колличество запросов (N + 1)

            filters = {"category__parent_category__slug": global_slug}

            if cat_slug: 
                filters["category__slug"] = cat_slug
                
            product_set = product_set.select_related("category__parent_category")\
                .filter(**filters)
        
            if not product_set.exists():
                raise Http404("Категорий не найдены.")
            
        
        # поиск товаров
        if search := self.request.GET.get("search"):

            # создаем список с Q параметрами, дальше их комбинируем через reduce и передаем в filter
            search_list_Q = [Q(name__icontains=term) for term in search.split()]
            combined_search = reduce(operator.and_, search_list_Q)
            product_set = product_set.filter(combined_search)

            if not product_set.exists():
                raise Http404("Товары не найдены.")
            

        return product_set
    

            


        
    







    
        
        

