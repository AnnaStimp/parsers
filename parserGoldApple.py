import psycopg2
import requests
import json
import time

from model import host, user, password, db_name, insert_product, insert_price_list

# указание категорий товаров для базы данных и запросов
categoryId = {
    'makeup': {'req': 3, 'db': 2},
    'care': {'req': 4, 'db': 1},
    'pharmacy': {'req': 3747, 'db': 3},
    'hair': {'req': 6, 'db': 4},
    'asia': {'req': 10, 'db': 5},
    'organic': {'req': 12, 'db': 6},
    'perfumer': {'req': 7, 'db': 7}
}

id_store = 1

HEADERS = {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Mobile Safari/537.36',
           'accept': '*/*'}

# подключение к базе данных
def get_db():
    db = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    return db

db = get_db()

for category in categoryId:
    page = 1
    cat = categoryId[category]['req']

    # выполнение запроса к магазину
    url = 'https://goldapple.ru/web_scripts/discover/category/products?cat={}&page={}'.format(cat, page)
    r = requests.get(url, headers=HEADERS)
    result_of_req = json.loads(r.text)

    count = 0
    while count != 1:
    # while 'products' in result_of_req.keys():
        products = result_of_req['products']

        for i in products:
            # получение необходимых данных из запроса и отправка в базу данных
            with  db.cursor() as cursor:
                name = '{} {}'.format(str(i['brand']).upper().replace(r"'", ""), str(i['name']).lower().replace(r"'", ""))
                response = insert_product(cursor, name, i['category_type'], i['image_url'], (i['volume'] or 0), categoryId[category]['db'])
                db.commit()

                if response[0][0]:
                    response = insert_price_list(cursor, response[0][0], id_store, i['url'], i['price'])
                    db.commit()
        
        page+=1
        count+=1
        time.sleep(5)
        url = 'https://goldapple.ru/web_scripts/discover/category/products?cat={}&page={}'.format(cat, page)
        r = requests.get(url, headers=HEADERS)
        result_of_req = json.loads(r.text)

print('end pars GoldApple')