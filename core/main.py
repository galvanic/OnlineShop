# coding: utf-8

"""
Script to automate who owes what for an online shop (i.e. easily dividing
the bill).

Input:  A .txt file generated by copying the confirmation email content
        into a text file
        Asks who ordered which item
Output: Name of flatmate and their share of costs for that shop.
"""

import re
import sys
import datetime as dt

from .models import (
    Flatmate,
    Delivery,
    Purchase,
    Assignment,
)
from sqlalchemy import text
from core import db

### HELPERS

def is_delivery_assigned(delivery_id):
    """Are all the purchases of the delivery assigned ?
    Is there an Assignment for all the purchases ?
    """
    purchases = db.session.query(Purchase
        ).filter_by(delivery_id=delivery_id).all()

    for purchase in purchases:
        purchase_is_assigned = db.session.query(Assignment
            ).filter_by(purchase_id=purchase.id).all()
        
        if not purchase_is_assigned:
            delivery_is_assigned = False
            break
    else:
        delivery_is_assigned = True

    return delivery_is_assigned


def get_contributions(delivery_id):
    """Returns a dictionary (flatmate_name, total)
    """
    with open('core/queries/get_contributions.sql', 'r') as ifile:
        stmt = ifile.read()

    stmt = stmt.replace('?', ':delivery_id')
    contribs = db.session.query('f_name', 'f_total'
        ).from_statement(text(stmt)
        ).params(delivery_id=delivery_id
        ).all()

    contribs = [(name, round(total, 2)) for name, total in contribs]

    return contribs


def get_purchasers(purchase_id):
    """I.e. get assignments with this purchase_id, and the 
    corresponding flatmates (reminder: a purchase can be bought by
    multiple flatmates so will appear as multiple assignments)
    TODO: do this with a JOIN
    """
    flatmate_ids = db.session.query(Assignment.flatmate_id
        ).filter_by(purchase_id=purchase_id).all()
    flatmates = [db.session.query(Flatmate
        ).filter_by(id=f_id).one() for f_id, in flatmate_ids]
    flatmates = sorted(flatmates, key=lambda f: f.name)
    return flatmates

###

def parse_receipt(receipt_text):
    """Finds all the ordered items (=purchases) in the receipt text (eg. the
    confirmation email for Ocado deliverys) using regular expressions.
    Returns a tuple (dict of delivery information,
                    list of tuples (description, quantity, price)).
    """
    purchases = re.findall(r'(^\d\d?) (.+?) £(\d\d?\.\d\d)', receipt_text, re.MULTILINE)

    delivery_date = re.search(r'Delivery date\s([\w\d ]+)', receipt_text)
    delivery_date = delivery_date.group(1)
    # format is WeekdayName MonthdayNumber MonthName
    delivery_date = dt.datetime.strptime(delivery_date, '%A %d %B')
    delivery_date = delivery_date.date()

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

    delivery_info = {
        'date': delivery_date,
        'total': total
    }

    return delivery_info, purchases


def process_input_delivery(receipt_text):
    """Parses the receipt text. Looks to see if a receipt with that
    date already exists in the database (assumed that there wouldn't
    be multiple deliveries on the same day). If the delivery already
    exists, it's also assumed that its purchases will have already
    been added to the database. Otherwise if the delivery isn't found in
    the database, the purchases are added to the database.
    Returns the delivery id (whether the delivery existed and the id was
    fetched from the database or the delivery was new and a new id was
    created)
    """
    delivery_info, purchases = parse_receipt(receipt_text)

    delivery = db.session.query(Delivery).filter_by(date=delivery_info['date']).first()

    if delivery:
        print('Shop already exists.')
        pass

    else:
        new_delivery = Delivery(
            date = delivery_info['date'],
            total = delivery_info['total']
        )
        db.session.add(new_delivery)
        db.session.commit()

        purchases = [
            Purchase(
                description = p['description'],
                quantity = p['quantity'],
                price = p['price'],
                delivery_id = new_delivery.id
            )   for p in purchases
        ]
        db.session.add_all(purchases)
        db.session.commit()

        delivery = new_delivery

    return delivery.id