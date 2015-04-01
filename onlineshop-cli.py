#!/usr/bin/env python
# coding: utf-8

import sys
import click
from onlineshop.onlineshop import parse_receipt,\
                                    process_input_order,\
                                    calculate_bill_contributions,\
                                    is_order_assigned,\
                                    get_order_purchases


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


def main(receipt_file):
    """"""
    with receipt_file as f:
        receipt_text = f.read()

    order_id = process_input_order(receipt_text)

    assigned = is_order_assigned(order_id)
    if assigned:
        print('Shop is already assigned.')
        pass
    else:
        purchases = get_order_purchases(order_id)
        assign_order(purchases)

    ## calculate individual contributions to bill
    flatmate_contributions = calculate_bill_contributions(order_id)
    for flatmate, flatmate_contribution in flatmate_contributions.items():
        print('{} spent £{:.2f}'.format(flatmate, flatmate_contribution))

    return


@click.command()
@click.argument('receipt_file', type=click.File('r'))
def cli(*args, **kwargs):
    return main(*args, **kwargs)


if __name__ == '__main__':
    sys.exit(cli())