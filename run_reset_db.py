#!venv/bin/python

from app import app
from app import db

db.engine.execute('SET FOREIGN_KEY_CHECKS = 0')
db.drop_all()
db.engine.execute('SET FOREIGN_KEY_CHECKS = 1')
db.create_all()
app.run(debug=True)
