# all the imports
import os
import sqlite3
from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from datetime import date

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

@app.route('/bookings', methods=['POST'])
def add_booking():
    cur = g.db.execute('select startDate endDate from bookings where hotelId=(?) and roomNo=(?) and guestId=(?)', [request.form['hotelId'], request.form['roomNo'], request.form['guestId']])
    rows = [row for row in cur.fetchall()]
    
    if len(rows) > 0:
        for row in rows:
            if request.form['startDate'] >= row[0] and request.form['startDate'] <= row[1]:
                return None
            elif request.form['endDate'] >= row[0] and request.form['endDate'] <= row[1]:
                return None

    g.db.execute('insert into bookings (hotelId, roomNo, guestId, startDate, endDate) values (?, ?, ?, ?, ?)', [request.form['hotelId'], request.form['roomNo'], request.form['guestId'], request.form['startDate'], request.form['endDate']])
    g.db.commit()

    cur = g.db.execute('select bookingId from bookings where hotelId=(?) and roomNo=(?) and guestId=(?) and startDate=(?)', [request.form['hotelId'], request.form['roomNo'], request.form['guestId'], request.form['startDate']])
    rows = [row for row in cur.fetchall()]
    
    return rows[0][0]

@app.route('/booking')
def gotobookings():
    return render_template('bookings.html')

#request args: hotelName, city, price, type, startDate(yyyy-mm-dd), endDate(yyyy-mm-dd)
#returns list of rows, each row containing: hotelId, hotelName, city, roomNo, price, type
@app.route('/get_available_rooms', methods=['GET'])
def see_available_rooms():
    cur = None
    if request.args.get('hotelName') != "" and request.args.get('city') != "":
        cur = g.db.execute('select hotelId from hotels where hotelName=(?) and city=(?)', [request.args.get('hotelName'), request.args.get('city')])
    elif request.args.get('hotelName') != "":
        cur = g.db.execute('select hotelId from hotels where hotelName=(?)', [request.args.get('hotelName')])
    elif request.args.get('city') != "":
        cur = g.db.execute('select hotelId from hotels where city=(?)', [request.args.get('city')])
    else:
        cur = g.db.execute('select hotelId from hotels')
    
    hotelIds = [row[0] for row in cur.fetchall()]

    query = 'select roomNo from rooms'
    if len(hotelIds) > 0:
        query += ' where hotelId in (' + str(hotelIds)[1:-1] + ')'
    if request.args.get('price') != "":
        if 'where' in query:
            query += ' and'
        else:
            query += ' where'

        query += ' price=("' + request.args.get('price') + '")'
    print request.args.get('type')
    if request.args.get('type') != "":
        if 'where' in query:
            query += ' and'
        else:
            query += ' where'

        query += ' type=("' + str(request.args.get('type')) +'")'

    print query
    cur = g.db.execute(query)
    allRoomIds = [row[0] for row in cur.fetchall()]
    
    startDate = date.today().isoformat()
    endDate = startDate
    if request.args.get('startDate'):
        startDate = request.args.get('startDate')
        endDate = startDate
    if request.args.get('endDate'):
        endDate = request.args.get('endDate') if request.args.get('endDate') > endDate else endDate

    cur = g.db.execute('select roomNo, startDate, endDate from bookings') 
    busyRooms = [row for row in cur.fetchall()]
    busyRoomIds = [row[0] for row in busyRooms if (startDate >= row[1] and startDate <= row[2]) or (endDate >= row[1] and endDate <= row[2])]

    availRoomIds = [i for i in allRoomIds if i not in busyRoomIds]

    cur = g.db.execute('select hotels.hotelId, hotels.hotelName, hotels.city, rooms.roomNo, rooms.price, rooms.type from rooms inner join hotels on rooms.hotelId=hotels.hotelId')
    result = [row for row in cur.fetchall() if row[3] in availRoomIds]
    bookings = []
    for room in result:
        bookings.append(
                {
                    "hotelId": room[0],
                    "hotelName": str(room[1]),
                    "roomNo": str(room[2]),
                    "guestId": room[3],
                    "price": room[4],
                    "type": str(room[5])
                }
            )

    return render_template('bookings.html', bookings=bookings)

@app.route('/refresh', methods=['GET'])
def refresh():
    init_db()

    g.db.execute('insert into hotels (city, hotelName) values ("a", "a")')
    g.db.execute('insert into hotels (city, hotelName) values ("a", "b")')
    g.db.execute('insert into hotels (city, hotelName) values ("b", "a")')
    g.db.execute('insert into hotels (city, hotelName) values ("c", "a")')

    g.db.execute('insert into rooms (hotelId, price, type) values (1, 3, "single")')
    g.db.execute('insert into rooms (hotelId, price, type) values (2, 1, "single")')
    g.db.execute('insert into rooms (hotelId, price, type) values (3, 3, "single")')
    g.db.execute('insert into rooms (hotelId, price, type) values (4, 4, "double")')
    g.db.execute('insert into rooms (hotelId, price, type) values (4, 3, "single")')
    g.db.execute('insert into rooms (hotelId, price, type) values (2, 5, "double")')
    
    g.db.execute('insert into guests (guestName, guestAddress) values ("Bob", "Waterloo")')

    g.db.execute('insert into bookings (hotelId, roomNo, guestId, startDate, endDate) values (1, 1, 1, date("2016-03-24"), date("2016-03-25"))')

    g.db.commit()
    
    return 'done'

if __name__ == '__main__':
    app.run()
