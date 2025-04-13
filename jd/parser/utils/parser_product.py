import requests
from django.db import transaction
from parser.models import (Category,
                         Product, 
                         PriceProduct, 
                         StockWarehouses,
                         reviewRatingProduct)

from parser.utils import get_info_supplier, get_info_sku, url_images
from jd.celery import app


import logging
logger = logging.getLogger('django')


def parsing_position(data: dict, category: Category):
        for position in data:

            id = position.get('id')
            name = position.get('name')
            supplierId = position.get('supplierId')
            pics = position.get("pics")
            reviewRating = position.get('reviewRating')
            totalQuantity = position.get('totalQuantity')
            feedbacks = position.get('feedbacks')
            info_product = get_info_sku(id)

            try:
                with transaction.atomic():
                    obj_product = Product.objects.select_for_update(nowait=True).filter(id=id)

                    if not obj_product.exists():

                        urls_images = url_images(id, pics)
                        obj_supplier = get_info_supplier(supplierId)


                        obj_product = Product.objects.create(
                            id=id,
                            name=name,
                            UrlsImages=urls_images,
                            supplier=obj_supplier,
                            category=category
                        )

                    else:
                        obj_product = obj_product.first()


                PriceProduct.objects.update_or_create(
                    product=obj_product,
                    price=info_product.get("price"),
                    PriceSale=info_product.get("sale_price"),
                    Sale=info_product.get("sale")
                )

                StockWarehouses.objects.update_or_create(
                    product=obj_product,
                    stocks=info_product.get("data_stock"),
                    total_quality=totalQuantity
                )

                reviewRatingProduct.objects.update_or_create(
                    product=obj_product,
                    reviewRating=reviewRating,
                    feedbacks=feedbacks
                )

            except Exception as e: 
                logger.error(f"{e}", exc_info=True)
                

                 

@app.task()
def parsing_position_pages(shard: str, query: str, name: str, categoryId: int):

    page = 1
    category = Category.objects.get(id=categoryId)

    while True:
        url = f'https://catalog.wb.ru/catalog/{shard}/v2/catalog?appType=32&{query}&curr=rub&dest=-4734875&page={page}'
        response = requests.get(url)

        if response.status_code == 200:
            parsing_position(response.json().get("data").get("products"), category)
        else:
            return f"категория {name} отмониторена"

        page += 1



@app.task()
def parsing():
    categories = Category.objects.all()

    for cat in categories:
        parsing_position_pages.delay(
            shard=cat.shard,
            query=cat.query,
            name=cat.name,
            categoryId=cat.id
        )



