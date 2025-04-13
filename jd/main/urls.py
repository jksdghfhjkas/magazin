from django.urls import path
from .views import Main, ProductView, SearchView

urlpatterns = [
    path("", Main.as_view(), name="product-search"),
    path("<int:id>/", ProductView.as_view(), name="product-detail"),
    path("<slug:global_slug>/", Main.as_view(), name="product-category"),
    path("<slug:global_slug>/<slug:cat_slug>/", Main.as_view(), name="product-category"),
]

