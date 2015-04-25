
from webapp import app, db
from flask import (
    render_template,
    send_from_directory,
    request,
    redirect,
    url_for,
)

from itertools import chain

import core as api
from core import (
    Flatmate,
    Delivery,
    Purchase,
    Assignment,
)

###
### controllers: main pages
###


@app.route('/')
@app.route('/index')
def index():
    """Renders the landing page with:
    - list of flatmates
    - list of previous deliverys (just the delivery date)
    - button to form page to add flatmate(s)
    - button to form page to add delivery
    """
    return render_template('index.html',
        flatmates = db.session.query(Flatmate).order_by(Flatmate.name).all(),
        deliverys = db.session.query(Delivery).all()
    )

##
### flatmates
##

@app.route('/new/flatmate')
def new_flatmates():
    """Renders a form page to add flatmates.
    """
    return render_template('add_flatmates.html',
        flatmates = db.session.query(Flatmate).order_by(Flatmate.name).all()
    )


@app.route('/new/flatmate/add', methods=['POST'])
def add_flatmates():
    """"""
    names = request.form['flatmates'].split()
    db.session.add_all(Flatmate(name=name.lower()) for name in names)
    db.session.commit()
    return redirect(url_for('index'))

##
### deliveries
##

@app.route('/delivery/<int:delivery_id>/')
def display_delivery(delivery_id):
    """Renders a page with:
    - list of flatmates and their individual contribution to the bill
    - list of purchases and the assigned flatmates next to each purchase
    - link to form page to re-assign
    """
    baskets = None
    if api.is_delivery_assigned(delivery_id):
        baskets = api.get_contributions(delivery_id)

    purchases = db.session.query(Purchase).filter_by(delivery_id=delivery_id).all()
    purchases = [(p, api.get_purchasers(p.id)) for p in purchases]

    return render_template('display_delivery.html',
        delivery  = db.session.query(Delivery).filter_by(id=delivery_id).one(),
        baskets   = baskets,
        purchases = purchases
    )


@app.route('/new/delivery')
def paste_receipt(default=True):
    """Renders a form page to paste the receipt text into.
    """
    if default:
        with open('tests/dummy_receipt.txt', 'rU') as ifile:
            default_shop = ifile.read()
    else:
        default_shop = ''

    return render_template('paste_receipt.html',
        default_shop = default_shop
    )


@app.route('/new/delivery/parse', methods=['POST'])
def process_receipt():
    """Processes the receipt and redirects to the appropriate next step.
    """
    receipt_text = request.form['receipt']
    delivery_id = api.process_input_delivery(receipt_text)

    assigned = api.is_delivery_assigned(delivery_id)
    if assigned:
        return redirect(url_for('display_delivery',
            delivery_id = delivery_id
        ))
    else:
        return redirect(url_for('assign_delivery',
            delivery_id = delivery_id
        ))


@app.route('/delivery/<int:delivery_id>/assign')
def assign_delivery(delivery_id):
    """Renders a form page with a list of purchases and flatmate names 
    next to each purchase to click and assign.
    """
    purchases = db.session.query(Purchase).filter_by(delivery_id=delivery_id).all()

    assigned_purchases = []
    for p in purchases:
        purchasers = list(chain(*db.session.query(Assignment.flatmate_id).filter_by(purchase_id=p.id).all()))
        if p.description == 'Delivery costs' and not purchasers:
            purchasers = list(chain(*db.session.query(Flatmate.id).all()))

        assigned_purchases.append((p, purchasers))

    return render_template('assign_delivery.html',
        delivery_id = delivery_id,
        purchases = assigned_purchases,
        flatmates = db.session.query(Flatmate).order_by(Flatmate.name).all()
    )


@app.route('/delivery/<int:delivery_id>/assigning', methods=['POST'])
def add_assignments(delivery_id):
    """"""
    purchases = db.session.query(Purchase).filter_by(delivery_id=delivery_id).all()

    ## delete everything that had been assigned before for this delivery
    for purchase in purchases:
        assignments = db.session.query(Assignment).filter_by(purchase_id=purchase.id).all()
        for fp in assignments:
            db.session.delete(fp)

    ## (re-)assign
    for purchase in purchases:
        purchasers = request.form.getlist(str(purchase.id))
        for name in purchasers:
            flatmate = db.session.query(Flatmate).filter_by(name=name).one()

            db.session.add(Assignment(
                purchase_id = purchase.id,
                flatmate_id = flatmate.id
            ))
            db.session.commit()

    return redirect(url_for('display_delivery',
        delivery_id = delivery_id
    ))


###
### controllers: other
###


@app.route('/style.css')
def css():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'css/style.css')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404