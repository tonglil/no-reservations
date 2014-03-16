#!venv/bin/python

from app import app
from app import db

db.drop_all()
db.create_all()
app.run(debug=True)
