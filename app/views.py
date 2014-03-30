from flask import render_template, request, flash, Markup
from app import app, db
import datetime

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


@app.route('/checkout', methods=['POST', 'GET'])
def checkout():
    if request.method == 'POST':
        qbid = request.form['borrowerId']
        qcallNumber = request.form['callNumber']
        qcopyNo = request.form['copyNo']
        qoutDate = datetime.datetime.now()
        qinDate = datetime.datetime.now() + datetime.timedelta(days=14)
        
        if (
            qbid == "" or 
            qcallNumber == "" or 
            qcopyNo == ""
        ):
            message = Markup('Please fill in all fields.')
            flash(message, 'error')
        else:
            query = """select *
                        from borrower
                        where bid='{}'""".format(qbid)
            qresult = db.engine.execute(query).first()
            if qresult == None:
                message = Markup('Borrower does not exist.')
                flash(message, 'error')
            else:
                query = """select status
                            from book_copy
                            where callNumber ='{0}' and 
                            copyNo='{1}'""".format(qcallNumber,qcopyNo)
                qresult = db.engine.execute(query).first()
                if qresult.status == "on-hold":
                    message = Markup('Copy is on hold.')
                    flash(message, 'warning')
                elif qresult.status == "out":
                    message = Markup('Copy has been taken out.')
                    flash(message, 'warning')
                else:
                    query = """update book_copy
                                set status='out'
                                where callNumber='{0}' and
                                copyNo='{1}'""".format(qcallNumber,qcopyNo)
                    qresult = db.engine.execute(query)
                    
                    query = """insert into borrowing(bid, callNumber, copyNo, outDate) values"""
                    query += """('{0}','{1}','{2}','{3}')""".format(qbid,
                                 qcallNumber,   
                                 qcopyNo,
                                 qoutDate)
                    qresult = db.engine.execute(query)
                    
                    result = {}
                    query = """select title
                                from book
                                where callNumber='{}'""".format(qcallNumber)
                    qresult = db.engine.execute(query).first()
                    result['title'] = qresult
                    result['callNumber'] = qcallNumber
                    result['dueDate'] = qinDate
            
    return render_template('admin/checkout.html',
                           title='Checkout Items',
                           user=user
                           )


@app.route('/returns', methods=['POST', 'GET'])
def returns():
    if request.method == 'POST':
        qcallNumber = request.form['callNumber']
        qcopyNo = request.form['copyNo']
        qinDate = datetime.datetime.now()
        
        if (
            qcallNumber == "" or
            qcopyNo == ""
        ):
            message = Markup('All fields must be completed.')
            flash(message, 'error')
        else:
            query = """update borrowing
                        set inDate='{0}'
                        where callNumber='{1}' and
                        copyNo='{2}'""".format(qinDate,qcallNumber,qcopyNo)
            qresults = db.engine.execute(query)
            query = """select outDate
                        from borrowing
                        where callNumber='{0}' and
                        copyNo='{1}'""".format(qcallNumber,qcopyNo)
            qresults = db.engine.execute(query).first()
            
            #if late, assign fine
            if qinDate > (qresults.outDate + datetime.timedelta(days=14)) :
                query = """select borid 
                            from borrowing
                            where callNumber='{0}' and
                            copyNo='{1}'""".format(qcallNumber,qcopyNo)
                qresults = db.engine.execute(query).first()
                query = """insert into fine(amount, issuedDate, borid) 
                            values"""
                query += """('
                {0}','{1}','{2}
                ')""".format(5.00,
                             qinDate,
                             qresults.borid)
                qresult = db.engine.execute(query)
                message = Markup('Late return, a fee was assigned.')
                flash(message, 'warning')
            
            #if there are no holds, set book status in, otherwise notify holdee
            query = """select *
                        from hold_request
                        where callNumber='{}'""".format(qcallNumber)
            qresults = db.engine.execute(query).fetchall()
            if len(qresults) == 0:
                query = """update book_copy
                            set status='in'
                            where callNumber='{0}' and
                            copyNo='{1}'""".format(qcallNumber, qcopyNo)
                qresults = db.engine.execute(query)
                message = Markup('Item successfully returned and processed.')
                flash(message, 'message')
            else:
                query = """update book_copy
                            set status='on-hold'
                            where callNumber='{0}' and
                            copyNo='{1}'""".format(qcallNumber, qcopyNo)
                qresults = db.engine.execute(query)
                message = Markup('Item on hold, notifying holdee.')
                flash(message, 'warning')
                query = """select bid
                            from hold_request
                            where callNumber='{}'""".format(qcallNumber)
                qresult = db.engine.execute(query).first()
                query = """select emailAddress
                            from borrower
                            where bid='{}'""".format(qresult)
                qresult = db.engine.execute(query).first()
                #notify holdee by sending email to qresult
                

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
            flash(message, 'error')
        else:
            query = """select distinct b.sinOrStNo
                        from borrower as b
                        where b.sinOrstNo='{}'""".format(qsinOrSid)
            qresults = db.engine.execute(query).fetchall()
            if len(qresults) > 0:
                message = Markup('This SIN or student number already exists')
                flash(message, 'error')
            elif qpassword != qpasswordConfirm:
                message = Markup('Make sure both passwords match')
                flash(message, 'error')
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
                message = Markup('New borrower added!')
                flash(message, 'message')
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
        flash(message, 'warning')
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

##overdue, checkedout, popular
#@app.route('/report/:report')
