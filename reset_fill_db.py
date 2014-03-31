#!venv/bin/python

#this script populates the database with some items (for testing purposes)

from app import db, models
import datetime

#clear the database
db.engine.execute('SET FOREIGN_KEY_CHECKS = 0')
db.drop_all()
db.engine.execute('SET FOREIGN_KEY_CHECKS = 1')
db.create_all()

#############################################
#borrower_type
#############################################
type_student = models.BorrowerType(type = 'student', bookTimeLimit = datetime.timedelta(weeks=2))
db.session.add(type_student)

type_faculty = models.BorrowerType(type = 'faculty', bookTimeLimit = datetime.timedelta(weeks=12))
db.session.add(type_faculty)

type_staff = models.BorrowerType(type = 'staff', bookTimeLimit = datetime.timedelta(weeks=6))
db.session.add(type_staff)

##############################################
#borrower
##############################################
borrower_b = models.Borrower(bid=111, password="abcd", name="Bill", address="India", phone="18005555555", emailAddress="bill@gmail.com", sinOrStNo="11112222", expiryDate=datetime.date(2014, 3, 31), type=type_student.type)
db.session.add(borrower_b)

#expired account, shouldn't be allowed to checkout stuff
borrower_c = models.Borrower(bid=222, password="efgh", name="Coco", address="China", phone="17781234567", emailAddress="blaah@mail.com", sinOrStNo="33334444", expiryDate=datetime.date(2014, 3, 25), type=type_faculty.type)
db.session.add(borrower_c)

borrower_d = models.Borrower(bid=333, password="ijkl", name="Doge", address="Coin", phone="18005555555", emailAddress="such@wow.com", sinOrStNo="55556666", expiryDate=datetime.date(2014, 5, 1), type=type_staff.type)
db.session.add(borrower_d)

##############################################
#book
##############################################
book_a = models.Book(callNumber="somecallnumber", isbn="someisbn", title="historyofstuff", mainAuthor="The Toj", publisher="somepublisher", year="2013")
db.session.add(book_a)

book_b = models.Book(callNumber="othercallnumber", isbn="otherisbn", title="somescifinovelwithalongtitle", mainAuthor="defaultauthor", publisher="defaultpublisher", year="1993")
db.session.add(book_b)

##############################################
#has_author
##############################################
hasauthor_a = models.HasAuthor(callNumber=book_a.callNumber, name="the other guy")
db.session.add(hasauthor_a)

hasauthor_a2 = models.HasAuthor(callNumber=book_a.callNumber, name="the second guy")
db.session.add(hasauthor_a2)

hasauthor_a3 = models.HasAuthor(callNumber=book_a.callNumber, name="elmo")
db.session.add(hasauthor_a3)

hasauthor_b = models.HasAuthor(callNumber=book_b.callNumber, name="bill nye the science guy")
db.session.add(hasauthor_b)

##############################################
#has_subject
##############################################
hassubject_a = models.HasSubject(callNumber=book_a.callNumber, subject="history")
db.session.add(hassubject_a)

hassubject_a2 = models.HasSubject(callNumber=book_a.callNumber, subject="story")
db.session.add(hassubject_a2)

##############################################
#book_copy
##############################################
bookcopy_aa = models.BookCopy(callNumber=book_a.callNumber, copyNo="1", status="in")
db.session.add(bookcopy_aa)

bookcopy_ab = models.BookCopy(callNumber=book_a.callNumber, copyNo="2", status="in")
db.session.add(bookcopy_ab)

bookcopy_ba = models.BookCopy(callNumber=book_b.callNumber, copyNo="1", status="out")
db.session.add(bookcopy_ba)

##############################################
#hold_request
##############################################
holdrequest_a = models.HoldRequest(hid=11, bid=borrower_b.bid, callNumber=book_b.callNumber, issuedDate=datetime.datetime.now())
db.session.add(holdrequest_a)

##############################################
#borrowing
##############################################
borrowing_a = models.Borrowing(borid=22, bid=borrower_b.bid, callNumber=bookcopy_ba.callNumber, copyNo=bookcopy_ba.copyNo, outDate=datetime.datetime(year=2013, month=1, day=1))
db.session.add(borrowing_a)

borrowing_b = models.Borrowing(borid=33, bid=borrower_b.bid, callNumber=bookcopy_aa.callNumber, copyNo=bookcopy_aa.copyNo, outDate=datetime.datetime.now(), inDate=datetime.datetime.now() + datetime.timedelta(days=10))
db.session.add(borrowing_b)

##############################################
#fine
##############################################
#woah, over 2000 dollars in fines
fine_a = models.Fine(fid=123, amount=2852.12, issuedDate=datetime.datetime.now(), borid=borrowing_a.borid)
db.session.add(fine_a)

db.session.commit()

