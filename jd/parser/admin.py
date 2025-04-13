from django.contrib import admin
from parser.models import (
    GlobalCategory,
    Category,
    Product,
    PriceProduct,
    reviewRatingProduct,
    Supplier
)

class GlobalCategoryAdmin(admin.ModelAdmin):
    filter_horizontal = ["categories"]

admin.site.register(GlobalCategory, GlobalCategoryAdmin)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Supplier)
admin.site.register(PriceProduct)
admin.site.register(reviewRatingProduct)

# Register your models here.
