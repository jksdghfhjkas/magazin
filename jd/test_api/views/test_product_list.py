from django.shortcuts import render

def test_product_view(request, global_slug=None, cat_slug=None):
    return render(request, "test_api/test.html")