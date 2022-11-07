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

    if __name__ == '__main__':
        unittest.main()


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
        assert b'No entries here so far' in rv.data

    def test_messages(self):
        rv = self.app.post('/add', data=dict(
            title='<Hello>',
            text='<strong>HTML</strong> allowed here'
        ), follow_redirects=True)
        assert b'No entries here so far' not in rv.data
        assert b'&lt;Hello&gt;' in rv.data
        assert b'<strong>HTML</strong> allowed here' in rv.data

    def table_test(self):
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