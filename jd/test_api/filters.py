from django_filters import rest_framework as filters
from parser.models import Product



class CategoryFilter(filters.FilterSet):
    """
    фильтр товаров
    отбирает по слагам гобальных категорий и обычных
    черех параметры пути
    """
    class Meta:
        model = Product
        fields = ["id"]

    @property
    def qs(self):
        parent = super().qs

        request_kwargs = self.request.parser_context["kwargs"] if self.request else {}
        global_slug = request_kwargs.get("global_slug")
        cat_slug = request_kwargs.get("cat_slug")


        if global_slug:
            filters = {"category__parent_category__slug": global_slug}

            if cat_slug: 
                filters["category__slug"] = cat_slug
                
            return parent.select_related("category__parent_category")\
                .filter(**filters)
        
        return parent