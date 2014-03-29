from flask import render_template, request, flash, Markup
from app import app, db, models

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
    err = False
    if request.method == 'POST':
        title = 'Search Results'
        
        #TODO: search parameters should stay in text boxes after post because it is more user friendly
        qtitle = request.form['title']
        qsubject = request.form['subject']
        qauthor = request.form['author']

        if qtitle == "" and qsubject == "" and qauthor == "":
            err = True
        else:
            query = """select distinct b.callNumber
                        from book as b, has_subject as s, has_author as a
                        where """
            if qtitle != "":
                query += "b.title like '%%{}%%' and ".format(qtitle)
            if qsubject != "":
                query += "b.callNumber=s.callNumber and s.subject like '%%{}%%' and ".format(qsubject)
            if qauthor != "":
                query += "(b.mainAuthor like '%%{}%%' or ".format(qauthor)
                query += "(b.callNumber=a.callNumber and a.name like '%%{}%%')) and ".format(qauthor)
            query = query[0:-4]
    #        return query

            qresults = db.engine.execute(query).fetchall()
         
            if len(qresults) == 0:
                message = Markup('No items in the collection match the search parameters.')
                flash(message, 'warning')
            else:
                results = []
                #TODO: test this with lots of subjects and authors, see if the tables look okay
                for callNumber in qresults:
                    result = {}

                    callNumber = callNumber[0]
                    query = """select *
                                from book
                                where callNumber='{}'""".format(callNumber)
                    qresult = db.engine.execute(query).first()
                    result['callNumber'] = qresult.callNumber
                    result['title'] = qresult.title
                    result['mainAuthor'] = qresult.mainAuthor
                    result['year'] = qresult.year
                    
                    query = """select name
                                from has_author
                                where callNumber='{}'""".format(callNumber)
                    qresult = db.engine.execute(query).fetchall()
                    result['authors'] = ""
                    for r in qresult:
                        result['authors'] += str(r[0]) + ', '
                    result['authors'] = result['authors'][0:-2]
                    
                    query = """select subject
                                from has_subject
                                where callNumber='{}'""".format(callNumber)
                    qresult = db.engine.execute(query).fetchall()
                    result['subjects'] = ""
                    for r in qresult:
                        result['subjects'] += str(r[0]) + ', '
                    result['subjects'] = result['subjects'][0:-2]
                    
                    query = """select status
                                from book_copy
                                where callNumber='{}'""".format(callNumber)
                    qresult = db.engine.execute(query).fetchall()
                    result['in'] = 0
                    result['out'] = 0
                    result['on-hold'] = 0
                    for r in qresult:
                        result[r[0]] += 1

                    results.append(result)
    else:
        title = 'Search'

    return render_template('search.html',
                           title=title,
                           user=user,
                           results=results,
                           error=err
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
