#!/usr/bin/env python
# coding: utf-8
""""""

from .models import engine, DB_FILE,\
                    Flatmate, Delivery, Purchase, Assignment

from sqlalchemy import text

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()


def is_delivery_assigned(delivery_id):
    """Are all the purchases of the delivery assigned ?
    Is there an Assignment for all the purchases ?
    """
    purchases = session.query(Purchase
        ).filter_by(delivery_id=delivery_id).all()

    for purchase in purchases:
        purchase_is_assigned = session.query(Assignment
            ).filter_by(purchase_id=purchase.id).all()
        
        if not purchase_is_assigned:
            delivery_is_assigned = False
            break
    else:
        delivery_is_assigned = True

    return delivery_is_assigned


def get_contributions(delivery_id):
    """Returns a dictionary {flatmate: total}
    """
    with open('onlineshop/get_baskets.sql', 'r') as ifile:
        stmt = ifile.read()

    stmt = stmt.replace('?', ':delivery_id')
    flatmate_contributions = session.query('f_name', 'f_total'
        ).from_statement(text(stmt)
        ).params(delivery_id=delivery_id
        ).all()

    return flatmate_contributions


def get_purchasers(purchase_id):
    """I.e. get assignments with this purchase_id, and the 
    corresponding flatmates (reminder: a purchase can be bought by
    multiple flatmates so will appear as multiple assignments)
    TODO: do this with a JOIN
    """
    flatmate_ids = session.query(Assignment.flatmate_id
        ).filter_by(purchase_id=purchase_id).all()
    flatmates = [session.query(Flatmate
        ).filter_by(id=f_id).one() for f_id, in flatmate_ids]
    flatmates = sorted(flatmates, key=lambda f: f.name)
    return flatmates