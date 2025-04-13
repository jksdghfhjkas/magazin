from django.db import models
from django.db.models import F

"""
manager модели продуктов
"""

class ProductManager(models.Manager):
    def get_queryset(self):
        """
        добавляем поля из связанных моделей
        """
        return super().get_queryset().annotate(
            price=F("price_db__price"),
            reviewRating=F("rating_db__reviewRating"),
            feedbacks=F("rating_db__feedbacks"),
            sale=F("price_db__Sale"),
            sale_price=F("price_db__PriceSale")
        )
    
