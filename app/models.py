from app import db
from sqlalchemy.schema import ForeignKeyConstraint
from datetime import datetime


# Borrower *:1 BorrowerType
# HoldRequest *:1 Borrower
# Borrowing *:1 Borrower
class Borrower(db.Model):
    bid = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(255))
    name = db.Column(db.String(255))
    address = db.Column(db.String(255))
    phone = db.Column(db.String(11))
    emailAddress = db.Column(db.String(255))
    sinOrStNo = db.Column(db.String(255))
    expiryDate = db.Column(db.DateTime)
    type = db.Column(db.String(255), db.ForeignKey('borrower_type.type'),
                     nullable=False)
    holdRequests = db.relationship('HoldRequest', backref='borrower',
                                   lazy='dynamic')
    borrowings = db.relationship('Borrowing', backref='borrower',
                                 lazy='dynamic')


# Borrower *:1 BorrowerType
#TODO: set time limit to something fluid, or a chunk
class BorrowerType(db.Model):
    type = db.Column(db.String(255), primary_key=True)
    bookTimeLimit = db.Column(db.Interval)
    borrowers = db.relationship('Borrower', backref='borrower_type',
                                lazy='dynamic')

    def __init__(self, type, time):
        self.type = type
        self.bookTimeLimit = time


# Join table for the Book:Author relationship
HasAuthor = db.Table('has_author',
                     db.Column('callNumber', db.String(50),
                               db.ForeignKey('book.callNumber'),
                               primary_key=True),
                     db.Column('name', db.String(255),
                               db.ForeignKey('author.name'),
                               primary_key=True)
                     )


# Join table for the Book:Subject relationship
HasSubject = db.Table('has_subject',
                      db.Column('callNumber', db.String(50),
                                db.ForeignKey('book.callNumber'),
                                primary_key=True),
                      db.Column('subject', db.String(255),
                                db.ForeignKey('subject.subName'),
                                primary_key=True)
                      )


# Book *:* Author
# Book *:* Subject
# BookCopy *:1 Book
# HoldRequest *:1 Book
class Book(db.Model):
    callNumber = db.Column(db.String(50), primary_key=True)
    isbn = db.Column(db.String(13))
    title = db.Column(db.String(255))
    mainAuthor = db.Column(db.String(255))
    publisher = db.Column(db.String(255))
    year = db.Column(db.String(4))
    authors = db.relationship('Author', secondary=HasAuthor,
                              backref=db.backref('book', lazy='dynamic'))
    subjects = db.relationship('Subject', secondary=HasSubject,
                               backref=db.backref('book', lazy='dynamic'))
    copies = db.relationship('BookCopy', backref='book', lazy='dynamic')
    holdRequests = db.relationship('HoldRequest', backref='book',
                                   lazy='dynamic')


# Book *:* Author
class Author(db.Model):
    name = db.Column(db.String(255), primary_key=True)
    books = db.relationship('Book', secondary=HasAuthor,
                            backref=db.backref('author', lazy='dynamic'))


# Book *:* Subject
class Subject(db.Model):
    subName = db.Column(db.String(255), primary_key=True)
    books = db.relationship('Book', secondary=HasSubject,
                            backref=db.backref('subName', lazy='dynamic'))


# Represents the BorrowableCopy/ItemCopy entity in the document
#TODO: set default status
# BookCopy *:1 Book
# Borrowing *:1 BookCopy
class BookCopy(db.Model):
    callNumber = db.Column(db.String(50), db.ForeignKey('book.callNumber'),
                           primary_key=True)
    copyNo = db.Column(db.String(10), primary_key=True)
    status = db.Column(db.Enum('on-hold', 'in', 'out', name='statuses'),
                       nullable=False)
    borrowings = db.relationship('Borrowing', backref='book_copy',
                                 lazy='dynamic')


# HoldRequest *:1 Borrower
# HoldRequest *:1 Book
class HoldRequest(db.Model):
    hid = db.Column(db.Integer, primary_key=True)
    bid = db.Column(db.Integer, db.ForeignKey('borrower.bid'), nullable=False)
    callNumber = db.Column(db.String(50), db.ForeignKey('book.callNumber'),
                           nullable=False)
    issuedDate = db.Column(db.DateTime)


# This model is a little special in that to define a composite foreign key it
# must be defined through the ForeignKeyConstraint syntax natively through
# sqlalchemy
# Fines *:1 Borrowing
# Borrowing *:1 Borrower
# Borrowing *:1 BookCopy
class Borrowing(db.Model):
    borid = db.Column(db.Integer, primary_key=True)
    bid = db.Column(db.Integer, db.ForeignKey('borrower.bid'), nullable=False)
    callNumber = db.Column(db.String(50), nullable=False)
    copyNo = db.Column(db.String(10), nullable=False)
    outDate = db.Column(db.DateTime)
    inDate = db.Column(db.DateTime)
    __table_args__ = (ForeignKeyConstraint([callNumber, copyNo],
                                           [BookCopy.callNumber,
                                            BookCopy.copyNo]),
                      {})
    fines = db.relationship('Fine', backref='borrowing', lazy='dynamic')

    def __init__(self):
        self.outDate = datetime.now


# Fines *:1 Borrowing
class Fine(db.Model):
    fid = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Numeric(12, 2))
    issuedDate = db.Column(db.DateTime)
    paidDate = db.Column(db.DateTime)
    borid = db.Column(db.Integer, db.ForeignKey('borrowing.borid'),
                      nullable=False)

    def __init__(self):
        self.issuedDate = datetime.now
