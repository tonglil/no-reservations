from flask import render_template
from app import app


@app.route('/')
@app.route('/index')
#@app.route('/login', methods=['GET', 'POST'])
def index():
    return render_template('index.html',
                           title='Home'
                           )
