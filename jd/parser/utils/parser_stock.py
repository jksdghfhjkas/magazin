import requests

url_all_stocks = 'https://static-basket-01.wbbasket.ru/vol0/data/stores-data.json'
response_all_stocks = requests.get(url_all_stocks)
all_stocks = response_all_stocks.json()


def get_info_sku(sku):
    global all_stocks

    url = f'https://card.wb.ru/cards/detail?appType=32&curr=rub&dest=-4734875&nm={sku}'
    respose = requests.get(url).json().get('data').get('products')[0]
    sizes = respose.get('sizes')

    price = respose.get('priceU') // 100
    sale_price = respose.get('salePriceU') // 100
    sale = respose.get('sale')
    
    if price == sale_price:
        sale_price = 0

    data_stocks = {}
    for size in sizes:
        for stock in size.get('stocks'):
            wh = stock.get('wh')
            qty = stock.get('qty')

            name = ''
            for st in all_stocks:
                if st.get('id') == wh:
                    name = st.get('name')


            if str(wh) not in data_stocks:
                data_stocks[str(wh)] = {
                    'qty': qty,
                    'name': name
                }
            else:
                data_stocks[str(wh)]['qty'] += qty

    data = []
    for st in data_stocks.items():
        data.append(st[1])

    return {
        'price': price,
        'sale_price': sale_price,
        'sale': sale,
        'data_stock': data
    }