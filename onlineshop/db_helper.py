#!/usr/bin/env python
# coding: utf-8

"""
"""
import sqlite3

DB_FILE = '/Users/jc5809/Dropbox/Programming/Projects/OnlineShop/data/onlineshop.db'


def create_tables(conn):

    # enable Foreign key constraints (disabled by default for backwards compatibility)
    conn.execute('PRAGMA foreign_keys = ON')
    conn.commit()

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
        order_id      INTEGER NOT NULL,
        FOREIGN KEY(order_id) REFERENCES shop_order(id)
    )''')

    ## Table structure for table 'basket_item'
    conn.execute('''CREATE TABLE basket_item (
        id            INTEGER PRIMARY KEY,
        purchase_id      INTEGER NOT NULL,
        flatmate_id      INTEGER NOT NULL,
        FOREIGN KEY(purchase_id) REFERENCES purchase(id),
        FOREIGN KEY(flatmate_id) REFERENCES flatmate(id)
    )''')

    conn.commit()
    return


def add_new_order(order_info, conn):
    """Creates a new shop order with order info (date, etc.),
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
    """"""
    curs = conn.cursor()
    curs.execute('INSERT INTO purchase (description, price, quantity, order_id) VALUES (?,?,?,?)',
        (purchase.description, purchase.price, purchase.quantity, order_id))
    conn.commit()
    purchase_id = curs.lastrowid
    curs.close()
    return purchase_id


def add_new_purchases(purchases, order_id, conn):
    """"""
    purchase_ids = []
    for purchase in purchases:
        purchase_id = add_new_purchase(purchase, order_id, conn)
        purchase_ids.append(purchase_id)
    return purchase_ids


def add_new_flatmate(name, conn):
    """"""
    curs = conn.cursor()
    curs.execute('INSERT INTO flatmate (name) VALUES (?)',
        (name, ))
    conn.commit()
    flatmate_id = curs.lastrowid
    curs.close()
    return flatmate_id


def add_new_basket_item(purchase_id, flatmate_id, conn):
    """I.e. assigning a purchase to (a) flatmate(s).
    """
    curs = conn.cursor()
    curs.execute('INSERT INTO basket_item (purchase_id, flatmate_id) VALUES (?,?)',
        (purchase_id, flatmate_id))
    conn.commit()
    basket_item_id = curs.lastrowid
    curs.close()
    return basket_item_id


def get_flatmate_id(name, conn):
    """"""
    curs = conn.cursor()
    curs.execute('SELECT id FROM flatmate WHERE name = ?',
        (name, ))
    flatmate_id = curs.fetchone()[0]
    curs.close()
    return flatmate_id


def get_order_purchases(order_id, conn):
    """"""
    curs = conn.cursor()
    curs.execute('''SELECT id, description, price, quantity
        FROM purchase WHERE order_id = ?''', (order_id, ))
    purchases = curs.fetchall()
    curs.close()
    return purchases


def get_order_baskets(order_id, conn):
    """Returns a list of tuples [(flatmate, total), (flatmate, total)]
    """
    with open('onlineshop/get_baskets.sql', 'r') as ifile:
        query = ifile.read()

    curs = conn.cursor()
    curs.execute(query, (order_id, ))
    baskets = curs.fetchall()
    curs.close()
    return baskets


def order_exists(delivery_date, conn):
    """Checks if an order exists, returns Boolean accordingly.
    """
    curs = conn.cursor()
    curs.execute('SELECT * FROM shop_order WHERE delivery_date = ?',
        (delivery_date, ))
    orders = curs.fetchone()
    curs.close()
    return bool(orders)


def get_order_id(delivery_date, conn):
    """"""
    curs = conn.cursor()
    curs.execute('SELECT id FROM shop_order WHERE delivery_date = ?',
        (delivery_date, ))
    order_id = curs.fetchone()[0]
    curs.close()
    return order_id


def purchase_assigned(purchase_id, conn):
    """Returns amount of people assigned to that purchase.
    """
    curs = conn.cursor()
    curs.execute('''SELECT COUNT(*) FROM basket_item
        WHERE purchase_id = ?
        GROUP BY purchase_id''',
        (purchase_id, ))
    flatmate_count = curs.fetchone()[0]
    curs.close()
    return flatmate_count


def get_count_unassigned(order_id, conn):
    """Returns amount of una
    """
    curs = conn.cursor()
    curs.execute('''SELECT
            purchase.id,
            COUNT(distinct basket_item.flatmate_id)
        FROM purchase
        LEFT OUTER JOIN basket_item
            ON purchase.id = basket_item.purchase_id
        WHERE purchase.order_id = ?
        GROUP BY purchase.id''',
        (order_id, ))
    assigned_puchases = curs.fetchall()
    curs.close()

    print(assigned_puchases)
    count_unassigned = len([p for p in assigned_puchases if p[1] == 0])
    print(count_unassigned)

    return count_unassigned


def get_orders(conn):
    """Returns a list of tuples of order information
    """
    curs = conn.cursor()
    curs.execute('SELECT id, delivery_date FROM shop_order')
    orders = curs.fetchall()
    curs.close()
    return orders


def get_flatmate_names(conn):
    """Returns a list of flatmate names.
    """
    curs = conn.cursor()
    curs.execute('SELECT name FROM flatmate')
    flatmates = curs.fetchall()
    flatmates = [f[0] for f in flatmates]
    curs.close()
    return flatmates


if __name__ == '__main__':
    conn = sqlite3.connect(DB_FILE)
    create_tables(conn)
    conn.close()