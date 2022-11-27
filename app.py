import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, g, redirect, url_for, render_template, flash, session
import werkzeug
from random import choices

app = Flask(__name__)

app.config.update(dict(
    #might have to change this back to flaskr instead of projectcards
    DATABASE=os.path.join(app.root_path, 'projectcards.db'),
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
    db = get_db()

    cur = db.execute('SELECT DISTINCT rank FROM cards ORDER BY rank')
    cards = cur.fetchall()
    cur = db.execute('SELECT * FROM collection ORDER BY card_id')
    collection = cur.fetchall()

    return render_template('your_inventory.html', cards=cards, collection=collection)


@app.route('/marketplace')
def marketplace():
    db = get_db()

    cur = db.execute('SELECT * FROM cards')
    cards = cur.fetchall()

    return render_template('marketplace.html', cards=cards)


@app.route('/connect_with_friends')
def connect_with_friends():
    return render_template('friends.html')


@app.route('/friend_inventory')
def friend_inventory():
    return render_template('friend_inventory.html')


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
        session['current_user'] = ("SELECT user_id FROM users WHERE username=?", [request.form['username']])
        return redirect(url_for('home'))
    return redirect(url_for('home'))


@app.route('/logout', methods=['POST'])
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))
     

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


@app.route('/add_friend', methods=['GET', 'POST'])
def add_friend():
    db = get_db()
    added_friend = request.form['new_friend']
    friend_id = db.execute("SELECT user_id FROM users WHERE username=?", [added_friend])
    user_id = db.execute("SELECT user_id FROM users WHERE username=?", [session['current_user']])
    friend_check = friend_id.fetchone()
    if friend_check is None:
        flash('user does not exist')
        return redirect(url_for('connect_with_friends'))
    already_friend = db.execute("SELECT * FROM friends WHERE user1=? AND user2=?", [user_id, friend_id])
    if already_friend:
        flash('this action has already been taken')
        return redirect(url_for('connect_with_friends'))

    flash('added friend, have them add you as well to become friends')
    db.execute('INSERT INTO friends (user1_id, user2_id)VALUES (?, ?)', [user_id, friend_id])


@app.route('/add_cards', methods=['POST'])
def add_cards():
    db = get_db()

    db.execute('INSERT INTO collection SELECT * FROM cards WHERE card_id=?', [request.form["id"]])
    db.commit()

    return redirect(url_for('marketplace'))


@app.route('/purchase', method=['POST'])
def purchase(amount):
    # use this method every time there is a purchase(pack or card) it will limit duplication of code in our application.
    # decreases the wallet of the logged-in user by the amount of the purchase, which is passed in as argument
    db = get_db()
    user_wallet = ('SELECT wallet_balance FROM users WHERE username=?', [session['current_user']])
    # this next line is weird, user wallet is being stored the wrong way
    user_wallet = user_wallet[2].fetchone()[4]
    new_balance = user_wallet-amount
    db.execute("UPDATE users SET wallet_balance=? WHERE username=?", [new_balance, session['current_user']])


@app.route('/buy_cards', method=['POST'])
def buy_card(card_id):
    # This function is used when purchasing an individual card: takes the id of the desired card as argument
    # and calls the purchase method with the card price to adjust the user wallet
    # Also inserts the card with corresponding id into the collection table
    db = get_db()
    user_id = db.execute("SELECT user_id FROM users WHERE username=?", [session['current_user']])
    user_id = user_id.fetchone()[0]
    card_price = db.execute("SELECT price FROM store WHERE card_id=?", [card_id])
    card_price = card_price.fetchone()[3]
    purchase(card_price)
    db.execute('INSERT INTO collection SELECT * FROM cards WHERE card_id=?', [card_id])
    db.execute('INSERT INTO transactions (user_id, card_id, wallet_change) VALUES (?, ?, ?)',
               [user_id, card_id, card_price])
    flash('Successfully purchased a card')
    db.commit()
