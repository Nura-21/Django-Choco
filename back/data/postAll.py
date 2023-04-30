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


def insert_certificate(conn, params):
    sql = ''' INSERT INTO choco_life_certificate(id, title, discount, bought_amount, initial_price, event_id)
              VALUES(?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, params)
    conn.commit()
    return cur.lastrowid


def insert_company(conn, params):
    sql = ''' INSERT INTO choco_life_company(id, title, info, sale_points)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, params)
    conn.commit()
    return cur.lastrowid


def insert_event_category(conn, params):
    sql = ''' INSERT INTO choco_life_eventcategory(id, title)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, params)
    conn.commit()
    return cur.lastrowid


def insert_event(conn, params):
    sql = ''' INSERT INTO choco_life_event(id, title, img, alert_info, expiration_date, use_until_date, category_id, company_id)
              VALUES(?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, params)
    conn.commit()
    return cur.lastrowid


def main():
    database = r'../db.sqlite3'
    conn = create_connection(database)
    with conn:
        with codecs.open('event_category.csv', 'r', 'utf-8') as f:
            csv_reader = csv.reader(f, delimiter=';')
            for row in csv_reader:
                insert_event_category(conn, row)
        with codecs.open('company.csv', 'r', 'utf-8') as f:
            csv_reader = csv.reader(f, delimiter=';')
            for row in csv_reader:
                insert_company(conn, row)
        with codecs.open('event.csv', 'r', 'utf-8') as f:
            csv_reader = csv.reader(f, delimiter=';')
            for row in csv_reader:
                insert_event(conn, row)
        with codecs.open('certificate.csv', 'r', 'utf-8') as f:
            csv_reader = csv.reader(f, delimiter=';')
            for row in csv_reader:
                insert_certificate(conn, row)


main()
