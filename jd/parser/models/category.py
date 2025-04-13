from django.db import models
from django.utils.text import slugify
from pytils.translit import translify

# просто категория wb

class Category(models.Model):

    id = models.IntegerField(
        primary_key=True,
        unique=True,
        verbose_name="id"
    )

    name = models.CharField(
        max_length=50,
        verbose_name="название"
    )

    parent_category = models.ForeignKey(
        "self",
        related_name="parent_cat",
        on_delete=models.SET_NULL,
        default=None, 
        blank=True,
        null=True,
        verbose_name="родительская категорий"
    )

    query = models.CharField(
        max_length=1500, 
        verbose_name="cat=id"
    )

    shard = models.CharField(
        max_length=1500,
        verbose_name="shard"
    )

    slug = models.SlugField(
        max_length=100,
        db_index=True,
        verbose_name="слаг"
    )

    is_parsing = models.BooleanField(
        default=False,
        verbose_name="получено"
    )

    def __str__(self):
        return f"cat={self.id}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(translify(self.name))
        return super().save(*args, **kwargs)
    
    class Meta:
        verbose_name="категория"
        verbose_name_plural="категорий"
        ordering = ("id", )

