import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, g, redirect, url_for, render_template, flash, session
import werkzeug

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


@app.route('/')
def show_entries():
    return render_template('login.html')


@app.route('/your_inventory')
def your_inventory():
    db = get_db()

    if "rank" in request.args:
        cur = db.execute('SELECT card_id, name, rank FROM collection WHERE rank = ? ORDER BY card_id',
                         [request.args["rank"]])
    else:
        cur = db.execute('SELECT card_id, name, rank FROM collection ORDER BY card_id')

    collection = cur.fetchall()
    cur = db.execute('SELECT DISTINCT rank FROM collection ORDER BY card_id')
    ranks = cur.fetchall()

    return render_template('your_inventory.html', collection=collection, ranks=ranks)


@app.route('/marketplace')
def marketplace():
    return render_template('marketplace.html')


@app.route('/connect_with_friends')
def connect_with_friends():
    return render_template('friends.html')

@app.route('/trade_page')
def trade_page():
    return render_template('trade_page.html')


@app.route('/new_user_info', methods=['POST'])
def new_user_info():
    return render_template('create_user.html')


@app.route('/create_user', methods=['POST'])
def create_user():
    db = get_db()
    chosen_username = request.form['choose_username']
    hashed_pw = werkzeug.security.generate_password_hash(request.form['choose_password'], method='pbkdf2:sha256',
                                                         salt_length=16)
    chosen_email = request.form['choose_email']
    db.execute('insert into users (username, password, email) values (?, ?, ?)',
               [chosen_username, hashed_pw, chosen_email])
    db.commit()
    return render_template('login.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    db = get_db()
    pswd = db.execute("SELECT password FROM users WHERE username=?", [request.args['username']])
    pw_check = pswd.fetchall()
    #commented this block out because if the username is invalid, the query will fail
    #so we dont need to check it explicitly
    #if request.args['username'] != username:
    #    error = 'Invalid username'
    if not werkzeug.security.check_password_hash(pw_check, request.args['password']):
        error = 'Invalid password'
    else:
        session['logged_in'] = True
        flash('You were logged in')
        current_user = db.execute("SELECT user_id FROM users WHERE username=?", [request.form['username']])
        return redirect(url_for('home'))
    return redirect(url_for('home'))



 #@app.route('/logout')
 #def logout():
#   session.pop('logged_in', None)
#   flash('You were logged out')
#   return redirect(url_foadd r('login'))
     
