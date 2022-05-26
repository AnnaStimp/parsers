# данные для подключения к базе данных
host = '127.0.0.1'
user = 'postgres'
password = 'AnnaStimp13'
db_name = 'aggregator'
port = 5432

# функция для внесения данных о товаре в базу данных
def insert_product (cursor, name, about, url, volume, id_category):
  cursor.execute(
    """INSERT INTO product (name_product, about_product, picture_product, volume, id_category)
        VALUES ('{}', '{}', '{}', '{}', {})
        RETURNING id_product;""".format(name, about, url, volume, id_category)
  )

  return cursor.fetchall()

# функция для внесения данных в прайс-лист конкретного товара в базу данных
def insert_price_list (cursor, id_product, id_store, link_product, price):
  cursor.execute(
    """INSERT INTO price_list (id_product, id_store, link_product, price)
        VALUES ({}, {}, '{}', {});""".format(id_product, id_store, link_product, price)
  )

  return cursor.statusmessage