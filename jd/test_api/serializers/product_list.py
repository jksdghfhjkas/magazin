from rest_framework import serializers
from parser.models import Product



class ProductSerializer(serializers.ModelSerializer):

    """
    серилизатор модели Product

    через manager модели (путь parser/managers/ProductManager) подгружаются поля 
    price, reviewRating, feedbacks, sale, sale_price
    """

    price = serializers.IntegerField()
    reviewRating = serializers.DecimalField(
        max_digits=20,
        decimal_places=2,
    )
    feedbacks = serializers.IntegerField()
    sale = serializers.IntegerField()
    sale_price = serializers.IntegerField()


    class Meta:
        model = Product
        fields = ["id", "UrlsImages", "name", "price", "reviewRating", "feedbacks", "sale", "sale_price"]