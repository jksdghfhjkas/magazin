
import requests
from parser.models import Supplier, reviewRatingSupplier
from django.db import transaction

def get_info_supplier(supplierId):
    headers = {
        'accept': '*/*',
        'accept-language': 'ru,en-GB;q=0.9,en;q=0.8',
        'origin': 'https://www.wildberries.ru',
        'priority': 'u=1, i',
        'referer': f'https://www.wildberries.ru/seller/{supplierId}',
        'sec-ch-ua': '"Chromium";v="124", "Opera";v="110", "Not-A.Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 OPR/110.0.0.0',
        'x-client-name': 'site',
    }

    with transaction.atomic():

        try:
            supplier = Supplier.objects.select_for_update().filter(id=supplierId)

            if not supplier.exists():

                response = requests.get(f'https://suppliers-shipment-2.wildberries.ru/api/v1/suppliers/{supplierId}', headers=headers).json()

                url_date = f'https://static-basket-01.wbbasket.ru/vol0/data/supplier-by-id/{supplierId}.json'
                res = requests.get(url_date, headers=headers)
                if res.status_code == 404:
                    return 
                response_date = res.json()

                supplier = Supplier.objects.create(
                    id = supplierId,
                    name = response_date.get("supplierName"),
                    FullName = response_date.get("supplierFullName"),
                    inn = response_date.get("inn"),
                    ogrn = response_date.get("ogrn"),
                    address = response_date.get("legalAddress"),
                    trademark = response_date.get("trademark"),
                    kpp = response_date.get("kpp"),
                    registrationDate = response.get("registrationDate")
                )

                reviewRatingSupplier.objects.create(
                    supplier=supplier,
                    ProgramLevel=response.get("supplierLoyaltyProgramLevel"),
                    data={
                        "feedbacksCount": response.get("feedbacksCount", 0),
                        "saleItemQuantity": response.get("saleItemQuantity", 0),
                        "suppRatio": response.get("suppRatio", 0.0),
                        "valuation": response.get("valuation", 0.0)
                })
                
            else:
                return supplier.first()
        
        except: 
            return Supplier.objects.get(id=supplierId)



    