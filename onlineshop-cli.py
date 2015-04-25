#!/usr/bin/env python
# coding: utf-8

import sys
import click

from core import (
    parse_receipt,
    process_input_delivery,
    is_delivery_assigned,
    get_contributions,
    Flatmate,
    Delivery,
    Purchase,
    Assignment,
    db,
)

def assign_purchase(purchase):
    """Given a purchase (Purchase instance), prints the quantity and
    description of the purchase, waits for user input and returns a
    list of purchasers' UIDs.
    User input is expected to be anything that would uniquely identify a
    flatmate (from the other flatmates). Multiple flatmates can be entered
    by seperating their UID by a space.
    """
    purchasers = input('Who bought {:50}'.format('{0.quantity} {0.description} ?'.format(purchase)))
    return purchasers.split()


def assign_delivery(purchases):
    """
    TODO: distinguish between unassigned purchases and purchases where
          we want to modify assignment
    """
    print('\nEnter flatmate identifier(s) (either a name, initial(s) or number that you keep to later.')
    print('Seperate the identifiers by a space.\n')

    flatmates = db.session.query(Flatmate.name).all()
    for purchase in purchases:

        if purchase.price == 0.00:
            continue

        purchasers = assign_purchase(purchase)
        cost_each = purchase.price / len(purchasers)

        for name in purchasers:
            if name not in flatmates:
                flatmates.append(name)
                new_flatmate = Flatmate(name=name.lower())
                db.session.add(new_flatmate)
                db.session.commit()
                flatmate_id = new_flatmate.id
            else:
                flatmate_id = db.session.query(Flatmate.id).filter_by(name=name).one()

            db.session.add(Assignment(
                purchase_id = purchase.id,
                flatmate_id = flatmate_id
            ))
            db.session.commit()
    return


def main(receipt_file):
    """"""
    with receipt_file as f:
        receipt_text = f.read()

    delivery_id = process_input_delivery(receipt_text)

    assigned = is_delivery_assigned(delivery_id)
    if assigned:
        print('Shop is already assigned.')
        pass
    else:
        purchases = db.session.query(Purchase).filter_by(delivery_id=delivery_id).all()
        assign_delivery(purchases)

    ## calculate individual contributions to bill
    for flatmate, flatmate_contribution in get_contributions(delivery_id):
        print('{} spent £{:.2f}'.format(flatmate, flatmate_contribution))

    return


@click.command()
@click.argument('receipt_file', type=click.File('r'))
def cli(*args, **kwargs):
    return main(*args, **kwargs)


if __name__ == '__main__':
    sys.exit(cli())