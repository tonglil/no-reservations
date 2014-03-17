from flask import render_template, request
from app import app

user = 12


@app.route('/')
def index():
    return render_template('index.html',
                           title='Home',
                           user=user
                           )


@app.route('/search', methods=['GET'])
def search():
    return render_template('search.html',
                           title='Search',
                           user=user
                           )


@app.route('/search', methods=['POST'])
def results():
    return render_template('results.html',
                           title='Search Results',
                           user=user
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



@app.route('/borrower/new')
def borrowerNew():
    return render_template('borrower/new.html',
                           title='New Borrower Account',
                           user=user
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
