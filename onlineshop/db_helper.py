#!/usr/bin/env python
# coding: utf-8

"""
"""
import sqlite3

DB_FILE = '/Users/jc5809/Dropbox/Programming/Projects/OnlineShop/data/onlineshop.db'


def create_tables(conn):

    ## Table structure for table 'flatmate'
    conn.execute('''CREATE TABLE flatmate (
        id            INTEGER PRIMARY KEY,
        name          CHAR(100) NOT NULL
    )''')

    ## Table structure for table 'shop_order'
    conn.execute('''CREATE TABLE shop_order (
        id            INTEGER PRIMARY KEY,
        delivery_date TEXT NOT NULL
    )''')

    ## Table structure for table 'purchase'
    conn.execute('''CREATE TABLE purchase (
        id            INTEGER PRIMARY KEY,
        description   CHAR(100),
        price         REAL,
        quantity      INTEGER NOT NULL,
        order_id      INTEGER NOT NULL
    )''')

    ## Table structure for table 'basket_item'
    conn.execute('''CREATE TABLE basket_item (
        id            INTEGER PRIMARY KEY,
        purchase_id   INTEGER NOT NULL,
        flatmate_id   INTEGER NOT NULL
    )''')

    conn.commit()
    return


def add_new_order(order_info, conn):
    """
    Creates a new shop order with order info (date, etc.),
    only if order doesn't exist yet.
    """
    curs = conn.cursor()
    curs.execute('INSERT INTO shop_order (delivery_date) VALUES (?)',
        (order_info['delivery date'],))
    conn.commit()
    order_id = curs.lastrowid
    curs.close()
    return order_id


def add_new_purchase(purchase, order_id, conn):
    """
    """
    curs = conn.cursor()
    curs.execute('INSERT INTO purchase (description, price, quantity, order_id) VALUES (?,?,?,?)',
        (purchase.description, purchase.price, purchase.quantity, order_id))
    conn.commit()
    purchase_id = curs.lastrowid
    curs.close()
    return purchase_id


def add_new_purchases(purchases, order_id, conn):
    """
    """
    purchase_ids = []
    for purchase in purchases:
        purchase_id = add_new_purchase(purchase, order_id, conn)
        purchase_ids.append(purchase_id)
    return purchase_ids


def add_new_flatmate(name, conn):
    """
    """
    curs = conn.cursor()
    curs.execute('INSERT INTO flatmate (name) VALUES (?)',
        (name, ))
    conn.commit()
    flatmate_id = curs.lastrowid
    curs.close()
    return flatmate_id


def add_new_basket_item(purchase_id, flatmate_id, conn):
    """
    I.e. assigning a purchase to (a) flatmate(s).
    """
    curs = conn.cursor()
    curs.execute('INSERT INTO basket_item (purchase_id, flatmate_id) VALUES (?,?)',
        (purchase_id, flatmate_id))
    conn.commit()
    basket_item_id = curs.lastrowid
    curs.close()
    return basket_item_id


def get_flatmate_id(name, conn):
    """
    """
    curs = conn.cursor()
    curs.execute('SELECT id FROM flatmate WHERE name = ?',
        (name, ))
    flatmate_id = curs.fetchone()[0]
    curs.close()
    return flatmate_id


if __name__ == '__main__':
    conn = sqlite3.connect(DB_FILE)
    create_tables(conn)
    conn.close()