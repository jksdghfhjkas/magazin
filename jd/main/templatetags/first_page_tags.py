from django import template
from django.core.cache import cache
from parser.models import GlobalCategory

register = template.Library()



def push_redis_globalcategory():
    """
    функция для заполнения redis данными категорий
    """

    global_cat = GlobalCategory.objects.first().categories.all()
    cache.set("global_category", global_cat, timeout=None)


    context = [cat.parent_cat.all() for cat in global_cat]
    cache.set("category", context, timeout=None)

    return global_cat


@register.simple_tag()
def get_globalcategory():
    """
    тег для вывода меню глобальных категорий
    """
    if context := cache.get("global_category"):
        return context
    else:
        return push_redis_globalcategory()


@register.simple_tag()
def get_category(key):
    """
    тег для вывода меню категорий
    """
    return cache.get("category")[key]