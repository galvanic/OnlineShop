#!/usr/bin/env python3.3

"""
"""

from datetime import datetime
import re
import csv
from collections import namedtuple
from onlineshop import isEveryItemAssigned


FLATMATES = ["Alice", "Bob", "Cass"]
flatmate_initials = [name[0] for name in FLATMATES]

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


def parseShopText(ifile):
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
    shop_items.append(ShopItem("Delivery costs", delivery_price, "".join(flatmate_initials)))
    if voucher:
        shop_items.append(ShopItem("Voucher savings", voucher, "".join(flatmate_initials)))

    shop_items += [ShopItem(name, float(price)/float(amount), "") for amount, name, price in items for i in range(int(amount))]
    return shop_items, delivery_date


def writeShop2File(shop_items, ofilename, verbose=False):
    """
    """
    with open(ofilename, "w") as ofile:
        writer = csv.writer(ofile, dialect='excel')

        # title row
        writer.writerow(["#", "Name", "Price"] + FLATMATES)

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


def getShopItems(filename):
    """
    From a csv file,
    Returns an (ordered) list of ShopItems.     # ordered by what ??
    """
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


def getAssignedShopItems(shop_items, people):
    """
    Returns list of assigned shop items (assigned to housemates).
    """
    modified_shopitems = list()

    for item, who in zip(shop_items, people):

        whose = ""
        for j, person in enumerate(FLATMATES):
            if person in who:
                whose += flatmate_initials[j]
            else: whose += " "

        modified_shopitems.append(ShopItem(item.name, item.price, whose))

    return modified_shopitems


def calculateMoneyOwed(shop_items):
    """
    """
    flatmates = {person: 0.0 for person in FLATMATES}

    # check every item is assigned otherwise, division by zero next
    if not isEveryItemAssigned:
        # make this into raising an exception?
        raise ValueError

    for i, item in enumerate(shop_items):
        amount_people = len([char for char in item.whose if char!= " "])
        for j, person in enumerate(item.whose):
            if person != " ":
                flatmates[FLATMATES[j]] += item.price/float(amount_people)

    return flatmates


def getRows(date):
    """
    """
    filepath = "%s.csv" % date
    with open(filepath, "rU") as file:
        reader = csv.reader(file)
        rows = [ row[:3] for row in reader ] 
    return rows