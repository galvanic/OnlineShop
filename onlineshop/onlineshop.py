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
import datetime as dt

from .api import does_order_exist,\
                    get_order_id,\
                    add_new_order,\
                    add_new_purchase,\
                    is_order_assigned,\
                    get_order_purchases,\
                    get_flatmate_names,\
                    add_new_flatmate,\
                    get_flatmate_id,\
                    add_new_basket_item,\
                    get_order_baskets


def parse_receipt(receipt_text):
    """Finds all the ordered items (=purchases) in the receipt text (eg. the
    confirmation email for Ocado orders) using regular expressions.
    Returns a tuple (dict of order information,
                    list of tuples (description, quantity, price)).
    """
    purchases = re.findall(r'(^\d\d?) (.+?) £(\d\d?\.\d\d)', receipt_text, re.MULTILINE)

    delivery_date = re.search(r'Delivery date\s([\w\d ]+)', receipt_text)
    delivery_date = delivery_date.group(1)
    # format is WeekdayName MonthdayNumber MonthName
    delivery_date = dt.datetime.strptime(delivery_date, '%A %d %B')

    subtotal = re.search(r'Sub ?total \(estimated\)\s.(\d\d?\.\d\d)', receipt_text)
    subtotal = float(subtotal.group(1))

    delivery_cost = re.search(r'Delivery\s.(\d\d?\.\d\d)', receipt_text)
    delivery_cost = float(delivery_cost.group(1))

    voucher = re.search(r'Voucher Saving\s.(-?\d\d?.\d\d)', receipt_text)
    voucher = float(voucher.group(1))

    purchases = [
        {
            'description': description,
            'quantity':    int(quantity),
            'price':       float(price)
        }

        for quantity, description, price in purchases
    ]

    purchases.append({
        'description': 'Delivery costs',
        'quantity':    1,
        'price':       delivery_cost
    })

    if voucher:
        purchases.append({
            'description': 'Voucher savings',
            'quantity':    1,
            'price':       voucher
        })

    total = subtotal + voucher + delivery_cost

    order_info = {
        'delivery_date': delivery_date,
        'total': total
    }

    return order_info, purchases


def process_input_order(receipt_text):
    """"""
    order_info, purchases = parse_receipt(receipt_text)

    order_exists = does_order_exist(order_info)
    if order_exists:
        order_id = get_order_id(order_info)
    else:
        order_id = add_new_order(order_info)

        for purchase in purchases:
            add_new_purchase(purchase, order_id)

    return order_id


def assign_purchase(purchase):
    """Given an item, prints the quantity and description of the purchase, waits
    for user input and returns a list of purchasers' UIDs.
    User input is expected to be anything that would uniquely identify a
    flatmate (from the other flatmates). Multiple flatmates can be entered
    by seperating their UID by a space.
    """
    purchasers = input('Who bought {:50}'.format('{quantity} {description} ?'.format(**purchase)))
    return purchasers.split()


def assign_order(purchases):
    """
    TODO: distinguish between unassigned purchases and purchases where
          we want to modify assignment
    """
    print('\nEnter flatmate identifier(s) (either a name, initial(s) or number that you keep to later.')
    print('Seperate the identifiers by a space.\n')

    flatmates = get_flatmate_names()
    for purchase in purchases:

        if purchase['price'] == 0.00:
            continue

        purchasers = assign_purchase(purchase)
        cost_each = purchase['price'] / len(purchasers)

        for flatmate in purchasers:
            if flatmate not in flatmates:
                flatmates.append(flatmate)
                flatmate_id = add_new_flatmate(flatmate)
            else:
                flatmate_id = get_flatmate_id(flatmate)
            basket_item_id = add_new_basket_item(purchase['id'], flatmate_id)
    print()
    return


def calculate_bill_contributions(order_id):
    """Given an order_id, run a query over database and return
    a dictionary (flatmate UID: their total share of the order bill).

    TODO: need better name for this function
    """
    flatmate_contributions = get_order_baskets(order_id)
    return flatmate_contributions


def main(receipt_file):
    """"""
    with receipt_file as f:
        receipt_text = f.read()

    order_id = process_input_order(receipt_text)

    assigned = is_order_assigned(order_id)
    if assigned:
        pass
    else:
        purchases = get_order_purchases(order_id)
        assign_order(purchases)

    ## calculate individual contributions to bill
    flatmate_contributions = calculate_bill_contributions(order_id)
    for flatmate, flatmate_contribution in flatmate_contributions.items():
        print('{} spent £{:.2f}'.format(flatmate, flatmate_contribution))

    return