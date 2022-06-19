import psycopg2
import requests
from bs4 import BeautifulSoup
import time

from model import host, user, password, db_name, get_price_list, update_price_list

HEADERS = {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Mobile Safari/537.36',
           'accept': '*/*'}

def get_db():
    db = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    return db

db = get_db()

def get_price(url):
    if 'podrygka' in url:
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.text, 'html.parser')
        item = soup.find('span', class_='price__item price__item--current')
        return item.find('span', class_='price_value').get_text()

    if 'goldapple' in url:
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.text, 'html.parser')
        item = soup.find('span', class_='special-price')
        return item.find('meta').get('content')


with  db.cursor() as cursor:
    price_list = get_price_list(cursor)
    for i in price_list:
        print(i)
        price = get_price(i[2])
        time.sleep(2)
        if price:
            response = update_price_list(cursor, i[0], i[1], int(price))
            db.commit()

print('end update')

