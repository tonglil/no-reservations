from flask import render_template, request, flash, Markup
from app import app

user = 12


@app.route('/')
def index():
    return render_template('index.html',
                           title='Home',
                           user=user
                           )


@app.route('/search', methods=['POST', 'GET'])
def results():
    results = None

    if request.method == 'POST':
        title = 'Search Results'
        print request.form

        message = Markup('''You have <a href="#overdue"
                        class="alert-link">overdue</a> items.''')
        flash(message, 'warning')
        message = Markup('''You have <a href="#outstanding"
                        class="alert-link">outstanding</a> fines.''')
        flash(message, 'warning')

        message = 'Item returned and processed.'
        flash(message, 'message')
        message = Markup('You have <a href="#overdue" class="alert-link">overdue</a> items.')
        flash(message, 'message')
    else:
        title = 'Search'

        message = 'Unable to add a new borrower.'
        flash(message, 'error')
        message = 'Another error.'
        flash(message, 'error')

    return render_template('search.html',
                           title=title,
                           user=user,
                           results=results
                           )


@app.route('/checkout')
def checkout():
    return render_template('admin/checkout.html',
                           title='Checkout Items',
                           user=user
                           )


@app.route('/returns')
def returns():
    return render_template('admin/returns.html',
                           title='Process Returns',
                           user=user
                           )



@app.route('/item/new')
def itemNew():
    return render_template('admin/new.html',
                           title='New Item',
                           user=user
                           )
#@app.route('/item/add')
#@app.route('/item/:item/hold')
#@app.route('/item/:item/checkout')
#@app.route('/item/:item/return')



@app.route('/borrower/new', methods=['POST', 'GET'])
def borrowerNew():
    results = None

    if request.method == 'POST':
        title = 'Search Results'
        print request.form
    else:
        title = 'Search'

    return render_template('borrower/new.html',
                           title='New Borrower Account',
                           user=user,
                           results=results
                           )


#@app.route('/borrower/add')
@app.route('/borrower/<int:borrower_id>')
def borrowerAccount(borrower_id):
    return render_template('borrower/account.html',
                           title='Account Information',
                           user=user
                           )
#@app.route('/borrower/:borrower/fines')



##overdue, checkedout, popular
#@app.route('/report/:report')
