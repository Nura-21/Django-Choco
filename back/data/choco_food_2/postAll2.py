import codecs
import csv
import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn


def insert_rest_category(conn, params):
    sql = ''' INSERT INTO choco_food_restaurantcategory(id, title, img)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, params)
    conn.commit()
    return cur.lastrowid


def insert_restaurant(conn, params):
    sql = ''' INSERT INTO choco_food_restaurant(id, title, description, address, img, delivery_time, delivery_price, category_id)
              VALUES(?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, params)
    conn.commit()
    return cur.lastrowid


def insert_product_category(conn, params):
    sql = ''' INSERT INTO choco_food_productcategory(id, title, icon, restaurant_id)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, params)
    conn.commit()
    return cur.lastrowid


def insert_product(conn, params):
    sql = ''' INSERT INTO choco_food_product(id, title, description, price, img, category_id, restaurant_id)
              VALUES(?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, params)
    conn.commit()
    return cur.lastrowid


def main():
    database = r'../../db.sqlite3'
    conn = create_connection(database)
    with conn:
        with codecs.open('restaurant2.csv', 'r', 'utf-8') as f:
            csv_reader = csv.reader(f, delimiter=';')
            for row in csv_reader:
                insert_restaurant(conn, row)
        with codecs.open('prod_category2.csv', 'r', 'utf-8') as f:
            csv_reader = csv.reader(f, delimiter=';')
            for row in csv_reader:
                insert_product_category(conn, row)
        with codecs.open('product2.csv', 'r', 'utf-8') as f:
            csv_reader = csv.reader(f, delimiter=';')
            for row in csv_reader:
                insert_product(conn, row)


main()
