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
type_student = models.BorrowerType(type='student',
                                   bookTimeLimit=datetime.timedelta(weeks=2))
db.session.add(type_student)

type_faculty = models.BorrowerType(type='faculty',
                                   bookTimeLimit=datetime.timedelta(weeks=12))
db.session.add(type_faculty)

type_staff = models.BorrowerType(type='staff',
                                 bookTimeLimit=datetime.timedelta(weeks=6))
db.session.add(type_staff)

##############################################
#borrower
##############################################
borrower_b = models.Borrower(bid=111,
                             password="abcd",
                             name="Bill Bennet",
                             address="India",
                             phone="18005555555",
                             emailAddress="bill@mail.com",
                             sinOrStNo="11112222",
                             expiryDate=datetime.date(2014, 3, 31),
                             type=type_student.type)
db.session.add(borrower_b)

#expired account, shouldn't be allowed to checkout stuff
borrower_c = models.Borrower(bid=222,
                             password="efgh",
                             name="Coco Carson",
                             address="China",
                             phone="17781234567",
                             emailAddress="coco@mail.com",
                             sinOrStNo="33334444",
                             expiryDate=datetime.date(2014, 3, 25),
                             type=type_faculty.type)
db.session.add(borrower_c)

borrower_d = models.Borrower(bid=333,
                             password="ijkl",
                             name="Doge",
                             address="Coin",
                             phone="18005555555",
                             emailAddress="such@wow.com",
                             sinOrStNo="55556666",
                             expiryDate=datetime.date(2014, 5, 1),
                             type=type_staff.type)
db.session.add(borrower_d)

##############################################
#book
##############################################
book_a = models.Book(callNumber="PQ2605.A37 E813 1989",
                     isbn="9780679720201",
                     title="The Stranger",
                     mainAuthor="Albert Camus",
                     publisher="Vintage International",
                     year="1989")
db.session.add(book_a)

book_b = models.Book(callNumber="PZ7.R79835 Hp 1997",
                     isbn="0747532699",
                     title="Harry Potter and the Philosopher's Stone",
                     mainAuthor="J.K. Rowling",
                     publisher="Bloomsbury",
                     year="1997")
db.session.add(book_b)

book_c = models.Book(callNumber="PZ7.R79835 Ht 1998a",
                     isbn="1551922444",
                     title="Harry Potter and the Chamber of Secrets",
                     mainAuthor="J.K. Rowling",
                     publisher="Bloomsbury",
                     year="1998")
db.session.add(book_c)

book_d = models.Book(callNumber="QH441.2 .M55 1996",
                     isbn="9780262133166",
                     title="An Introduction to Genetic Algorithms",
                     mainAuthor="Melanie Mitchell",
                     publisher="Mit Press",
                     year="1998")
db.session.add(book_d)

book_e = models.Book(callNumber="AI782.4 .O98 2008",
                     isbn="9780142412145",
                     title="Let It Snow",
                     mainAuthor="John Green",
                     publisher="Speak",
                     year="2008")
db.session.add(book_e)

##############################################
#has_author
##############################################
hasauthor_b = models.HasAuthor(callNumber=book_d.callNumber,
                               name="Bill Nye the Science Guy")
db.session.add(hasauthor_b)

hasauthor_a = models.HasAuthor(callNumber=book_e.callNumber,
                               name="Maureen Johnson")
db.session.add(hasauthor_a)

hasauthor_a2 = models.HasAuthor(callNumber=book_e.callNumber,
                                name="Lauren Myracle")
db.session.add(hasauthor_a2)

##############################################
#has_subject
##############################################
hassubject_a = models.HasSubject(callNumber=book_a.callNumber,
                                 subject="fiction")
db.session.add(hassubject_a)

hassubject_a2 = models.HasSubject(callNumber=book_a.callNumber,
                                  subject="existentialism")
db.session.add(hassubject_a2)

hassubject_b = models.HasSubject(callNumber=book_b.callNumber,
                                 subject="fiction")
db.session.add(hassubject_b)

hassubject_b2 = models.HasSubject(callNumber=book_b.callNumber,
                                  subject="fantasy")
db.session.add(hassubject_b2)

hassubject_c = models.HasSubject(callNumber=book_c.callNumber,
                                 subject="fiction")
db.session.add(hassubject_c)

hassubject_c2 = models.HasSubject(callNumber=book_c.callNumber,
                                  subject="fantasy")
db.session.add(hassubject_c2)

hassubject_d = models.HasSubject(callNumber=book_d.callNumber,
                                 subject="non-fiction")
db.session.add(hassubject_d)

hassubject_d2 = models.HasSubject(callNumber=book_d.callNumber,
                                  subject="algorithms")
db.session.add(hassubject_d2)

hassubject_e = models.HasSubject(callNumber=book_e.callNumber,
                                 subject="fiction")
db.session.add(hassubject_e)

hassubject_e2 = models.HasSubject(callNumber=book_e.callNumber,
                                  subject="young adult")
db.session.add(hassubject_e2)

##############################################
#book_copy
##############################################
bookcopy_aa = models.BookCopy(callNumber=book_a.callNumber,
                              copyNo="1",
                              status="out")
db.session.add(bookcopy_aa)

bookcopy_ab = models.BookCopy(callNumber=book_a.callNumber,
                              copyNo="2",
                              status="in")
db.session.add(bookcopy_ab)

bookcopy_ba = models.BookCopy(callNumber=book_b.callNumber,
                              copyNo="1",
                              status="out")
db.session.add(bookcopy_ba)

bookcopy_ca = models.BookCopy(callNumber=book_c.callNumber,
                              copyNo="1",
                              status="in")
db.session.add(bookcopy_ca)

bookcopy_da = models.BookCopy(callNumber=book_d.callNumber,
                              copyNo="1",
                              status="in")
db.session.add(bookcopy_da)

bookcopy_db = models.BookCopy(callNumber=book_d.callNumber,
                              copyNo="2",
                              status="in")
db.session.add(bookcopy_db)

bookcopy_ea = models.BookCopy(callNumber=book_e.callNumber,
                              copyNo="1",
                              status="out")
db.session.add(bookcopy_ea)

##############################################
#hold_request
##############################################
holdrequest_a = models.HoldRequest(hid=11,
                                   bid=borrower_b.bid,
                                   callNumber=book_b.callNumber)
db.session.add(holdrequest_a)

##############################################
#borrowing
##############################################
borrowing_a = models.Borrowing(borid=22,
                               bid=borrower_b.bid,
                               callNumber=bookcopy_ba.callNumber,
                               copyNo=bookcopy_ba.copyNo,
                               outDate=datetime.datetime(year=2013,
                                                         month=1,
                                                         day=1))
db.session.add(borrowing_a)

borrowing_b = models.Borrowing(borid=33,
                               bid=borrower_b.bid,
                               callNumber=bookcopy_aa.callNumber,
                               copyNo=bookcopy_aa.copyNo,
                               outDate=datetime.datetime.now(),
                               inDate=datetime.datetime.now() + datetime.timedelta(days=10))
db.session.add(borrowing_b)

##############################################
#fine
##############################################
#woah, over 2000 dollars in fines
fine_a = models.Fine(fid=123,
                     amount=2852.12,
                     issuedDate=datetime.datetime.now(),
                     borid=borrowing_a.borid)
db.session.add(fine_a)

fine_b = models.Fine(fid=456,
                     amount=852.12,
                     issuedDate=datetime.datetime.now(),
                     borid=borrowing_b.borid)
db.session.add(fine_b)

db.session.commit()
