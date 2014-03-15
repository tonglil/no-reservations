from app import db

ROLE_USER = 0
ROLE_ADMIN = 1

db.create_all()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    role = db.Column(db.SmallInteger, default=ROLE_USER)

    def __repr__(self):
        return '<User %r>' % (self.nickname)


class Borrower(db.Model):
    bid = db.Column(db.String(64), primary_key=True)
    password = db.Column(db.String(255))
    name = db.Column(db.String(255))
    address = db.Column(db.String(255))
    phone = db.Column(db.String(255))
    emailAddress = db.Column(db.String(255))
    sinOrStNo = db.Column(db.String(255))
    expiryDate = db.Column(db.String(255))
    type = db.Column(db.String(255))


class BorrowerType(db.Model):
    type = db.Column(db.String(255), primary_key=True)
    bookTimeLimit = db.Column()


class Book(db.Model):
    callNumber = db.Column(db.String(255), primary_key=True)
    isbn = db.Column()
    title = db.Column()
    mainAuthor = db.Column()
    publisher = db.Column()
    year = db.Column()


class HasAuthor(db.Model):
    callNumber = db.Column(db.String(255), primary_key=True)
    name = db.Column()


class HasSubject(db.Model):
    callNumber = db.Column(db.String(255), primary_key=True)
    subject = db.Column()


class BookCopy(db.Model):
    callNumber = db.Column(db.String(255), primary_key=True)
    copyNo = db.Column(db.String(255), primary_key=True)
    status = db.Column()


class HoldRequest(db.Model):
    hid = db.Column(db.String(255), primary_key=True)
    bid = db.Column()
    callNumber = db.Column()
    issuedDate = db.Column()


class Borrowing(db.Model):
    borid = db.Column(db.String(255), primary_key=True)
    bid = db.Column()
    callNumber = db.Column()
    copyNo = db.Column()
    outDate = db.Column()
    inDate = db.Column()


class Fine(db.Model):
    fid = db.Column(db.String(255), primary_key=True)
    amount = db.Column()
    issuedDate = db.Column()
    paidDate = db.Column()
    borid = db.Column()
