from django.views.generic import DetailView
from parser.models import Product
from django.shortcuts import get_object_or_404  
from django.db.models import F

"""
страница представления товара
"""

class ProductView(DetailView):

    model = Product
    template_name="main/product_detail.html"
    context_object_name="data"

    def get_object(self, queryset=None):
        id = self.kwargs.get("id", None)
        return get_object_or_404(Product, id=id)


    


