#!/usr/bin/env python3.3

"""
"""

import os
from os.path import join, dirname
from bottle import route, run, template, get, post, request, static_file
import sqlite3
# import bottle_mysql
from helper import ShopItem, getShopsInfo, makeSwedishDate, parseShopText, getShopID, getShopItems, assignShopItems, calculateMoneyOwed
from models import DB_DIR

appPath = dirname(__file__)
GROUP_ID = 1

@route('<filename:re:.*\.js>')
def javascripts(filename):
    return static_file(filename, root=join(appPath, 'static'))

@route('<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root=join(appPath, 'static'))

@route('<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
    return static_file(filename, root=join(appPath, 'static'))

@route('/<filename:re:.*\.(eot|ttf|woff|svg)>')
def fonts(filename):
    return static_file(filename, root=join(appPath, 'static'))


@route('/')
@route('/index')
@route('/login')
def landing_page():
    """
    """
    shops = getShopsInfo(GROUP_ID, "delivery_date")
    return template("index", shops=shops)


@route('/pasteshop')
def copy_paste_shop(default=True):
    """
    """
    if default:
        with open("test_shop.txt", "rU") as ifile:
            default_shop = ifile.read()
    else:
        default_shop = ""
    return template("pasteshop", default_shop=default_shop)


@route('/newshop', method="POST")
def shoplist(group_id=GROUP_ID):
    """
    """
    shoptext = request.forms['shoptext']
    flatmate_names = request.forms['flatmate_names'].split()

    # add flatmates to database 'person' and keep ids

    flatmates = {}

    conn = sqlite3.connect('%s/person.db' % DB_DIR)
    c = conn.cursor()
    for flatmate_name in flatmate_names:
        c.execute("INSERT INTO person (name, group_id) VALUES (?, ?)", (flatmate_name, group_id))
        flatmates[flatmate_name] = c.lastrowid
    conn.commit()
    c.close()

    # fetch shop and its items
    
    shop_items, date = parseShopText(shoptext, flatmate_names)

    # add shop to database 'shop'

    conn = sqlite3.connect('%s/shop.db' % DB_DIR)
    c = conn.cursor()
    c.execute("INSERT INTO shop (delivery_date, group_id) VALUES (?, ?)", (int(date), group_id))
    shop_id = c.lastrowid
    conn.commit()
    c.close()

    # add items to database 'item' and 'item_to_shop'

    conn = sqlite3.connect('%s/item.db' % DB_DIR)
    conn2 = sqlite3.connect('%s/item_to_shop.db' % DB_DIR)
    c = conn.cursor()
    c2 = conn2.cursor()
    for item in shop_items:
        c.execute("INSERT INTO item (name, price) VALUES (?, ?)", (item.name, item.price))
        item_id = c.lastrowid
        c2.execute("INSERT INTO item_to_shop (item_id, shop_id) VALUES (?, ?)", (item_id, shop_id))
    conn.commit()
    conn2.commit()
    c.close()
    c2.close()

    rows = getShopItems(shop_id)

    return template(
        "shoplist",
        date=date,
        rows=enumerate(rows),
        flatmates=flatmates.items()
        )


@route('/<date>', method="POST")
def money_owed(date, group_id=GROUP_ID):
    """
    """
    who = request.forms.dict
    who.pop('submit', None) # could pop anything that wasn't 'item'
    who = who.items()
    who = sorted(who, key=lambda x: x[0])

    shop_id = getShopID(date, group_id)
    assignShopItems(shop_id, who)

    flatmates = calculateMoneyOwed(shop_id)

    return template("money", date=date, money=flatmates.items(), total=sum(flatmates.values()))


def main():
    # run(host='localhost', port=8080, debug=True)
    run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
    return


if __name__ == '__main__':
    main()

