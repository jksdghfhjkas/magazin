
import requests

def url_images(id: str, pics: int):
    id = str(id)
    """
        id - артикул товара
        pict - колличество изображений товара

        тут мы получаем ссылки на изображения товаров путем простого перебебора серверов 

        id серверов вб: 10 - 18 и 01 - 09; пример ->
        https://basket-04.wbbasket.ru/vol482/part48282/48282096/images/big/1.webp
        https://basket-14.wbbasket.ru/vol2177/part217794/217794970/images/big/1.webp

        ссылка строиться из кусочков артикула товара

        vol(тут артикул без 5 символов)
        part(тут артикул без 3 символов)

    """


    url = "https://basket-{}.wbbasket.ru/"
    servers = list(range(10, 19)) + [f"0{i}" for i in range(1, 10)]

    url_two = f"vol{id[:len(id) - 5]}/part{id[:len(id) - 3]}/{id}/images/big/"

    for server in servers:
        try:
            response = requests.get(url.format(server) + url_two + "1.webp")
            if response.status_code == 200:
                return [url.format(server) + url_two + f"{image}.webp" for image in range(1, pics + 1)]
        except:
            pass

    else: 
        return [id]
    
    
