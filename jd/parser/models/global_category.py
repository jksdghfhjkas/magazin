from django.db import models
from .category import Category

# глобальная категория wb

class GlobalCategory(models.Model):

    categories = models.ManyToManyField(
        Category, 
        blank=True,
        null=True,
    )

    def __str__(self):
        return 'global category'
