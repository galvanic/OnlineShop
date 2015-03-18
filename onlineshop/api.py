#!/usr/bin/env python
# coding: utf-8

"""
"""
import sqlite3
import requests

ADDRESS = 'http://localhost:8080'
DB_FILE = '/Users/jc5809/Dropbox/Programming/Projects/OnlineShop/data/onlineshop.db'


def create_tables():
    """"""
    with open('onlineshop/tables.sql', 'r') as ifile:
        queries = ifile.read().split('\n\n')

    conn = sqlite3.connect(DB_FILE)
    curs = conn.cursor()
    for query in queries:
        curs.execute(query)
        conn.commit()
    curs.close()
    conn.close()
    return


def does_order_exist(order_info):
    """Checks if an order exists, returns Boolean accordingly.
    """
    payload = { 'delivery_date': order_info['delivery_date'] }
    resp = requests.get('{}/shop_orders'.format(ADDRESS), params=payload)
    order_exists = len(resp.json()['resources'])
    return order_exists


def get_order_id(order_info):
    """"""
    payload = { 'delivery_date': order_info['delivery_date'] }
    resp = requests.get('{}/shop_orders'.format(ADDRESS), params=payload)
    order_id = resp.json()['resources'][0]['id']
    return order_id


def add_new_order(order_info):
    """Creates a new shop order with order info (date, etc.).
    Assumes order doesn't exist yet.
    """
    resp = requests.post('{}/shop_orders'.format(ADDRESS), data=order_info)
    order_id = resp.json()['id']
    return order_id


def add_new_purchase(purchase, order_id):
    """Creates a new purchase.
    purchase input must be a dictionary.
    """
    purchase['order_id'] = order_id
    resp = requests.post('{}/purchases'.format(ADDRESS), data=purchase)
    purchase_id = resp.json()['id']
    return purchase_id


def get_order_purchases(order_id):
    """"""
    payload = { 'order_id': order_id }
    resp = requests.get('{}/purchases'.format(ADDRESS), params=payload)
    purchases = resp.json()['resources']
    return purchases


def is_order_assigned(order_id):
    """Are all the purchases of the order assigned ?
    Is there a basket_item for all the purchases ?
    """
    purchases = get_order_purchases(order_id)
    purchase_ids = [p['id'] for p in purchases]

    for p_id in purchase_ids:
        payload = { 'purchase_id': p_id }
        resp = requests.get('{}/basket_items'.format(ADDRESS), params=payload)
        basket_item_exists = len(resp.json()['resources'])
        if not basket_item_exists:
            order_is_assigned = False
            break
    else:
        order_is_assigned = True

    return order_is_assigned


def get_flatmate_names():
    """"""
    resp = requests.get('{}/flatmates'.format(ADDRESS))
    flatmates = resp.json()['resources']
    flatmate_names = [f['name'] for f in flatmates]
    return flatmate_names


def add_new_flatmate(name):
    """Assumes name isn't already present in database
    """
    payload = { 'name': name }
    resp = requests.post('{}/flatmates'.format(ADDRESS), data=payload)
    flatmate_id = resp.json()['id']
    return flatmate_id


def get_flatmate_id(name):
    """"""
    payload = { 'name': name }
    resp = requests.get('{}/flatmates'.format(ADDRESS), params=payload)
    flatmate_id = resp.json()['resources'][0]['id']
    return flatmate_id


def add_new_basket_item(purchase_id, flatmate_id):
    """I.e. assigning a purchase to (a) flatmate(s).
    """
    payload = {
        'purchase_id': purchase_id,
        'flatmate_id': flatmate_id
    }
    resp = requests.post('{}/basket_items'.format(ADDRESS), data=payload)
    basket_item_id = resp.json()['id']
    return basket_item_id


def get_order_baskets(order_id):
    """Returns a dictionary {flatmate: total}
    """
    with open('onlineshop/get_baskets.sql', 'r') as ifile:
        query = ifile.read()

    conn = sqlite3.connect(DB_FILE)
    curs = conn.cursor()
    curs.execute(query, (order_id, ))
    baskets = curs.fetchall()
    curs.close()
    conn.close()

    flatmate_contributions = {flatmate:total for flatmate, total in baskets}
    return flatmate_contributions


def get_orders():
    """"""
    resp = requests.get('{}/shop_orders'.format(ADDRESS))
    orders = resp.json()['resources']
    return orders


def get_order(order_id):
    """"""
    payload = { 'id': order_id }
    resp = requests.get('{}/shop_orders'.format(ADDRESS), params=payload)
    order = resp.json()['resources'][0]
    return order


def get_purchasers(purchase_id):
    """I.e. get baskets items with this purchase_id, and the 
    corresponding flatmate
    """
    payload = { 'purchase_id': purchase_id }
    resp = requests.get('{}/basket_items'.format(ADDRESS), params=payload)
    basket_items = resp.json()['resources']
    flatmates = []
    for item in basket_items:
        payload = { 'id': item['flatmate_id'] }
        resp = requests.get('{}/flatmates'.format(ADDRESS), params=payload)
        flatmates.append(resp.json()['resources'][0]['name'])
    return flatmates


if __name__ == '__main__':

    create_tables()