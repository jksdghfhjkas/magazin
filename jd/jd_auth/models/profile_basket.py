from django.db import models
from parser.models import Product


class Basket(models.Model):
    """
    модель корзины пользователя
    """
    user = models.OneToOneField(
        "User",
        on_delete=models.CASCADE
    )
    products = models.ManyToManyField(
        Product,
        blank=True,
        verbose_name="товары пользователя"
    )



        