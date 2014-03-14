# No Reservations

## Prerequisites
This application requires the following to be installed:
* [mysql 5.6](http://dev.mysql.com/downloads/mysql/)
* python 2.7
* pip
* [virtualenv](#virtualenv)

### virtualenv
You can build natively or use pip: `sudo pip install virtualenv`

## Getting started
1. Clone repository:
    * `git clone ...`
    * `cd no-reservations/`
1. Setup virtualenv:
    * `virtualenv venv`
1. Activate virtualenv:
    * \*nix: `source venv/bin/activate`
    * Windows: `venv\scripts\activate`
    * **Note**: to exit virtualenv: `deactivate`
1. Install dependencies: `pip install -r requirements.txt`
1. Create the database

### Set up the database
1. Log into mysql with user root password root: `mysql -u root -p`
1. Create the database: `create database no_reservations`
1. Activate virtualenv
1. `python`
1. `from app import db`
1. `db.create_all()`

## Running the app
1. Activate virtualenv
* \*nix: `./run.py`
* Windows: `venv\scripts\python run.py`
1. Open [http://127.0.0.1:5000/](http://127.0.0.1:5000/) in a web browser

## Flask tutorial
This is the [tutorial](http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world) to get started/use as a reference for Flask apps.
