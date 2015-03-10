#!/usr/bin/env python
# coding: utf-8

"""
Script to automate who owes what for an online shop (i.e. easily dividing
the bill).

Input:  A .txt file generated by copying the confirmation email content
        into a text file
        Asks who ordered which item
Output: Name of flatmate and amount they owe for that shop.

Future improvements:
- Yahoo Mail API to fetch shop receipt email automatically
- Makes guesses on whose item it is based on previous shop assignments
"""

import re
import sys
import click
import datetime as dt
from collections import namedtuple

from helper import ask, get_latest_file

Purchase = namedtuple('Purchase', 'name, price, amount')

RECEIPT_DIRECTORY='../data/receipts/'


def parse_receipt(receipt_filepath):
    """
    Finds all the ordered items (=purchases) in the receipt text (eg. the
    confirmation email for Ocado orders) using regular expressions.
    Returns a list of Purchases.
    """
    with open(receipt_filepath, 'rU') as f:
        ifile = f.read()
        purchases = re.findall(r'(^\d\d?) (.+?) £(\d\d?\.\d\d)', ifile, re.MULTILINE)

        delivery_date = re.search(r'Delivery date\s([\w\d ]+)', ifile)
        delivery_date = delivery_date.group(1)
        # format is WeekdayName MonthdayNumber MonthName
        delivery_date = dt.datetime.strptime(delivery_date, '%A %d %B')

        delivery_cost = re.search(r'Delivery\s.(\d\d?\.\d\d)', ifile)
        delivery_cost = float(delivery_cost.group(1))

        voucher = re.search(r'Voucher Saving\s.(-?\d\d?.\d\d)', ifile)
        voucher = float(voucher.group(1))

    purchases = [Purchase(name, float(price), int(amount)) 
        for amount, name, price in purchases]

    purchases.append(Purchase('Delivery costs', delivery_cost, 1))
    if voucher:
        purchases.append(Purchase('Voucher savings', voucher, 1))

    subtotal = sum([float(purchase.price) for purchase in purchases])
    total = subtotal + voucher + delivery_cost

    order_info = {
        'total': total,
        'subtotal': subtotal,
        'voucher': voucher,
        'delivery cost': delivery_cost,
        'delivery date': delivery_date,
    }

    return order_info, purchases


def assign_purchase(purchase):
    """
    Given an item, prints the amount and name of the purchase, waits
    for user input and returns a list of purchasers' UIDs.
    User input is expected to be anything that would uniquely identify a
    flatmate (from the other flatmates). Multiple flatmates can be entered
    by seperating their UID by a space.
    """
    purchasers = ask('Who bought   {0.amount} {0.name}   {1:<10}'.format(purchase, '?'), None, '')
    return purchasers


def calculate_money_spent_by_each(baskets):
    """
    Given a dictionary (flatmate UID: their cost share of each of
    their purchases), return a dictionary (flatmate UID: their total
    share of the order bill).

    TODO: need better name for this function
    """
    baskets = {person:sum(purchases) for person, purchases in baskets.items()}
    return baskets


def main(receipt_filepath):
    """"""
    if not receipt_filepath:
        receipt_filepath = get_latest_file(RECEIPT_DIRECTORY)

    order_info, purchases = parse_receipt(receipt_filepath)

    ## assign all purchases
    print('\nEnter flatmate identifier(s) (either a name, initial(s) or number that you keep to later.')
    print('Seperate the identifiers by a space.\n')

    people = {}
    for index, purchase in enumerate(purchases, 1):
        if purchase.price == 0:
            continue

        purchasers = assign_purchase(purchase)
        purchasers = purchasers.split()

        cost_each = purchase.price / float(purchase.amount)

        for person in purchasers:
            if person in people:
                people[person].append(cost_each)
            else:
                people[person] = [cost_each]

    ## display how much each person owes for the shop order
    for person, owes in calculate_money_spent_by_each(people).items():
        print('{} spent £{:.2f}'.format(person, owes))

    return


@click.command()
@click.option('receipt_filepath', '-i', '--receipt',    default=None,
                                                        type=click.Path(exists=True),
                                                        help='Input filepath.')
def cli(*args, **kwargs):
    return main(*args, **kwargs)


if __name__ == '__main__':
    sys.exit(cli())