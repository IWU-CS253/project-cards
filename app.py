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
    file = os.path.join(app.root_path, 'cards_csv/mix_packs.csv')
    contents = csv.reader(open(file))
    insert_records = "INSERT INTO store (card_id, rank, image, pack1, pack2, pack3, pack4, pack5, pack6, pack7) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"
    cursor.executemany(insert_records, contents)
    file_cards = os.path.join(app.root_path, 'cards_csv/all_cards.csv')
    insert_cards = "INSERT INTO cards (card_id, name, rank) VALUES (?, ?, ?);"
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

    if "rank" in request.args:
        cur = db.execute('SELECT * FROM collection JOIN cards ON collection.card_id = cards.card_id '
                         'WHERE collection.user_id=? AND cards.rank=?', [session['current_user'], request.args['rank']])
        collection = cur.fetchall()

    else:
        cur = db.execute('SELECT * FROM collection JOIN cards ON collection.card_id = cards.card_id '
                         'WHERE collection.user_id=?', [session['current_user']])
        collection = cur.fetchall()

    cur = db.execute('SELECT DISTINCT rank FROM cards ORDER BY rank')
    cards = cur.fetchall()

    return render_template('your_inventory.html', cards=cards, collection=collection)



@app.route('/marketplace')
def marketplace():
    db = get_db()

    cur = db.execute('SELECT * FROM marketplace')
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
        flash('Username already taken')
        return redirect(url_for('new_user_info'))

    hashed_pw = werkzeug.security.generate_password_hash(request.form['choose_password'], method='pbkdf2:sha256',
                                                         salt_length=16)
    chosen_email = request.form['choose_email']
    email_exists = db.execute("SELECT password FROM users WHERE email=?", [chosen_email])
    email_exists_check = email_exists.fetchone()
    if email_exists_check:
        flash('Email already taken')
        return redirect(url_for('new_user_info'))
    db.execute('insert into users (username, password, email, wallet_baLance) values (?, ?, ?, 1000)',
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
        flash('Invalid username')
        return redirect(url_for('show_entries'))
    if not werkzeug.security.check_password_hash(pw_check['password'], request.form['password']):
        error = 'Invalid password'
        flash('Incorrect password')
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
     

@app.route('/pull_cards', methods=["POST"])
def pull_cards():
    """Adds 5 cards to collections table from the store table using rank
            to determine the probability of pulling each card"""
    if not purchase(250):
        db = get_db()
        pack = request.form.get('pack')

        # create a list of weights for use in random's choice method
        query = "SELECT rank FROM store WHERE {} = 'TRUE'".format(pack)
        card_weight = db.execute(query)
        ranks = [float(rank[0]) for rank in card_weight.fetchall()]

        query = "SELECT card_id FROM store WHERE {} = 'TRUE'".format(pack)
        card_population = db.execute(query)
        cid_list = [card_id[0] for card_id in card_population.fetchall()]

        cards_img = []

        # pull 5 cards from the cards table and inserts the card to the collection table
        for i in range(5):
            pull = choices(cid_list, ranks)
            query = "SELECT card_id FROM store WHERE {} = 'TRUE' AND card_id = ?".format(pack)
            ran_pull = db.execute(query, pull)
            card = ran_pull.fetchone()

            query = "SELECT image FROM store WHERE {} = 'TRUE' AND card_id = ?".format(pack)
            img = db.execute(query, pull)
            img = img.fetchone()

            db.execute('INSERT INTO collection(card_id, user_id, image) VALUES (?, ?, ?)',
                       [card[0], session['current_user'], img[0]])

            for row in img:
                cards_img.append(row)
            db.commit()

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
        flash('User does not exist')
        return redirect(url_for('connect_with_friends'))
    friend_id = friend_id[0]
    already_friend = db.execute("SELECT * FROM friends WHERE user1_id=? AND user2_id=?", [session['current_user'],
                                                                                          friend_id])
    # commented out to test displaying friends list - may be preventing the addition of friends in the first place
    # if already_friend is not None:
    #     flash('this action has already been taken')
    #     return redirect(url_for('connect_with_friends'))

    flash('Added friend, have them add you as well to become friends')
    db.execute('INSERT INTO friends (user1_id, user2_id)VALUES (?, ?)', [session['current_user'], friend_id])
    db.commit()
    return redirect(url_for('connect_with_friends'))
  
  
@app.route('/add_cards')
def add_cards(market_id):
    db = get_db()
    cur = db.execute('SELECT card_id FROM marketplace WHERE market_id=?', market_id)
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
        flash('Insufficient funds: get ya money up')
        broke = True
        return broke
    db.execute("UPDATE users SET wallet_balance=? WHERE user_id=?", [new_balance, session['current_user']])
    db.commit()
    return broke


@app.route('/buy_card', methods=["POST"])
def buy_card():
    # This function is used when purchasing an individual card: takes the id of the desired card as argument
    # and calls the purchase method with the card price to adjust the user wallet
    # Also inserts the card with corresponding id into the collection table
    db = get_db()
    card_id = request.form.get('card_id')
    market_id = request.form.get('market_id')

    card_price = db.execute("SELECT price FROM marketplace WHERE market_id=?", market_id)
    card_price = card_price.fetchone()[-1]
    broke_check = purchase(card_price)
    if broke_check:
        return redirect(url_for('marketplace'))
    add_cards(market_id)
    wallet_change = -1 * card_price
    db.execute('INSERT INTO transactions(user_id, card_id, wallet_change) VALUES (?, ?, ?)',
               [session['current_user'], card_id[0], wallet_change])

    wallet_change_out = card_price
    user_id_out = db.execute('SELECT user_id FROM marketplace WHERE market_id=?', market_id)
    user_id_out = user_id_out.fetchone()
    sell(card_price, user_id_out)
    db.execute('INSERT INTO transactions(user_id, card_id, wallet_change) VALUES (?, ?, ?)',
               [user_id_out[0], card_id[0], wallet_change_out])

    db.execute('DELETE FROM marketplace WHERE market_id=?', market_id)

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
def sell(amount, user_id):
    db = get_db()
    user_wallet = db.execute('SELECT wallet_balance FROM users WHERE user_id=?', user_id)
    user_wallet = user_wallet.fetchone()[-1]
    add_balance = (user_wallet + amount)

    db.execute('UPDATE users SET wallet_balance=? WHERE user_id=?', [add_balance, user_id[0]])
    db.commit()


@app.route('/sell_card', methods=['POST'])
def sell_card():
    db = get_db()
    card_id = request.form.get('id')
    price = request.form.get('choose_price')
    name = request.form.get('name')
    cur = db.execute('INSERT INTO marketplace(user_id, card_id, name, price) VALUES(?, ?, ?, ?)',
                     [session['current_user'], card_id, name, price])

    delete_id = request.form.get('delete_id')
    delete_card = db.execute('DELETE FROM collection WHERE delete_id=?', [delete_id])
    delete_card = delete_card.fetchone()

    db.commit()
    return redirect(url_for('your_inventory'))


@app.route('/post_card', methods=["POST"])
def post_card():
    db = get_db()
    card_id = request.form.get('id')
    delete_id = request.form.get('delete_id')

    cur = db.execute('SELECT image FROM collection WHERE card_id = ?', [card_id])
    image = cur.fetchone()
    card_image = []
    for row in image:
        card_image.append(row)

    cur = db.execute('SELECT name FROM cards JOIN collection ON cards.card_id = ?', [card_id])
    name = cur.fetchone()
    card_name = []
    for row in name:
        card_name.append(row)

    return render_template('post_card.html', cardimage=card_image, cardname=card_name, id=card_id, delete_id=delete_id)


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
        flash('You do not have all the cards required for this collection, bozo')
        return redirect(url_for('collections'))
    else:
        db.execute('DELETE FROM collection WHERE delete_id=?', [cheese[0]])
        db.execute('DELETE FROM collection WHERE delete_id=?', [taco[0]])
        db.execute('DELETE FROM collection WHERE delete_id=?', [cat[0]])
        sell(500, session['current_user'])
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
        flash('You do not have all the cards required for this collection, bozo')
        return redirect(url_for('collections'))
    else:
        db.execute('DELETE FROM collection WHERE delete_id=?', [belly[0]])
        db.execute('DELETE FROM collection WHERE delete_id=?', [brain[0]])
        sell(250, session['current_user'])
        db.commit()
        flash('You turned in Belly and Brain in exchange for 250 points')
        return redirect(url_for('collections'))


@app.route('/view_cards', methods=["POST"])
def view_cards():
    db = get_db()
    pack = request.form.get('pack')
    query = "SELECT image FROM store WHERE {} = 'TRUE' ORDER BY rank DESC".format(pack)
    images = db.execute(query)
    cards = [images[0] for images in images.fetchall()]

    return render_template('view_cards.html', cards=cards)


