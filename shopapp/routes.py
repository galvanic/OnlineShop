
from shopapp import app
from flask import render_template,\
                  send_from_directory,\
                  request,\
                  redirect,\
                  url_for

from onlineshop import get_orders,\
                       get_flatmate_names

from collections import namedtuple
Order = namedtuple('Order', 'id, delivery_date')


###
### Database stuff
###


import sqlite3
from flask import g

DB_FILE = '/Users/jc5809/Dropbox/Programming/Projects/OnlineShop/data/onlineshop.db'

def connect_to_database():
    return sqlite3.connect(DB_FILE)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_to_database()
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


###
### controllers: other
###


@app.route('/style.css')
def css():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'css/style.css')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


###
### controllers: main pages
###


@app.route('/')
@app.route('/index')
def index():
    """Renders the landing page with:
    - list of flatmates
    - list of previous orders (just the delivery date)
    - button to form page to add flatmate(s)
    - button to form page to add order
    """
    orders = [Order(o_id, delivery_date) for o_id, delivery_date in get_orders(get_db())]

    return render_template('index.html',
        flatmates = get_flatmate_names(get_db()),
        orders    = orders
    )


@app.route('/order/<int:order_id>/', methods=['POST'])
def display_order(order_id):
    """Renders a page with:
    - list of flatmates and their individual contribution to the bill
    - list of purchases and the assigned flatmates next to each purchase
    - button to form page to re-assign
    """

    return render_template('display_order.html',
        purchases = purchases
    )


@app.route('/new/flatmate')
def add_flatmates():
    """Renders a form page to add flatmates.
    """
    return render_template('add_flatmates.html')


@app.route('/new/order')
def paste_receipt(default=True):
    """Renders a form page to paste the receipt text into.
    """
    if default:
        with open('../tests/dummy_receipt.txt', 'rU') as ifile:
            default_shop = ifile.read()
    else:
        default_shop = ''

    return render_template('paste_receipt.html',
        default_shop = default_shop
    )


@app.route('/order/<int:order_id>/parse', methods=['POST'])
def parse_receipt(order_id):
    """Parses the receipt and redirects to the appropriate next step.
    """
    # parse
    receipt_text = request.forms['receipt']

    # check if order exists already using the delivery date
    # if so, check if already assigned
    # if exists and all purchases are assigned, redirect to the order page
    return redirect(url_for('display_order',
        order_id = order_id
    ))

    # if not, generate a new order id and redirect to the assignment page
    return redirect(url_for('assign_order',
        order_id = generate_new_order_id()
    ))


@app.route('/order/<int:order_id>/assign', methods=['POST'])
def assign_order(order_id):
    """Renders a form page with a list of purchases and flatmate names 
    next to each purchase to click and assign.
    """

    return render_template('assign_order.html',
        purchases = purchases,
        flatmates = flatmates
    )


@app.route('/order/<int:order_id>/calculate', methods=['POST'])
def divide_bill(order_id):
    """Calculates each flatmate's individual contribution to the bill
    and redirects to the order page to summarise.
    """

    return redirect(url_for('display_order',
        order_id = order_id
    ))