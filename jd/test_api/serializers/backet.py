from rest_framework import serializers


class BasketSerializer(serializers.Serializer):
    """
    серилизватор для корзины пользователя
    """
    product_id = serializers.IntegerField()

    



