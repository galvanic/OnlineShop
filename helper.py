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
ShopItem = namedtuple("ShopItem", "name, price, whose")


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
    flatmate_initials = [name[0] for name in flatmate_names]

    items = re.findall(r'(^\d\d?) (.+?) £(\d\d?\.\d\d)', ifile, re.MULTILINE)

    delivery_date = re.search(r'Delivery date\s([\w\d ]+)', ifile)
    delivery_date = delivery_date.group(1)
    delivery_date = makeSwedishDate(delivery_date)

    delivery_price = re.search(r'Delivery\s.(\d\d?\.\d\d)', ifile) # pound sign doesn't work !!
    delivery_price = float(delivery_price.group(1))

    voucher = re.search(r'Voucher Saving\s.(-?\d\d?.\d\d)', ifile) # pound sign doesn't work !!
    voucher = float(voucher.group(1))

    shop_items = []
    shop_items.append(ShopItem("Delivery costs", delivery_price, "".join(flatmate_initials)))
    if voucher:
        shop_items.append(ShopItem("Voucher savings", voucher, "".join(flatmate_initials)))

    shop_items += [ShopItem(name, float(price)/float(amount), "") for amount, name, price in items for i in range(int(amount))]
    return shop_items, delivery_date


def writeShop2File(shop_items, ofilename, flatmate_names, verbose=False):
    """
    """
    with open(ofilename, "w") as ofile:
        writer = csv.writer(ofile, dialect='excel')

        # title row
        writer.writerow(["#", "Name", "Price"] + flatmate_names)

        for i, item in enumerate(shop_items):
            who_ordered = []
            # this assumes whose is ordered
            for initial in item.whose:
                if initial != " ":
                    who_ordered.append("yes")
                else:
                    who_ordered.append("")
            writer.writerow([i, item.name, item.price] + who_ordered)
    if verbose:
        print("\nWritten to file %s.\n"%(ofilename))
    return


def getShopItems(filename, flatmate_names):
    """
    From a csv file,
    Returns an (ordered) list of ShopItems.     # ordered by what ??
    """
    flatmate_initials = [name[0] for name in flatmate_names]

    if filename[-3:] == "txt":
        return findShopItems(filename)

    shop_items = list()
    with open(filename, "rU") as f:
        csv_reader = csv.reader(f)
        for i, row in enumerate(csv_reader):
            number, itemname, price, *flatmate_headers = row
            if i == 0:
                continue    # skips header
            whose = ""
            for j, name in enumerate(flatmate_headers):
                if name:
                    whose += flatmate_initials[j]
                else:
                    whose += " "
            s = ShopItem(itemname, float(price), whose)
            shop_items.append(s)
    return shop_items


def getAssignedShopItems(shop_items, people, flatmate_names):
    """
    Returns list of assigned shop items (assigned to housemates).
    """
    flatmate_initials = [name[0] for name in flatmate_names]

    modified_shopitems = list()

    for item, who in zip(shop_items, people):

        whose = ""
        for j, person in enumerate(flatmate_names):
            if person in who:
                whose += flatmate_initials[j]
            else: whose += " "

        modified_shopitems.append(ShopItem(item.name, item.price, whose))

    return modified_shopitems


def calculateMoneyOwed(shop_items, flatmate_names):
    """
    """
    flatmates = {person: 0.0 for person in flatmate_names}

    # check every item is assigned otherwise, division by zero next
    if not isEveryItemAssigned:
        # make this into raising an exception?
        raise ValueError

    for i, item in enumerate(shop_items):
        amount_people = len([char for char in item.whose if char!= " "])
        for j, person in enumerate(item.whose):
            if person != " ":
                flatmates[flatmate_names[j]] += item.price/float(amount_people)

    return flatmates


def getRows(shop_id):
    """
    Get the name and price of all the items which are in the shop with that shop_id
    """
    conn = sqlite3.connect('%s/item_to_shop.db' % DB_DIR)
    c = conn.cursor()
    c.execute("SELECT item_id FROM item_to_shop WHERE shop_id = ?", (shop_id,))
    item_ids = c.fetchall()
    c.close()

    item_ids = list(zip(*item_ids))[0] # not very clean

    conn = sqlite3.connect('%s/item.db' % DB_DIR)
    c = conn.cursor()
    all_item_info = []
    for item_id in item_ids:
        c.execute("SELECT name, price FROM item WHERE id = ?", (item_id,))
        item_info = c.fetchall()
        item_info = item_info[0]    # ok, I'm missing something here, it must be something else than fetchall()
        all_item_info.append(item_info)
    c.close()

    r = [list(range(1, len(item_ids)+1)), ]
    data = zip(*(r + list(zip(*all_item_info))))

    return data








