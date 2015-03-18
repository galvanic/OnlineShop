
from shopapp import app
from flask import render_template,\
                  send_from_directory,\
                  request,\
                  redirect,\
                  url_for

import onlineshop as api

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
    return render_template('index.html',
        flatmates = api.get_flatmate_names(),
        orders    = api.get_orders()
    )


@app.route('/order/<int:order_id>/')
def display_order(order_id):
    """Renders a page with:
    - list of flatmates and their individual contribution to the bill
    - list of purchases and the assigned flatmates next to each purchase
    - link to form page to re-assign
    """
    if api.is_order_assigned:
        baskets = api.get_order_baskets(order_id)

    purchases = api.get_order_purchases(order_id)
    purchases = [(p, api.get_purchasers(p['id'])) for p in purchases]

    return render_template('display_order.html',
        order     = api.get_order(order_id),
        purchases = purchases,
        baskets   = None
    )


@app.route('/new/flatmate')
def new_flatmates():
    """Renders a form page to add flatmates.
    """
    existing_flatmates = api.get_flatmate_names()
    return render_template('add_flatmates.html',
        flatmates = existing_flatmates
    )


@app.route('/new/flatmate/add', methods=['POST'])
def add_flatmates():
    """"""
    names = request.form['flatmates'].split()
    for name in names:
        api.add_new_flatmate(name)
    return redirect(url_for('index'))


@app.route('/new/order')
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

@app.route('/new/order/parse', methods=['POST'])
def parse_receipt():
    """Parses the receipt and redirects to the appropriate next step.
    """
    receipt_text = request.form['receipt']
    order_id = api.process_input_order(receipt_text)

    assigned = api.is_order_assigned(order_id)
    if assigned:
        return redirect(url_for('display_order',
            order_id = order_id
        ))
    else:
        return redirect(url_for('assign_order',
            order_id = order_id
        ))


@app.route('/order/<int:order_id>/assign')
def assign_order(order_id):
    """Renders a form page with a list of purchases and flatmate names 
    next to each purchase to click and assign.
    """
    return render_template('assign_order.html',
        order_id  = order_id,
        purchases = api.get_order_purchases(order_id),
        flatmates = api.get_flatmate_names()
    )


@app.route('/order/<int:order_id>/assigning', methods=['POST'])
def add_basket_items(order_id):
    """"""
    purchase_ids = [p['id'] for p in api.get_order_purchases(order_id)]
    for p_id in purchase_ids:
        purchasers = request.form.getlist(str(p_id))
        for name in purchasers:
            f_id = api.get_flatmate_id(name)
            api.add_new_basket_item(p_id, f_id)

    return redirect(url_for('display_order',
        order_id = order_id
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