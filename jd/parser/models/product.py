from django.db import models
from django.contrib.postgres.fields import ArrayField
from parser.managers import ProductManager


class Product(models.Model):
    """Модель продукта"""

    id = models.IntegerField(
        primary_key=True,
        verbose_name="id"
    )
    name = models.CharField(
        max_length=350,
        verbose_name="Название"
    )
    supplier = models.ForeignKey(
        "Supplier",
        null=True,
        on_delete=models.CASCADE,
        verbose_name="поставщик"
    )
    UrlsImages = ArrayField(
        models.CharField(max_length=250),
        null=True,
        verbose_name="пути изображений"
    )
    category = models.ForeignKey(
        "Category",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="категория"
    )

    objects = ProductManager()
    
    class Meta:
        verbose_name="продукт"
        verbose_name_plural="продукты"
        ordering = ("id", )



class PriceProduct(models.Model):
    """Модель цены продукта"""

    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        related_name="price_db",
        verbose_name="продукт"
    )
    price = models.IntegerField(
        verbose_name="цена"
    )
    PriceSale = models.IntegerField(
        verbose_name="скидочная цена"
    )
    Sale = models.IntegerField(
        verbose_name="скидка"
    )

    def __str__(self):
        return f"price {self.product.name}"
    


class StockWarehouses(models.Model):
    """Модель колличества товаров

    'stocks': [
            {
                'name': 'Казань WB(char)',
                'qty': '1003(int)'
            }
        ]

    """

    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        verbose_name="продукт"
    )
    stocks = models.JSONField(
        verbose_name="тован на складе"
    )
    total_quality = models.IntegerField(
        verbose_name="общее колличество"
    )

    def __str__(self):
        return f"stock {self.product.name}"
    


class reviewRatingProduct(models.Model):
    """Модель рейтинга"""
    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        related_name="rating_db",
        verbose_name="продукт"
    )
    reviewRating = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0.0,
        verbose_name="рейтинг"
    )
    feedbacks = models.IntegerField(
        verbose_name="отзывы",
        default=0
    )
    def __str__(self):
        return f"rating {self.product.name}"
