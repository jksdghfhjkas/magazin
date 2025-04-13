from django.urls import path
from test_api.views import ProductAPIview, test_product_view, basket_add_view

"""
api/v1/
"""

urlpatterns = [
    path("products/", ProductAPIview.as_view()),
    path("products/<slug:global_slug>/", ProductAPIview.as_view()),
    path("products/<slug:global_slug>/<slug:cat_slug>/", ProductAPIview.as_view(), name="api_product_list"),
    path("basket/", basket_add_view),


    path("", test_product_view, name="product_api"),
    path("<slug:global_slug>/", test_product_view, name="product_api"),
    path("<slug:global_slug>/<slug:cat_slug>/", test_product_view, name="product_api")
    
]