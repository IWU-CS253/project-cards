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
    insert_records = "INSERT INTO store (card_id, rank, image, pack1, pack2, pack3, pack4, pack5, pack6, pack7) " \
                     "VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"
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

    cur = db.execute('SELECT wallet_balance FROM users WHERE user_id=?', [session['current_user']])
    wallet = cur.fetchone()

    return render_template('marketplace.html', cards=cards, wallet=wallet)


@app.route('/connect_with_friends')
def connect_with_friends():
    return render_template('friends.html')


@app.route('/friend_inventory', methods=["POST", "GET"])
def friend_inventory():
    db = get_db()

    username = request.form.get('user')
    user_id = db.execute('SElECT user_id FROM users WHERE username = ?', [username])
    user_id = user_id.fetchone()

    if "rank" in request.args:
        cur = db.execute('SELECT * FROM collection JOIN cards ON collection.card_id = cards.card_id '
                         'WHERE collection.user_id=? AND cards.rank=?', [user_id[0], request.args['rank']])
        collection = cur.fetchall()

    else:
        cur = db.execute('SELECT * FROM collection JOIN cards ON collection.card_id = cards.card_id '
                         'WHERE collection.user_id=?', [user_id[0]])
        collection = cur.fetchall()

    cur = db.execute('SELECT DISTINCT rank FROM cards ORDER BY rank')
    cards = cur.fetchall()

    return render_template('friend_inventory.html', cards=cards, collection=collection)


@app.route('/trade')
def trade():
    return render_template('trade.html')

@app.route('/trade_request',methods=['GET', 'POST'])
def trade_request():
    db = get_db()
    user = request.args['username']
    user_cur = db.execute("""SELECT users.user_id,collection.card_id,store.rank,store.image,name,collection.delete_id
                                FROM users
                              JOIN collection
                                ON users.user_id = collection.user_id
                              JOIN cards 
                                ON cards.card_id= collection.card_id
                              Join Store
                                On cards.card_id= store.card_id
                              WHERE users.username =?""",  [user])
    cur = db.execute(
        "SELECT * FROM cards JOIN collection ON collection.card_id = cards.card_id WHERE collection.user_id=?",
        [session['current_user']])
    collection = cur.fetchall()

    user_inv = user_cur.fetchall()

    return render_template('trade_request.html', deck=user_inv, collection=collection, user=user)



@app.route('/trade_result', methods=['POST'])
def trade_result():

    db = get_db()

    delete_id_r = request.form.getlist('delete_id_r')
    cards_request = request.form.getlist('card_id_request')

    delete_id_o = request.form.getlist('delete_id_o')
    cards_offer = request.form.getlist('card_id_offer')
    requested_user = request.form.get('user')

    user_id = db.execute('SELECT user_id FROM users WHERE username = ?', requested_user)
    user_id = user_id.fetchone()

    most_recent = db.execute('SELECT trade_id FROM trades ORDER BY trade_id DESC')
    most_recent = most_recent.fetchone()

    if most_recent is None:
        new_id = 1
    else:
        new_id = most_recent[0] + 1

    i = 0
    for card in cards_request:
        db.execute('INSERT INTO trades (trade_id, request_id, offer_id, card_id, delete_id) VALUES(?, ?, ?, ?, ?)',
                   [new_id, user_id[0], session['current_user'], card, delete_id_r[i]])
        i += 1

    j = 0
    for card in cards_offer:
        db.execute('INSERT INTO trades (trade_id, request_id, offer_id, card_id, delete_id) VALUES(?, ?, ?, ?, ?)',
                   [new_id + 1, user_id[0], session['current_user'], card, delete_id_o[j]])
        j += 1

    db.commit()

    request_cards = db.execute('SELECT * FROM store JOIN trades WHERE store.card_id = trades.card_id AND trades.offer_id = ?', [user_id[0]])
    request_cards = request_cards.fetchall()

    offer_cards = db.execute('SELECT * FROM store JOIN trades WHERE store.card_id = trades.card_id AND trades.request_id = ?', [session['current_user']])
    offer_cards = offer_cards.fetchall()

    return render_template('trade_result.html', offer=offer_cards, request=request_cards)


@app.route('/pending_trades.html', methods=["GET", "POST"])
def pending_trades():
    db = get_db()

    trade_offers = db.execute('SELECT offer_id FROM trades WHERE request_id = ? GROUP BY offer_id', [session['current_user']])
    trade_offers = trade_offers.fetchall()

    trade_ids = db.execute('SELECT trade_id FROM trades WHERE request_id = ? GROUP BY offer_id', [session['current_user']])
    trade_ids = trade_ids.fetchall()
    trade_id_list = [trade_id[0] for trade_id in trade_ids]

    print(trade_id_list)

    usernames = []
    requested_cards_list = []
    offered_cards_list = []

    for i in range(len(trade_offers)):
        user = db.execute('SELECT username FROM users WHERE user_id = ?', trade_offers[i])
        user = user.fetchone()
        usernames.append(user[0])

        request_id = trade_ids[i][0] + 1

        offered_cards = db.execute("""SELECT cards.name FROM cards JOIN trades WHERE trades.card_id = cards.card_id
                                        AND trades.trade_id = ?""", trade_ids[i])
        offered_cards_list.append([card[0] for card in offered_cards.fetchall()])

        requested_cards = db.execute("""SELECT cards.name FROM cards JOIN trades WHERE trades.card_id = cards.card_id
                                        AND trades.trade_id = ?""", [request_id])
        requested_cards_list.append([card[0] for card in requested_cards.fetchall()])

    return render_template('pending_trades.html', users=usernames, trade_id=trade_id_list,
                           offered=offered_cards_list, requested=requested_cards_list)


@app.route('/finalize', methods=["POST", "GET"])
def finalize():

    db = get_db()
    trade_id = request.form.get('id')
    trade_id2 = int(trade_id[1]) + 1

    requested_user = db.execute('SELECT request_id FROM trades where trade_id = ? GROUP BY request_id', [trade_id[1]])
    requested_user = requested_user.fetchone()

    delete_id_r = db.execute('SELECT delete_id FROM trades where trade_id = ?', [trade_id2])
    delete_id_r = delete_id_r.fetchall()

    requested_from = db.execute('SELECT card_id FROM trades WHERE trade_id = ?', [trade_id2])
    requested_from = requested_from.fetchall()

    offered = db.execute('SELECT card_id FROM trades WHERE trade_id = ?', [trade_id[1]])
    offered = offered.fetchall()

    delete_id_o = db.execute('SELECT delete_id FROM trades WHERE trade_id = ?', [trade_id[1]])
    delete_id_o = delete_id_o.fetchall()

    i = 0
    for card in requested_from:
        db.execute('INSERT INTO collection(card_id, user_id) VALUES(?, ?)', [card[0], requested_user[0]])
        db.execute('DELETE FROM collection WHERE delete_id = ? ', [delete_id_r[0][i]])
        i += 1

    j = 0
    for card in offered:
        db.execute('INSERT INTO collection(card_id, user_id) VALUES(?, ?)', [card[0], session['current_user']])
        db.execute('DELETE FROM collection WHERE delete_id = ? AND user_id = ?', [delete_id_o[0][j], session['current_user']])
        j += 1

    db.execute('DELETE FROM trades WHERE trade_id = ? AND trade_id = ?', [trade_id[1], trade_id2])

    db.commit()

    return redirect(url_for('your_inventory'))


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
    cur = db.execute('SELECT card_id FROM marketplace WHERE market_id=?', [market_id])
    card = cur.fetchone()

    image = db.execute('SELECT image FROM store WHERE card_id=?', [card[0]])
    image = image.fetchone()

    db.execute('INSERT INTO collection(card_id, user_id, image) VALUES(?, ?, ?)',
               [card[0], session['current_user'], image[0]])
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

    card_price = db.execute("SELECT price FROM marketplace WHERE market_id=?", [market_id])
    card_price = card_price.fetchone()
    broke_check = purchase(card_price[0])
    if broke_check:
        return redirect(url_for('marketplace'))
    add_cards(market_id)
    wallet_change = -1 * card_price[0]
    db.execute('INSERT INTO transactions(user_id, card_id, wallet_change) VALUES (?, ?, ?)',
               [session['current_user'], card_id, wallet_change])

    wallet_change_out = card_price[0]
    user_id_out = db.execute('SELECT user_id FROM marketplace WHERE market_id=?', [market_id])
    user_id_out = user_id_out.fetchone()
    sell(card_price[0], user_id_out)
    db.execute('INSERT INTO transactions(user_id, card_id, wallet_change) VALUES (?, ?, ?)',
               [user_id_out[0], card_id, wallet_change_out])

    db.execute('DELETE FROM marketplace WHERE market_id=?', [market_id])

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
    user_wallet = user_wallet.fetchone()
    add_balance = (user_wallet[0] + amount)

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


