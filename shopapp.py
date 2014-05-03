#!/usr/bin/env python3.3

"""
"""

import os
from os.path import join, dirname
from bottle import route, run, template, get, post, request, static_file
# import bottle_mysql
from helper import *

appPath = dirname(__file__)

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
    return template("index") # dummy page -> links to pasteshop


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
def shoplist():
    """
    """
    shoptext = request.forms['shoptext']
    flatmate_names = request.forms['flatmate_names'].split()
    shop_items, date = parseShopText(shoptext, flatmate_names)
    writeShop2File(shop_items, "%s.csv" % date, flatmate_names, verbose=True)

    rows = getRows(date)

    return template("shoplist", date=date, rows=rows[1:], flatmates=flatmate_names)


@route('/<date>', method="POST")
def money_owed(date):
    """
    """
    flatmate_names = request.forms['flatmate_names'].split()
    who = request.forms.dict 
    who = [ who["item%d" % idx] for idx in range(len(who)-2) ]
    shop_items = getShopItems("%s.csv" % date, flatmate_names)
    shop_items = getAssignedShopItems(shop_items, who, flatmate_names)

    flatmates = calculateMoneyOwed(shop_items, flatmate_names)
    from code import interact; interact(local=dict( globals(), **locals() ))

    return template("money", date=date, money=flatmates.items(), total=sum(flatmates.values()))


def main():
    # run(host='localhost', port=8080, debug=True)
    run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
    return


if __name__ == '__main__':
    main()

