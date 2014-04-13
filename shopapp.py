

"""
Seems to be problem with an unclosed socket (??)
"""


from bottle import route, run, template, get, post, request
import bottle_mysql
import csv
from collections import namedtuple
import re
from onlineshop import writeShop2File, getShopItems, isEveryItemAssigned
from code import interact

FLATMATES = ["Jenny", "Emily", "Justine", "Ross", "Harry"]
flatmates = {person: 0.0 for person in FLATMATES}
flatmate_names = sorted(flatmates.keys(), key=len)
flatmate_initials = [name[0] for name in flatmate_names]

# make the ShopItem class (= a named tuple)
ShopItem = namedtuple("ShopItem", "name, price, whose")


def parse_shop_text(ifile):

    items = re.findall(r'(^\d\d?) (.+?) £(\d\d?\.\d\d)', ifile, re.MULTILINE)
    other_info = re.search(r'^Delivery date\s([\w\d ]+).+?Delivery\s*£(\d\d?\.\d\d)\n^Voucher Saving\s*£(-?\d\d?.\d\d)', ifile, re.MULTILINE | re.DOTALL)

    delivery_date = other_info.group(1)
    delivery = float(other_info.group(2))
    voucher  = float(other_info.group(3))

    shop_items = []
    shop_items.append(ShopItem("Delivery costs", delivery, "".join(flatmate_initials)))
    if voucher:
        shop_items.append(ShopItem("Voucher savings", voucher, "".join(flatmate_initials)))

    shop_items += [ShopItem(name, float(price)/float(amount), "") for amount, name, price in items for i in range(int(amount))]
    # need to make function to reformat floated price into a £price

    return shop_items


def calculateMoneyOwed(shop_items, check=False):
    """
    """
    flatmates = {person: 0.0 for person in FLATMATES}
    flatmate_names = sorted(flatmates.keys(), key=len)

    # check every item is assigned otherwise, division by zero next
    if not isEveryItemAssigned:
        # make this into raising an exception?
        return template("Not every item is assigned, so we cannot calculate total.")

    for i, item in enumerate(shop_items):
        amount_people = len([char for char in item.whose if char!= " "])
        for j, person in enumerate(item.whose):
            if person != " ":
                flatmates[flatmate_names[j]] += item.price/float(amount_people)

    # Each person's total:
    for person, total in flatmates.items():
        print("%s\t£%.2f"%(person, total))

    if check:
        print("\nTotal paid by flatmates is £%.2f"%sum(flatmates.values()))
        print("Total paid for all items is £%.2f\n"%sum(item.price for item in shop_items))

    return flatmates


def getRows(date):

    filepath = "%d.csv" % date
    with open(filepath, "rU") as file:
        reader = csv.reader(file)
        rows = list(reader)

    return rows


@route('/')
@route('/index')
@route('/login')
def landing_page():
    return template("login") # dummy page -> links to pasteshop


@route('/pasteshop')
def copy_paste_shop():
    return template("copypaste")


@route('/newshop')
def shoplist(date=140413, debug=True):

    if debug:
        with open("test_shop.txt", "rU") as f:
            shoptext = f.read()
    else:
        shoptext = request.forms.get('shoptext')
    shop_items = parse_shop_text(shoptext)
    writeShop2File(shop_items, "%s.csv"%(date), verbose=True)

    rows = getRows(date)

    return template("shoplist", date=date, rows=rows)


@route('/<date:int>')
def money_owed(date):

    shop_items = getShopItems("%d.csv" % date)
    flatmates = calculateMoneyOwed(shop_items)

    rows = getRows(date)

    return template("shoplist", date=date, rows=rows, money=flatmates)


def main():
    run(host='localhost', port=8080, debug=True)
    return


if __name__ == '__main__':
    main()
