from flask import render_template
from app import app

user = 'hi'
#user = None


@app.route('/style')
def style():
    return render_template('style.html',
                           title='Styles',
                           user=user
                           )


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
#@app.route('/checkout')
#@app.route('/returns')



#@app.route('/item/new')
#@app.route('/item/add')
#@app.route('/item/:item/hold')
#@app.route('/item/:item/checkout')
#@app.route('/item/:item/return')



#@app.route('/user/new')
#@app.route('/user/add')
#@app.route('/user/:user')
#@app.route('/user/:user/fines')



##overdue, checkedout, popular
#@app.route('/report/:report')
