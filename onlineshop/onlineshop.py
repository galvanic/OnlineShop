#!/usr/bin/env python
# coding: utf-8

"""
Script to automate who owes what for an online shop (i.e. easily dividing
the bill).

Input:  A .txt file generated by copying the confirmation email content
        into a text file
        Asks who ordered which item
Output: Name of flatmate and their share of costs for that shop.

Future improvements:
- Yahoo Mail API to fetch shop receipt email automatically
- Makes guesses on whose item it is based on previous shop assignments

TODO: naming isn't quite there yet. Might want to explain here exactly
what each 'thing' represents.
"""

import re
import sys
import click
import datetime as dt
from collections import namedtuple
import sqlite3
import logging

from helper import ask, get_latest_file
from db_helper import DB_FILE,\
                      add_new_order,\
                      add_new_purchase,\
                      add_new_purchases,\
                      add_new_flatmate,\
                      add_new_basket_item,\
                      get_flatmate_id,\
                      get_order_purchases,\
                      get_order_baskets

RECEIPT_DIRECTORY = '../data/receipts/'

Purchase = namedtuple('Purchase', 'description, price, quantity')


def parse_receipt(receipt_filepath):
    """Finds all the ordered items (=purchases) in the receipt text (eg. the
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

        subtotal = re.search(r'Sub ?total \(estimated\)\s.(\d\d?\.\d\d)', ifile)
        subtotal = float(subtotal.group(1))

        delivery_cost = re.search(r'Delivery\s.(\d\d?\.\d\d)', ifile)
        delivery_cost = float(delivery_cost.group(1))

        voucher = re.search(r'Voucher Saving\s.(-?\d\d?.\d\d)', ifile)
        voucher = float(voucher.group(1))

    purchases = [Purchase(description, float(price), int(quantity))
        for quantity, description, price in purchases]

    purchases.append(Purchase('Delivery costs', delivery_cost, 1))
    if voucher:
        purchases.append(Purchase('Voucher savings', voucher, 1))

    total = subtotal + voucher + delivery_cost
    logging.info('Subtotal: £{:.2f}'.format(subtotal))
    logging.info('Voucher:  £{:.2f}'.format(voucher))
    logging.info('Delivery: £{:.2f}'.format(delivery_cost))
    logging.info('Total:    £{:.2f}'.format(total))

    order_info = {
        'delivery date': delivery_date,
        'total': total,
    }

    return order_info, purchases


def assign_purchase(purchase):
    """Given an item, prints the quantity and description of the purchase, waits
    for user input and returns a list of purchasers' UIDs.
    User input is expected to be anything that would uniquely identify a
    flatmate (from the other flatmates). Multiple flatmates can be entered
    by seperating their UID by a space.
    """
    purchasers = ask('Who bought   {0.quantity} {0.description}   {1:<10}'.format(purchase, '?'), None, '')
    return purchasers.split()


def assign_order(order_id, conn):
    """"""
    purchases = get_order_purchases(order_id, conn)
    logging.debug('Fetched {} purchases for order {}'.format(len(purchases), order_id))
    purchases = [(pid, Purchase(description, float(price), int(quantity)))
        for pid, description, price, quantity in purchases]

    print('\nEnter flatmate identifier(s) (either a name, initial(s) or number that you keep to later.')
    print('Seperate the identifiers by a space.\n')

    flatmates = []
    for pid, purchase in purchases:

        if purchase.price == 0:
            continue

        purchasers = assign_purchase(purchase)
        cost_each = purchase.price / len(purchasers)

        for flatmate in purchasers:
            if flatmate not in flatmates:
                flatmates.append(flatmate)
                logging.debug('New flatmate: {}'.format(flatmate))
                flatmate_id = add_new_flatmate(flatmate, conn) #
                logging.debug('Flatmate added: ID {}'.format(flatmate_id))
            else:
                flatmate_id = get_flatmate_id(flatmate, conn) #
                logging.debug('Got {}\'s ID: {}'.format(flatmate, flatmate_id))
            basket_item_id = add_new_basket_item(pid, flatmate_id, conn) #
            logging.debug('Basket item added: ID {}'.format(basket_item_id))
    return


def divide_order_bill(order_id, conn):
    """Given an order_id, run a query over database and return
    a dictionary (flatmate UID: their total share of the order bill).

    TODO: need better name for this function
    """
    flatmate_totals = get_order_baskets(order_id, conn)
    flatmate_totals = {flatmate:total for flatmate, total in flatmate_totals}
    return flatmate_totals


def main(receipt_filepath):
    """"""
    if not receipt_filepath:
        receipt_filepath = get_latest_file(RECEIPT_DIRECTORY)
        logging.info('No receipt given, got latest: {}'.format(receipt_filepath))

    order_info, purchases = parse_receipt(receipt_filepath)
    logging.info('Order was delivered on {}'.format(order_info['delivery date']))
    logging.info('There were {} items purchased for a total of £{:.2f}'.format(len(purchases), order_info['total']))

    conn = sqlite3.connect(DB_FILE) #
    logging.debug('Connected to database')

    try:
        order_id = add_new_order(order_info, conn) #
        logging.debug('Order added: ID {}'.format(order_id))

        for index, purchase in enumerate(purchases, 1):
            purchase_id = add_new_purchase(purchase, order_id, conn) #
            logging.debug('Purchase added: ID {}'.format(purchase_id))

        assign_order(order_id, conn) #
        print()

        flatmate_total_share = divide_order_bill(order_id, conn) #
        for flatmate, share_of_total_cost in flatmate_total_share.items():
            print('{} spent £{:.2f}'.format(flatmate, share_of_total_cost))

        logging.info('For a total of £{:.2f}'.format(sum(flatmate_total_share.values())))

    except KeyboardInterrupt:
        pass

    finally:
        conn.close() #
        logging.debug('Closed db connection.')

    return


@click.command()
@click.option('receipt_filepath', '-i', '--receipt',    default=None,
                                                        type=click.Path(exists=True),
                                                        help='Input filepath.')
@click.option('debug', '--debug', is_flag=True)
@click.option('info',  '--info',  is_flag=True)
def cli(debug, info, *args, **kwargs):

    if debug:
        log_level = logging.DEBUG
    elif info:
        log_level = logging.INFO
    else:
        log_level = logging.WARN
    logging.basicConfig(level=log_level)

    return main(*args, **kwargs)


if __name__ == '__main__':
    sys.exit(cli())