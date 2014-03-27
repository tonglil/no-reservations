#!venv/bin/python

from app import db
from app import models
import datetime

type_student = models.BorrowerType('student', datetime.timedelta(weeks=2))
db.session.add(type_student)

type_faculty = models.BorrowerType('faculty', datetime.timedelta(weeks=12))
db.session.add(type_faculty)

type_staff = models.BorrowerType('staff', datetime.timedelta(weeks=6))
db.session.add(type_staff)

db.session.commit()
