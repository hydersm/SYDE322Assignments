# all the imports
import os
import sqlite3
from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

# create our little application :)
app = Flask(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/')
def show_hotels():
    cur = g.db.execute('select guestName, guestAddress from guests order by guestId')
    guests = [dict(guestName=row[0], guestAddress=row[1]) for row in cur.fetchall()]
    return render_template('show_hotels.html', guests=guests)

@app.route('/add', methods=['POST'])
def add_guest():
    g.db.execute('insert into guests (guestName, guestAddress) values (?, ?)',
                 [request.form['guestname'], request.form['address']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_hotels'))

@app.route('/add_booking', methods=['POST'])
def add_booking():
    g.db.execute('insert into guests (guestName, guestAddress) values (?, ?)',
                 [request.form['guestname'], request.form['address']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_hotels'))

@app.route('/get_bookings', methods=['GET'])
def see_bookings():
    g.db.execute('insert into guests (guestName, guestAddress) values (?, ?)',
                 [request.form['guestname'], request.form['address']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_hotels'))

if __name__ == '__main__':
    app.run()