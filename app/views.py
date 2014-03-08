from flask import render_template
from app import app


@app.route('/')
@app.route('/index')
def index():
    user = {
        'nickname': 'Miguel'
    }
    posts = [{
        'author': {
            'nickname': 'John'
        },
        'body': 'Beautify day in Vancouver (yeah right)!'
    }, {
        'author': {
            'nickname': 'Susan'
        },
        'body': 'The Avengers movie was so cool!'
    }]
    return render_template('index.html',
                           title='Home',
                           user=user,
                           posts=posts
                           )
