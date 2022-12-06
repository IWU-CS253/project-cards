import os
import app as flaskr
import unittest
import tempfile

# Some unit tests taken from past Flaskr assignments (source: https://sun.iwu.edu/~mliffito/flask_tutorial/testing.html)
# This unit tests file is going to be an ongoing file as we continue to add new features and update our application.


class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
        flaskr.app.testing = True
        self.app = flaskr.app.test_client()
        with flaskr.app.app_context():
            flaskr.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(flaskr.app.config['DATABASE'])

    def test_empty_db(self):
        rv = self.app.get('/')
        assert b'' in rv.data

    if __name__ == '__main__':
        unittest.main()

    def test_create_user(self):
        rv = self.app.post('/create_user', data=dict(
            choose_username='username',
            choose_password='password',
            choose_email='email'
        ))
        assert b'Account Created' in rv.data
        rv = self.app.post('/create_user', data=dict(
            choose_username='username',
            choose_password='password',
            choose_email='testingusername'
        ))
        assert b'Username already taken'
        rv = self.app.post('/create_user', data=dict(
            choose_username='testingemail',
            choose_password='password',
            choose_email='email'
        ))
        assert b'Email is already taken'

    def login(self, username, password):
        # Creates a user to login with
        self.app.post('/create_user', data=dict(
            choose_username='username',
            choose_password='password',
            choose_email='email'
        ))
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def test_login_logout(self):
        rv = self.login('username', 'password')
        assert b'You were logged in' in rv.data
        rv = self.logout()
        assert b'You were logged out' in rv.data
        rv = self.login('fakeusername', 'password')
        assert b'Invalid username' in rv.data
        rv = self.login('username', 'fakepassword')
        assert b'Invalid password' in rv.data

    def test_buy_individual_card(self):
        self.app.post('/create_user', data=dict(
            choose_username='username',
            choose_password='password',
            choose_email='email'
        ))
        self.login('username', 'password')

        self.app.post('/add_cards', data=dict(
            id=1,

        ))

        rv = self.app.get('/your_inventory')
        assert b'1' in rv.data
        assert b'BURGER' in rv.data
        assert b'0.45' in rv.data

    def test_table_test(self):
        rv = self.app.post('/', data=dict(
            card_id='1',
            name='name',
            rank='3',
            type='rare',
            pack='basic',
            amount='1',
        ), follow_redirects=True)
        assert b'No entries here so far' not in rv.data
        assert b'1' in rv.data
        assert b'name' in rv.data
        assert b'3' in rv.data
        assert b'rare' in rv.data
        assert b'basic' in rv.data
        assert b'1' in rv.data