#!/usr/bin/env python3.3

"""
"""

import os
from bottle import route, run, template, get, post, request, static_file
# import bottle_mysql
from helper import *


@route('<filename:re:.*\.js>')
def javascripts(filename):
    return static_file(filename, root='static')

@route('<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root='static')

@route('<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
    return static_file(filename, root='static')


@route('/')
@route('/index')
@route('/login')
def landing_page():
    """
    """
    return template("login") # dummy page -> links to pasteshop


@route('/pasteshop')
def copy_paste_shop(debug=True):
    """
    """
    if debug:
        with open("test_shop.txt", "rU") as ifile:
            default_shop = ifile.read()
    return template("pasteshop", default_shop=default_shop)


@route('/newshop', method="POST")
def shoplist():
    """
    """
    shoptext = request.forms['shoptext']
    shop_items, date = parseShopText(shoptext)
    writeShop2File(shop_items, "%s.csv" % date, verbose=True)

    rows = getRows(date)

    return template("shoplist", date=date, rows=rows[1:], flatmates=list(enumerate(FLATMATES, 1)))


@route('/<date>', method="POST")
def money_owed(date):
    """
    """
    who = request.forms.dict
    who = [ who["item%d" % idx] for idx in range(len(who)-1) ]
    shop_items = getShopItems("%s.csv" % date)
    shop_items = getAssignedShopItems(shop_items, who)

    flatmates = calculateMoneyOwed(shop_items)

    return template("money", date=date, money=flatmates.items(), total=sum(flatmates.values()))


def main():
    # run(host='localhost', port=8080, debug=True)
    run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
    return


if __name__ == '__main__':
    main()
