import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, g, redirect, url_for, render_template, flash, session
import werkzeug
from random import choices
import csv

app = Flask(__name__)

app.config.update(dict(
    # might have to change this back to flaskr instead of projectcards
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

    database = os.path.join(app.root_path, 'projectcards.db')
    connection = sqlite3.connect(database)
    cursor = connection.cursor()
    file = os.path.join(app.root_path, 'cards_csv/mix_pack1.csv')
    contents = csv.reader(open(file))
    insert_records = "INSERT INTO store (card_id, rank, image, pack, price) VALUES(?, ?, ?, ?, ?);"
    cursor.executemany(insert_records, contents)
    file_cards = os.path.join(app.root_path, 'cards_csv/all_cards.csv')
    insert_cards = "INSERT INTO cards (card_id, name, rank, price) VALUES (?, ?, ?, ?);"
    contents_cards = csv.reader(open(file_cards))
    cursor.executemany(insert_cards, contents_cards)
    connection.commit()
    connection.close()


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
    db = get_db()

    cur = db.execute('SELECT wallet_balance FROM users WHERE user_id=?', [session['current_user']])
    wallet = cur.fetchone()

    cur = db.execute('SELECT username FROM users WHERE user_id=?', [session['current_user']])
    user = cur.fetchone()

    return render_template('home.html', wallet=wallet, user=user)


@app.route('/')
def show_entries():
    return render_template('login.html')


@app.route('/your_inventory')
def your_inventory():
    db = get_db()

    cur = db.execute('SELECT DISTINCT rank FROM cards ORDER BY rank')
    cards = cur.fetchall()
    cur = db.execute("SELECT * FROM cards JOIN collection ON collection.card_id = cards.card_id WHERE collection.user_id=?", [session['current_user']])
    collection = cur.fetchall()

    return render_template('your_inventory.html', cards=cards, collection=collection)


@app.route('/marketplace')
def marketplace():
    db = get_db()

    cur = db.execute('SELECT * FROM cards WHERE card_id = 7 OR card_id = 82 OR card_id = 153')
    cards = cur.fetchall()

    return render_template('marketplace.html', cards=cards)


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


@app.route('/transactions')
def transactions():
    db = get_db()

    cur = db.execute('SELECT * FROM transactions')
    transaction_history = cur.fetchall()

    return render_template('transactions.html', transaction_history=transaction_history)


@app.route('/collections')
def collections():
    return render_template('collections.html')


@app.route('/wallet_balance', methods=['POST'])
def wallet_balance():
    db = get_db()
    balance = request.form['wallet_balance']
    user_wallet = db.execute("SELECT wallet_balance FROM users WHERE username=?", [balance])
    user_wallet_check = user_wallet.fetchone()
    if user_wallet_check:
        return render_template('home.html', user_wallet=user_wallet_check)


@app.route('/sell_cards', methods=['POST'])
def sell_cards():
    db = get_db()


@app.route('/get_user', methods=['POST'])
def get_user():
    db = get_db()
    user = request.form['username']
    user_exist = db.execute("SELECT wallet_balance FROM users WHERE username=?", [user])
    user_exist_check = user_exist.fetchone()
    if user_exist_check:
        return render_template('home.html', user_exist=user_exist_check)


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
    db.execute('insert into users (username, password, email, wallet_baLance) values (?, ?, ?, 500)',
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
        cur = db.execute("SELECT user_id FROM users WHERE username=?", [request.form['username']])
        session['current_user'] = cur.fetchone()['user_id']
        return redirect(url_for('home'))
    return redirect(url_for('home'))


@app.route('/logout', methods=['GET'])
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))
     

@app.route('/pull_cards')
def pull_cards():
    """Adds 5 cards to collections table from the total cards table using rank
            to determine the probability of pulling each card"""
    if not purchase(250):
        db = get_db()

        # create a list of weights for use in random's choice method
        card_weight = db.execute('SELECT rank FROM store')
        ranks = [float(rank[0]) for rank in card_weight.fetchall()]
        card_population = db.execute('SELECT card_id FROM store')
        cid_list = [card_id[0] for card_id in card_population.fetchall()]

        cards_img = []

        # pull 5 cards from the cards table and inserts the card to the collection table
        for i in range(5):
            pull = choices(cid_list, ranks)
            ran_pull = db.execute('SELECT card_id FROM store WHERE card_id = ?', pull)
            card = ran_pull.fetchone()
            db.execute('INSERT INTO collection(card_id, user_id) VALUES (?, ?)', [card[0], session['current_user']])
            db.commit()

            img = db.execute('SELECT image FROM store WHERE card_id = ?', pull)
            img = img.fetchone()
            for row in img:
                cards_img.append(row)

        return render_template('pull_cards.html', cards=cards_img)

    else:
        return redirect(url_for('marketplace'))



@app.route('/add_friend', methods=['GET', 'POST'])
def add_friend():
    db = get_db()
    added_friend = request.form['new_friend']
    friend_id = db.execute("SELECT user_id FROM users WHERE username=?", [added_friend]).fetchone()
    #friend_id = friend_id[0]
    if friend_id is None:
        flash('user does not exist')
        return redirect(url_for('connect_with_friends'))
    friend_id = friend_id[0]
    already_friend = db.execute("SELECT * FROM friends WHERE user1_id=? AND user2_id=?", [session['current_user'],
                                                                                          friend_id])
    # commented out to test displaying friends list - may be preventing the addition of friends in the first place
    # if already_friend is not None:
    #     flash('this action has already been taken')
    #     return redirect(url_for('connect_with_friends'))

    flash('added friend, have them add you as well to become friends')
    db.execute('INSERT INTO friends (user1_id, user2_id)VALUES (?, ?)', [session['current_user'], friend_id])
    db.commit()
    return redirect(url_for('connect_with_friends'))
  
  
@app.route('/add_cards', methods=['POST'])
def add_cards():
    db = get_db()
    cur = db.execute('SELECT card_id FROM cards WHERE card_id=?', [request.form['id']])
    card = cur.fetchone()
    db.execute('INSERT INTO collection(card_id, user_id) VALUES(?, ?)', [card[0], session['current_user']])
    db.commit()

    return redirect(url_for('marketplace'))


@app.route('/purchase', methods=['GET'])
def purchase(amount):
    # use this method every time there is a purchase(pack or card) it will limit duplication of code in our application.
    # decreases the wallet of the logged-in user by the amount of the purchase, which is passed in as argument
    db = get_db()
    broke = False
    user_wallet = db.execute('SELECT wallet_balance FROM users WHERE user_id=?', [session['current_user']])
    user_wallet = user_wallet.fetchone()[-1]
    new_balance = (user_wallet - amount)
    if new_balance < 0:
        flash('insufficient funds: get ya money up')
        broke = True
        return broke
    db.execute("UPDATE users SET wallet_balance=? WHERE user_id=?", [new_balance, session['current_user']])
    db.commit()
    return broke


@app.route('/buy_cards', methods=['POST'])
def buy_card():
    # This function is used when purchasing an individual card: takes the id of the desired card as argument
    # and calls the purchase method with the card price to adjust the user wallet
    # Also inserts the card with corresponding id into the collection table
    db = get_db()
    cur = db.execute('SELECT card_id FROM cards WHERE card_id=?', [request.form['id']])
    card_id = cur.fetchone()
    card_price = db.execute("SELECT price FROM store WHERE card_id=?", card_id)
    card_price = card_price.fetchone()[-1]
    broke_check = purchase(card_price)
    if broke_check:
        return redirect(url_for('marketplace'))
    add_cards()
    wallet_change = -1 * card_price
    db.execute('INSERT INTO transactions(user_id, card_id, wallet_change) VALUES (?, ?, ?)',
               [session['current_user'], card_id[0], wallet_change])
    flash('Successfully purchased a card')
    db.commit()
    return redirect(url_for('marketplace'))


@app.route('/show_friends', methods=['GET'])
def show_friends():
    db = get_db()
    cur = db.execute('SELECT * FROM friends WHERE user1_id=?', [session['current_user']])
    friend_list = []
    friends_list = cur.fetchall()
    for i in friends_list:
        friend_username = db.execute('SELECT username FROM users WHERE user_id=?', [i[1]])
        f = friend_username.fetchone()[0]
        friend_list.append(f)
    return render_template('friends.html', friend_list=friend_list)


@app.route('/sell', methods=['GET'])
def sell(amount):
    db = get_db()
    user_wallet = db.execute('SELECT wallet_balance FROM users WHERE user_id=?', [session['current_user']])
    user_wallet = user_wallet.fetchone()[-1]
    add_balance = (user_wallet + amount)

    db.execute("UPDATE users SET wallet_balance=? WHERE user_id=?", [add_balance, session['current_user']])
    db.commit()


@app.route('/sell_card', methods=['POST'])
def sell_card():
    db = get_db()
    cur = db.execute('SELECT card_id FROM collection WHERE card_id=?', [request.form['id']])
    card_id = cur.fetchone()
    sell_price = db.execute('SELECT price FROM cards WHERE card_id=?', card_id)
    price = sell_price.fetchone()[-1]
    delete = db.execute('SELECT delete_id FROM collection WHERE delete_id=?', [request.form['delete_id']])
    delete_id = delete.fetchone()
    delete_card = db.execute('DELETE FROM collection WHERE delete_id=?', delete_id)
    delete_card = delete_card.fetchone()
    sell(price)
    db.execute('INSERT INTO transactions(user_id, card_id, wallet_change) VALUES (?, ?, ?)',
               [session['current_user'], card_id[0], price])
    flash('Successfully sold a card')
    db.commit()
    return redirect(url_for('your_inventory'))


@app.route('/starter_collection', methods=['GET'])
def starter_collection():
    db = get_db()
    cur = db.execute('SELECT * FROM collection WHERE EXISTS(SELECT delete_id WHERE card_id=? AND user_id=?)',
                     [7, session['current_user']])
    cheese = cur.fetchone()
    cur = db.execute('SELECT * FROM collection WHERE EXISTS(SELECT delete_id WHERE card_id=? AND user_id=?)',
                     [12, session['current_user']])
    taco = cur.fetchone()
    cur = db.execute('SELECT * FROM collection WHERE EXISTS(SELECT delete_id WHERE card_id=? AND user_id=?)',
                     [53, session['current_user']])
    cat = cur.fetchone()
    if cheese is None or taco is None or cat is None:
        flash('you do not have all the cards required for this collection, bozo')
        return redirect(url_for('collections'))
    else:
        db.execute('DELETE FROM collection WHERE delete_id=?', [cheese[0]])
        db.execute('DELETE FROM collection WHERE delete_id=?', [taco[0]])
        db.execute('DELETE FROM collection WHERE delete_id=?', [cat[0]])
        sell(500)
        db.commit()
        flash('You turned in Cheese, Taco, and Cat for 500 points')
        return redirect(url_for('collections'))


@app.route('/body_collection', methods=['GET'])
def body_collection():
    db = get_db()
    cur = db.execute('SELECT * FROM collection WHERE EXISTS(SELECT delete_id WHERE card_id=? AND user_id=?)',
                     [161, session['current_user']])
    belly = cur.fetchone()
    cur = db.execute('SELECT * FROM collection WHERE EXISTS(SELECT delete_id WHERE card_id=? AND user_id=?)',
                     [198, session['current_user']])
    brain = cur.fetchone()
    if belly is None or brain is None:
        flash('you do not have all the cards required for this collection, bozo')
        return redirect(url_for('collections'))
    else:
        db.execute('DELETE FROM collection WHERE delete_id=?', [belly[0]])
        db.execute('DELETE FROM collection WHERE delete_id=?', [brain[0]])
        sell(250)
        db.commit()
        flash('You turned in Belly and Brain in exchange for 250 points')
        return redirect(url_for('collections'))
