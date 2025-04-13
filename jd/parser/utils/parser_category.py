import requests
from django.db import transaction
from parser.models import GlobalCategory, Category
from jd.celery import app
from django.utils.text import slugify
from pytils.translit import translify
# это парсер валдбериеса

URL_CATEGORIES = 'https://static-basket-01.wbbasket.ru/vol0/data/main-menu-ru-ru-v2.json'


# у нас api выдает данные в виде ступенек то есть 
# у категорий может быть поле chields в нем будут еще категорий


def parsing_chield_cat(chield_data: dict, parent_category: Category):
    # тут мы парсим категорий childs и запоняем WbCategory

    for cat in chield_data:
        if cat.get("query") and cat.get("shard"):
            with transaction.atomic():

                category, create = Category.objects.get_or_create(
                    id=cat["id"],
                    name=cat["name"],
                    query=cat["query"],
                    shard=cat["shard"],
                    slug=slugify(translify(cat["name"])),
                    parent_category=parent_category,
                    is_parsing=True
                )

                

            if childs := cat.get("childs"):
                parsing_chield_cat(childs, category)



@app.task()
def parsing_category():
    response = requests.get(URL_CATEGORIES)

    if response.status_code == 200:

        global_category = GlobalCategory.objects.first()

        for cat in response.json():
            if cat.get("query") and cat.get("shard"):
                with transaction.atomic():

                    category, create = Category.objects.get_or_create(
                        id=cat["id"],
                        name=cat["name"],
                        query=cat["query"],
                        shard=cat["shard"],
                        slug=slugify(translify(cat["name"])),
                        is_parsing=True
                    )

                    global_category.categories.add(category)

                    if childs := cat.get("childs"):
                        parsing_chield_cat(childs, category)





    




    



