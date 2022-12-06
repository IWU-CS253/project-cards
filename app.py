import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, g, redirect, url_for, render_template, flash, session
import werkzeug
from random import choices

app = Flask(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    DEBUG=True,
    SECRET_KEY='development key',
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    """Initializes the database."""
    db = get_db()
    with app.open_resource('database.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.cli.command('initdb')
def initdb_command():
    """Creates the database tables."""
    init_db()
    print('Initialized the database.')


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/')
def show_entries():
    return render_template('login.html')


@app.route('/your_inventory')
def your_inventory():
    return render_template('your_inventory.html')


@app.route('/marketplace')
def marketplace():
    return render_template('marketplace.html')


@app.route('/connect_with_friends')
def connect_with_friends():
    return render_template('friends.html')


@app.route('/friend_inventory')
def friend_inventory():
    return render_template('friend_inventory.html')

@app.route('/trade')
def trade():
    return render_template('trade.html')


@app.route('/trade_request')
def trade_request():
    return render_template('trade_request.html')

@app.route('/trade_result')
def trade_result():
    return render_template('trade_result.html')

@app.route('/new_user_info', methods=['GET'])
def new_user_info():
    return render_template('create_user.html')


@app.route('/create_user', methods=['POST'])
def create_user():
    db = get_db()
    chosen_username = request.form['choose_username']
    user_exists = db.execute("SELECT password FROM users WHERE username=?", [chosen_username])
    user_exists_check = user_exists.fetchone()
    if user_exists_check:
        flash('username already taken')
        return redirect(url_for('new_user_info'))

    hashed_pw = werkzeug.security.generate_password_hash(request.form['choose_password'], method='pbkdf2:sha256',
                                                         salt_length=16)
    chosen_email = request.form['choose_email']
    email_exists = db.execute("SELECT password FROM users WHERE email=?", [chosen_email])
    email_exists_check = email_exists.fetchone()
    if email_exists_check:
        flash('email already taken')
        return redirect(url_for('new_user_info'))
    db.execute('insert into users (username, password, email) values (?, ?, ?)',
               [chosen_username, hashed_pw, chosen_email])
    db.commit()
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    error = None
    db = get_db()
    pswd = db.execute("SELECT password FROM users WHERE username=?", [request.form['username']])
    pw_check = pswd.fetchone()
    if pw_check is None:
        flash('invalid username')
        return redirect(url_for('show_entries'))
    if not werkzeug.security.check_password_hash(pw_check['password'], request.form['password']):
        error = 'Invalid password'
        flash('incorrect password')
        return redirect(url_for('show_entries'))
    else:
        session['logged_in'] = True
        flash('You were logged in')
        current_user = db.execute("SELECT user_id FROM users WHERE username=?", [request.form['username']])
        return redirect(url_for('home'))
    return redirect(url_for('home'))

@app.route('/trade', methods=['POST'])
def sendtrade():
    """updates ownership in database"""
    db = get_db()
    current_user = db.execute("UPDATE card_id FROM collection WHERE cards=?", [request.form['cards']])
    db.commit()
    flash('Trade sent')
    return redirect(url_for('trade_result'))

@app.route('/trade', methods=['GET'])
def checktrades():
    """pulls in trade offers"""
    db = get_db()
    db.execute('INSERT INTO collection WHERE (cards,users) VALUES (?,?)',
               [request.form['cards']])
    db.commit()
    flash('Trade pending')
    return redirect(url_for('trade_request'))





@app.route('/trade', methods=['POST'])
def confirmtrade():
    """gives user the ability to accept/decline trades"""
    db = get_db()
    trade = db.execute("SELECT cards  FROM collection WHERE card_id=?", [request.form['cards']])

    if trade is None:
        flash('No Trades')
        return redirect(url_for('trade'))
    else
        trade = True
        db.execute("UPDATE cards FROM collection WHERE card_id=?", [request.form['cards']])
        flash('incorrect password')
        return redirect(url_for('show_entries'))
    else:
        trade = False
        flash('Trade Declined')
        return redirect(url_for('trade_result'))



#@app.route('/logout')
#def logout():
#   session.pop('logged_in', None)
#   flash('You were logged out')
#   return redirect(url_for('login'))
     

def pull_cards():
    """Adds 5 cards to collections table from the total cards table using rank
            to determine the probability of pulling each card"""
    db = get_db()

    # create a list of weights for use in random's choice method
    card_weight = db.execute('SELECT rank FROM cards')
    ranks = card_weight.fetchall()
    ranks = [rank[0] for rank in ranks]

    # pull 5 cards from the cards table and inserts the card to the collection table
    for i in range(5):
        pull = choices(range(1, 52), ranks)
        ran_pull = db.execute('SELECT * FROM cards WHERE card_id = ?', pull)
        card = ran_pull.fetchone()

        db.execute('INSERT INTO collection VALUES (?, ?, ?)', card)
        db.commit()


