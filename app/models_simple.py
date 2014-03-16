from app import db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import ForeignKeyConstraint

Base = declarative_base()


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


class BorrowerType(db.Model):
    type = db.Column(db.String(255), primary_key=True)
    bookTimeLimit = db.Column(db.DateTime)


class Book(db.Model):
    callNumber = db.Column(db.String(50), primary_key=True)
    isbn = db.Column(db.String(13))
    title = db.Column(db.String(255))
    mainAuthor = db.Column(db.String(255))
    publisher = db.Column(db.String(255))
    year = db.Column(db.String(4))


#TODO: not sure if this table is created
class Author(db.Model):
    name = db.Column(db.String(255), primary_key=True)


class HasAuthor(db.Model):
    callNumber = db.Column(db.String(50), db.ForeignKey('book.callNumber'),
                           primary_key=True)
    name = db.Column(db.String(255), primary_key=True)


#TODO: not sure if this table is created
class Subject(db.Model):
    subName = db.Column(db.String(255), primary_key=True)


class HasSubject(db.Model):
    callNumber = db.Column(db.String(50), db.ForeignKey('book.callNumber'),
                           primary_key=True)
    subject = db.Column(db.String(255), primary_key=True)


# Represents the BorrowableCopy/ItemCopy entity in the document
#TODO: set default status
class BookCopy(db.Model):
    callNumber = db.Column(db.String(50), db.ForeignKey('book.callNumber'),
                           primary_key=True)
    copyNo = db.Column(db.String(10), primary_key=True)
    status = db.Column(db.Enum('on-hold', 'in', 'out', name='statuses'),
                       nullable=False)


class HoldRequest(db.Model):
    hid = db.Column(db.Integer, primary_key=True)
    bid = db.Column(db.Integer, db.ForeignKey('borrower.bid'), nullable=False)
    callNumber = db.Column(db.String(50), db.ForeignKey('book.callNumber'),
                           nullable=False)
    issuedDate = db.Column(db.DateTime)


#This model is a little special in that to define a composite foreign key it
#must be defined through the ForeignKeyConstraint syntax natively through
#sqlalchemy
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


class Fine(db.Model):
    fid = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Numeric(12, 2))
    issuedDate = db.Column(db.DateTime)
    paidDate = db.Column(db.DateTime)
    borid = db.Column(db.Integer, db.ForeignKey('borrowing.borid'),
                      nullable=False)
