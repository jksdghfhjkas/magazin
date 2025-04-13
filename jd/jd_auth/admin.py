from django.contrib import admin
from jd_auth.models import User, Profile, Basket

admin.site.register(User)
admin.site.register(Profile)

class BasketAdmin(admin.ModelAdmin):
    filter_horizontal = ("products", )

admin.site.register(Basket, BasketAdmin)


