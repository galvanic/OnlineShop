#!/usr/bin/env python3.3

"""
"""

from datetime import datetime
import re
import csv
from collections import namedtuple
from onlineshop import isEveryItemAssigned
import sqlite3
from models import DB_DIR

# make the ShopItem object (= a named tuple)
ShopItem = namedtuple("ShopItem", "item_id, name, price")


def makeSwedishDate(date_string):
    '''
    Swedes represent their dates as YY/MM/DD, or simply YYMMDD
    Returns time_string
    date:           the date as a string "Weekday MonthDay Month"
    time_string:    the date instance converted to a string in Swedish format
    '''
    # first convert input date into a datetime instance
    date = datetime.strptime(" ".join(date_string.split()[1:]), "%d %B") # better way to pop first word off ?

    # next convert datetime instance into our preferred format
    year = str(datetime.now().year)[-2:] # quick hack, doesn't work if it's an old shop
    time_string = date.strftime("%m%d")
    return year + time_string


def parseShopText(ifile, flatmate_names):
    """
    """
    items = re.findall(r'(^\d\d?) (.+?) £(\d\d?\.\d\d)', ifile, re.MULTILINE)

    delivery_date = re.search(r'Delivery date\s([\w\d ]+)', ifile)
    delivery_date = delivery_date.group(1)
    delivery_date = makeSwedishDate(delivery_date)

    delivery_price = re.search(r'Delivery\s.(\d\d?\.\d\d)', ifile) # pound sign doesn't work !!
    delivery_price = float(delivery_price.group(1))

    voucher = re.search(r'Voucher Saving\s.(-?\d\d?.\d\d)', ifile) # pound sign doesn't work !!
    voucher = float(voucher.group(1))

    shop_items = []
    shop_items.append(ShopItem(0, "Delivery costs", delivery_price))
    if voucher:
        shop_items.append(ShopItem(0, "Voucher savings", voucher))

    shop_items += [ShopItem(0, name, float(price)/float(amount)) for amount, name, price in items for i in range(int(amount))]
    return shop_items, delivery_date


def getFlatmateInfo(group_id=None, shop_id=None, info="id"):
    """
    """
    if not group_id:
        group_id = getGroupID(shop_id)

    conn = sqlite3.connect('%s/person.db' % DB_DIR)
    c = conn.cursor()
    c.execute("SELECT %s FROM person WHERE group_id = ?" % info, (group_id, ))
    flatmate_info = c.fetchall()
    c.close()

    flatmate_info = list(zip(*flatmate_info))[0] # not very clean

    return flatmate_info


def getFlatmateName(person_id):
    """
    """
    conn = sqlite3.connect('%s/person.db' % DB_DIR)
    c = conn.cursor()
    c.execute("SELECT name FROM person WHERE id = ?", (person_id, ))
    flatmate_name = c.fetchone()
    c.close()

    return flatmate_name[0]


def getShopID(delivery_date, group_id):
    """
    """
    conn = sqlite3.connect('%s/shop.db' % DB_DIR)
    c = conn.cursor()
    c.execute("SELECT id FROM shop WHERE group_id = ? AND delivery_date = ?", (group_id, int(delivery_date)))
    shop_id = c.fetchone()
    c.close()

    return shop_id[0]


def getGroupID(shop_id):
    """
    """
    conn = sqlite3.connect('%s/shop.db' % DB_DIR)
    c = conn.cursor()
    c.execute("SELECT group_id FROM shop WHERE id = ?", (shop_id, ))
    group_id = c.fetchone()
    c.close()

    return group_id[0]


def getShopItems(shop_id):
    """
    Returns a list of ShopItems.
    """
    # get shop items
    conn = sqlite3.connect('%s/item_to_shop.db' % DB_DIR)
    c = conn.cursor()
    c.execute("SELECT item_id FROM item_to_shop WHERE shop_id = ?", (shop_id,))
    item_ids = c.fetchall()
    c.close()

    item_ids = list(zip(*item_ids))[0] # not very clean

    conn = sqlite3.connect('%s/item.db' % DB_DIR)
    c = conn.cursor()
    shop_items = []
    for item_id in item_ids:
        c.execute("SELECT name, price FROM item WHERE id = ?", (item_id,))
        item_info = c.fetchall()
        name, price = item_info[0]    # ok, I'm missing something here, it must be something else than fetchall()
        shop_items.append((item_id, name, price))
    c.close()

    shop_items = [ShopItem(item_id, name, price) for item_id, name, price in shop_items]

    return shop_items


def assignShopItems(shop_id, who):
    """
    """
    # add assigned items to database 'item_to_shop_to_person'
    conn = sqlite3.connect('%s/item_to_shop_to_person.db' % DB_DIR)
    c = conn.cursor()

    for item_id, people in who:
        for person_id in people:
            c.execute("INSERT INTO item_to_shop_to_person (item_id, shop_id, person_id) VALUES (?, ?, ?)",
                (item_id, shop_id, person_id))
    conn.commit()
    c.close()

    return


def calculateMoneyOwed(shop_id):
    """
    """
    group_id = getGroupID(shop_id)
    flatmate_ids = getFlatmateInfo(group_id=group_id, info="id")
    flatmates = {person: 0.0 for person in flatmate_ids}

    # let's just assume every item is assigned so there won't be a zero division error later

    # get the price of each item which is connected to this shop
    shop_items = getShopItems(shop_id)

    for item in shop_items:

        # get how many times that item appears and the people ids
        conn = sqlite3.connect('%s/item_to_shop_to_person.db' % DB_DIR)
        c = conn.cursor()
        c.execute("SELECT person_id FROM item_to_shop_to_person WHERE item_id = ? AND shop_id = ?",
            (item.item_id, shop_id))
        person_ids = c.fetchall()
        c.close()

        person_ids = list(zip(*person_ids))[0]

        amount_people = len(person_ids)

        for person in person_ids:
            flatmates[person] += item.price/float(amount_people)

    # turn id into name
    flatmates = {getFlatmateName(person_id): owes for person_id, owes in flatmates.items()}

    return flatmates










