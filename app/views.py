from flask import render_template, request, flash, Markup
from app import app, db
import datetime
import csv

user = 111


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

        #TODO: search parameters should stay in text boxes after post because
        #it is more user friendly
        #TODO: tony: I can do that from the client side?
        qtitle = request.form['title']
        qsubject = request.form['subject']
        qauthor = request.form['author']

        if qtitle == "" and qsubject == "" and qauthor == "":
            message = Markup('Bad search: <a href="#" class="alert-link">you must complete at least one field</a>.')
            flash(message, 'error')
        else:
            query = """select distinct b.callNumber
                        from book as b, has_subject as s, has_author as a
                        where """
            if qtitle != "":
                query += "b.title like '%%{}%%' and ".format(qtitle)
            if qsubject != "":
                query += """b.callNumber=s.callNumber and s.subject like
                '%%{}%%' and """.format(qsubject)
            if qauthor != "":
                query += "(b.mainAuthor like '%%{}%%' or ".format(qauthor)
                query += """(b.callNumber=a.callNumber and a.name like
                '%%{}%%')) and """.format(qauthor)
            query = query[0:-4]

            qresults = db.engine.execute(query).fetchall()

            if len(qresults) == 0:
                message = Markup('''No items in the collection match the search
                                 parameters.''')
                flash(message, 'warning')
            else:
                results = []
                #TODO: test this with lots of subjects and authors, see if the
                #tables look okay
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
                           results=results
                           )


@app.route('/checkout')
def checkout():
    qbid = request.form['borrowerId']
    qcallNumber = request.form['callNumber']
    qcopyNo = request.form['copyNo']

    if qbid == "" or qcallNumber == "" or qcopyNo == "":
        message = Markup('Please fill in all fields.')
        flash(message, 'warning')
    else:
        query = """select
                    from borrower
                    where bid='{}'""".format(borrowerID)
        qresult = db.engine.execute(query).first()
        if len(qresult) == 0:
            message = Markup('Borrower does not exist.')
            flash(message, 'warning')
        else:
            query = """select status
                        from book_copy as bc
                        where bc.callNumber ='{0}' and
                        bc.copyNo='{1}'""".format(qcallNumber,qcopyNo)
            qresult = db.engine.execute(query).first()
            if qresult == "on-hold":
                message = Markup('Copy is on hold.')
                flash(message, 'warning')
            elif qresult == "out":
                message = Markup('Copy has been taken out.')
                flash(message, 'warning')
            else:
                query = """update book_copy
                            set status='out'
                            where callNumber='{0}' and
                            copyNo='{1}'""".format(qcallNumber,qcopyNo)
                qresult = db.engine.execute(query)
                #query = """


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


@app.route('/item/new', methods = ['GET', 'POST'])
def itemNew():
    results = None
    err = False
    if request.method == 'POST':
        qcallNumber = request.form['callNumber']
        qisbn = request.form['isbn'].replace("-", "")
        qtitle = request.form['title']
        qmainAuthor = request.form['mainAuthor']
        qpublisher = request.form['publisher']
        qyear = request.form['year']
        if (
            qcallNumber == "" or
            qisbn == "" or
            qtitle == "" or
            qmainAuthor == "" or
            qpublisher == "" or
            qyear == ""
            ):
            message = Markup('All fields must be completed.')
            flash(message, 'warning')
        else:
            query = """SELECT B.callNumber
                        FROM Book B
                        WHERE B.callNumber='{}'""".format(qcallNumber)
            qresults = db.engine.execute(query).fetchall()
            if len(qresults) > 0:
                query = """SELECT MAX(copyNo)
                            FROM Book_Copy C
                            WHERE C.callNumber = '{}'""".format(qcallNumber)
                qresults = db.engine.execute(query).fetchall()
                for row in qresults:
                    qcopyNo = int(row[0]) + 1
                query = """INSERT INTO Book_Copy (callNumber, copyNo, status) VALUES """
                query += """('{0}','{1}','{2}')""".format(
                    qcallNumber,
                    qcopyNo,
                    'in')
                qresult = db.engine.execute(query)
                message = Markup('This book already exists, adding as copy')
                flash(message, 'warning')
            else:
                query = """INSERT INTO Book (callNumber, isbn, title, mainAuthor, publisher, year) VALUES """
                query += """('{0}','{1}','{2}','{3}','{4}','{5}')""".format(
                    qcallNumber,
                    qisbn,
                    qtitle,
                    qmainAuthor,
                    qpublisher,
                    qyear)
                qresult = db.engine.execute(query)
                message = Markup('You added an item. Query is: ' + query)
                flash(message, 'success')

                qcopyNo = 1
                query = """INSERT INTO Book_Copy (callNumber, copyNo, status) VALUES """
                query += """('{0}','{1}','{2}')""".format(
                    qcallNumber,
                    qcopyNo,
                    'in')
                qresult = db.engine.execute(query)
                message = Markup('Adding as copy: ' + query)
                flash(message, 'warning')

                if request.form['otherAuthor'] != "":
                    qotherAuthors = []
                    qotherAuthors.append(qmainAuthor)
                    for row in csv.reader([request.form['otherAuthor']]):
                        for value in row:
                            qotherAuthors.append(value.strip())
                    for author in qotherAuthors:
                        query1 = """INSERT INTO Has_Author (callNumber, name) VALUES """
                        query1 += """('{0}','{1}')""".format(
                            qcallNumber,
                            author)
                        message = Markup('You added multiple authors: ' + query1)
                        flash(message, 'success')
                        qresult = db.engine.execute(query1)

                if request.form['subjects'] != "":
                    qsubjects = []
                    for row in csv.reader([request.form['subjects']]):
                        for value in row:
                            qsubjects.append(value.strip())
                    for subject in qsubjects:
                        query2 = """INSERT INTO Has_Subject (callNumber, subject) VALUES """
                        query2 += """('{0}','{1}')""".format(
                            qcallNumber,
                            subject)
                        message = Markup('You added multiple subjects: ' + query2)
                        flash(message, 'success')
                        qresult = db.engine.execute(query2)

    return render_template('admin/new.html',
                           title='New Item',
                           user=user,
                           results = results
                           )
#@app.route('/item/add')
#@app.route('/item/:item/hold')
#@app.route('/item/:item/checkout')
#@app.route('/item/:item/return')


@app.route('/borrower/new', methods=['POST', 'GET'])
def borrowerNew():
    results = None
    err = False

    if request.method == 'POST':
        title = 'New Borrower Account'
        #print request.form

        qname = request.form['name']
        qemail = request.form['email']
        qpassword = request.form['password']
        qpasswordConfirm = request.form['passwordConfirm']
        qaddress = request.form['address']
        qphoneNumber = request.form['phoneNumber']
        qsinOrSid = request.form['sinOrSid']
        qtype = request.form['type']
        qexpiryDate = datetime.datetime.now() + datetime.timedelta(days=365)

        if (
            qname == "" or
            qemail == "" or
            qpassword == "" or
            qpasswordConfirm == "" or
            qaddress == "" or
            qphoneNumber == "" or
            qsinOrSid == "" or
            qtype == ""
        ):
            message = Markup('All fields must be completed.')
            flash(message, 'warning')
        else:
            query = """select distinct b.sinOrStNo
                        from borrower as b
                        where b.sinOrstNo='{}'""".format(qsinOrSid)
            qresults = db.engine.execute(query).fetchall()
            if len(qresults) > 0:
                message = Markup('This SIN or student number already exists')
                flash(message, 'warning')
            elif qpassword != qpasswordConfirm:
                message = Markup('Make sure both passwords match')
                flash(message, 'warning')
            else:
                query = """insert into borrower(password, name, address, phone,
                emailAddress, sinOrStNo, expiryDate, type) values"""
                query += """('
                {0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}
                ')""".format(qpassword,
                             qname,
                             qaddress,
                             qphoneNumber,
                             qemail,
                             qsinOrSid,
                             qexpiryDate,
                             qtype)
                qresult = db.engine.execute(query)
    else:
        title = 'New Borrower Account'

    return render_template('borrower/new.html',
                           title=title,
                           user=user,
                           results=results
                           )


#@app.route('/borrower/add')
@app.route('/borrower/<int:borrower_id>')
def borrowerAccount(borrower_id):
    overdue = 0
    borrowerInfo = None
    borrowedItems = None
    fines = []
    holdRequests = None
    query = """select *
                from borrower
                where bid='{}'""".format(borrower_id)
    qresults = db.engine.execute(query).first()
    if qresults is None:
        message = Markup('No borrower exists with this borrower_id.')
        flash(message, 'error')
    else:
        borrowerInfo = qresults

        borrowedItems = []
        query = """select borid, c.callNumber as cn, title, mainAuthor, outDate
                    from borrowing as b, book as c
                    where b.callNumber=c.callNumber
                    and bid='{}'
                    and inDate is NULL""".format(borrower_id)
        qresults = db.engine.execute(query).fetchall()
        typeQuery = """select bookTimeLimit
                        from borrower as b, borrower_type as t
                        where bid='{}' and b.type=t.type""".format(borrower_id)
        timeLimit = db.engine.execute(typeQuery).first()
        for result in qresults:
            borrowedItem = {}
            borrowedItem['borid'] = result.borid
            borrowedItem['callNumber'] = result.cn
            borrowedItem['title'] = result.title
            borrowedItem['mainAuthor'] = result.mainAuthor
            borrowedItem['outDate'] = result.outDate
            borrowedItem['expiryDate'] = (result.outDate +
                                          (timeLimit.bookTimeLimit -
                                           datetime.datetime(year=1970,
                                                             month=1,
                                                             day=1)
                                           )
                                          )
            if borrowedItem['expiryDate'] > datetime.datetime.now():
                borrowedItem['expired'] = False
            else:
                borrowedItem['expired'] = True
                overdue += 1
            borrowedItems.append(borrowedItem)
        if overdue > 0:
            message = Markup('''You have <a href="#overdue"
                             class="alert-link">{} overdue</a>
                             item(s).'''.format(overdue))
            flash(message, 'warning')

        query = """select hid, h.callNumber, title, issuedDate from
        hold_request as h, book as b where bid='{}' and
        b.callNumber=h.callNumber""".format(borrower_id)
        qresults = db.engine.execute(query).fetchall()
        holdRequests = []
        for result in qresults:
            hr = {}
            hr['hid'] = result.hid
            hr['callNumber'] = result.callNumber
            hr['title'] = result.title
            hr['issuedDate'] = result.issuedDate
            holdRequests.append(hr)

        query = """select fid, amount, issuedDate
                    from fine as f, borrowing as b
                    where f.borid=b.borid and b.bid='{}'
                    and paidDate is NULL""".format(borrower_id)
        qresults = db.engine.execute(query).fetchall()
        if len(qresults) > 0:
            message = Markup('''You have <a href="#fines"
                             class="alert-link">outstanding</a> fines.''')
            flash(message, 'warning')
            for result in qresults:
                fine = {}
                fine['fid'] = result.fid
                fine['amount'] = result.amount
                fine['issuedDate'] = result.issuedDate
                fines.append(fine)

    return render_template('borrower/account.html',
                           title='Account Information',
                           user=user,
                           borrower=borrowerInfo,
                           borrowedItems=borrowedItems,
                           holdRequests=holdRequests,
                           fines=fines
                           )

#TODO: hold urls should map to:
#/hold/borrower_id/remove and
#/hold/borrower_id/new
#@app.route('/borrower/<int:borrower_id>/holdcancel', methods=['POST'])
@app.route('/borrower/<int:borrower_id>/holdrequest', methods=['POST', 'GET'])
def placeHoldRequest(borrower_id):
    if request.method == 'POST':
        #check if call number is valid
        #check if a copy of the book is available
        #place hold request
        callNumber = request.form['callNumber']
        query = """select title
                    from book
                    where callNumber='{}'""".format(callNumber)
        qresult = db.engine.execute(query).first()
        if qresult is None: #Invalid call number
            message = Markup('The call number "{}" is not associated with a book.'.format(callNumber))
            flash(message, 'error')
        else:
            title = qresult.title
            query = """select *
                        from book_copy
                        where status='in' and callNumber='{}'""".format(callNumber)
            qresult = db.engine.execute(query).fetchall()
            if len(qresult) == 0:
                query = """select *
                            from hold_request
                            where bid='{0}' and callNumber='{1}'""".format(borrower_id,
                                                                            callNumber)
                qresult=db.engine.execute(query).first()
                if qresult is None:
                    query = """insert into hold_request (bid, callNumber)
                                VALUES ('{0}', '{1}')""".format(borrower_id,
                                                                callNumber)
                    db.engine.execute(query)
                    message = Markup('Hold request placed for the book "{}".'.format(title))
                    flash(message, 'success')
                else:
                    message = Markup('Hold request not placed. You have already placed a hold request on the book "{}".'.format(title))
                    flash(message, 'warning')
            else:
                message = Markup('Hold request not placed. A copy of the book "{}" is available.'.format(title))
                flash(message, 'warning')
    return render_template('borrower/holdrequest.html',
                            title='Place Hold Request',
                            user=user
                            )

@app.route('/borrower/<int:borrower_id>/fines', methods=['POST', 'GET'])
def payFines(borrower_id):
    if request.method == 'POST':
        query = ""
        for key in request.form:
            query = """update fine
                        set paidDate='{0}'
                        where fid='{1}'""".format(datetime.datetime.now(), key)
            break
        db.engine.execute(query)
        message = Markup('You have paid a fine.')
        flash(message, 'success')
    fines = None
    query = """select fid, amount, issuedDate
                from fine as f, borrowing as b
                where f.borid=b.borid and b.bid='{}'
                and paidDate is NULL""".format(borrower_id)
    qresults = db.engine.execute(query).fetchall()
    if len(qresults) == 0:
        message = Markup('You have no outstanding fines.')
        flash(message, 'warning')
    else:
        fines = []
        for result in qresults:
            fine = {}
            fine['fid'] = result.fid
            fine['amount'] = result.amount
            fine['issuedDate'] = result.issuedDate
            fines.append(fine)
    return render_template('borrower/fines.html',
                           title='Pay Fines',
                           user=user,
                           fines=fines
                           )

#checkedout, popular
@app.route('/report/checkedout', methods=['GET', 'POST'])
def reportCheckedout():
    booksout = None
    qresults = None
    subject = None
    if request.method == 'POST':
        qsubjects = []
        for row in csv.reader([request.form['subjects']]):
            for value in row:
                qsubjects.append(value.strip())
        if len(qsubjects) > 1:
            message = Markup('Put only 1 subject')
            flash(message, 'warning')
        else:
            subject = request.form['subjects']
            query = """SELECT *,B.callNumber as BCallNumber,C.copyNo as CCopyNo
                        FROM Book_Copy C, Borrowing R, Book B
                        WHERE C.status = 'out' AND C.callNumber = R.callNumber AND C.copyNo = R.copyNo AND B.callNumber = C.callNumber AND EXISTS (SELECT *
                                        FROM Book B, Has_Subject S
                                        WHERE B.callNumber = S.callNumber AND S.subject = '""" + subject + """' AND C.callNumber = B.callNumber)
                        ORDER BY C.callNumber"""
            qresults = db.engine.execute(query).fetchall()
    else:
        query = """SELECT *,B.callNumber as BCallNumber,C.copyNo as CCopyNo
                    FROM Book_Copy C, Borrowing R, Book B
                    WHERE C.status = 'out' AND C.callNumber = R.callNumber AND C.copyNo = R.copyNo AND B.callNumber = C.callNumber
                    ORDER BY C.callNumber"""
        qresults = db.engine.execute(query).fetchall()
    if qresults == None:
        message = Markup('Bad search')
        flash(message, 'warning')
    elif len(qresults) == 0:
        message = Markup('LOL NO BOOKS OUT')
        flash(message, 'warning')
    else:
        booksout = []
        for result in qresults:
            book = {}
            book['callNumber'] = result.BCallNumber
            book['copyNo'] = result.CCopyNo
            book['title'] = result.title
            book['bid'] = result.bid
            book['outDate'] = result.outDate

            typeQuery = """select bookTimeLimit
                        from borrower as b, borrower_type as t
                        where bid='{}' and b.type=t.type""".format(result.bid)
            timeLimit = db.engine.execute(typeQuery).first()

            book['dueDate'] = result.outDate + (timeLimit.bookTimeLimit - datetime.datetime(year=1970, month=1, day=1))

            book['inDate'] = result.inDate

            if datetime.datetime.now() > book['dueDate'] and book['inDate'] is None:
                book['overdue'] = 'Yes'
            else:
                book['overdue'] = 'No'
            booksout.append(book)

    return render_template('admin/reportcheckedout.html',
                           title='Checked Out Report',
                           user=user,
                           booksout=booksout,
                           subject=subject
                           )

@app.route('/report/popular', methods=['GET', 'POST'])
def reportPopular():
    topResults = []
    limit = None
    year = None
    rank = 0
    if request.method == 'POST':
        limit = request.form['limit']
        year = request.form['year']
        if limit == "" or year == "":
            message = Markup('Put a Limit and Year')
            flash(message, 'warning')
        else:
            query = """SELECT B.callNumber,COUNT(R.callNumber) AS numcheout,B.title,outDate
                        FROM Borrowing R, Book B
                        WHERE R.callNumber = B.callNumber AND YEAR(outDate) = """ + year + """
                        GROUP BY R.callNumber
                        ORDER BY numcheout DESC
                        LIMIT """ + limit
            qresults = db.engine.execute(query).fetchall()
            for result in qresults:
                topResult = {}
                rank = rank + 1
                topResult['rank'] = rank
                topResult['callNumber'] = result.callNumber
                topResult['title'] = result.title
                topResult['times'] = result.numcheout
                topResults.append(topResult)
    else:
        message = Markup('Put a Limit and Year')
        flash(message, 'warning')
    return render_template('admin/reportpopular.html',
                           title='Popular Books Report',
                           user=user,
                           topResults=topResults,
                           limit=limit,
                           year=year
                           )
