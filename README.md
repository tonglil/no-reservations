# No Reservations

## Prerequisites
This application requires the following to be installed:
* [mysql 5.6](http://dev.mysql.com/downloads/mysql/)
* python 2.7
* pip
* virtualenv: you can build natively or use pip: `sudo pip install virtualenv`

## Getting Started
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
1. Create the database in mysql for the first time

## Running the App
1. Activate virtualenv
1. Run `scripts/reset_fill_db.py` to automatically **drop**, create, and fill the database tables with test data.
1. Run `run.py` to start the server
1. Open [http://127.0.0.1:5000/](http://127.0.0.1:5000/) in a web browser

## Notes

### The database
* Log into mysql with user root password root: `mysql -u root -p`
* Create the database: `create database no_reservations`

Other actions:
* Use the database: `use no_reservations`
* Create a table: `create table table_name`
* Drop (delete) the database: `drop database no_reservations`
* Drop a table: `drop table table_name`

### Running python scripts
* \*nix OSes: `./run.py`
* Windows: `venv\scripts\python run.py`

### Flask tutorial
This is a [tutorial](http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world) to get started/use as a reference for Flask apps.
