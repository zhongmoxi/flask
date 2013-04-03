import os
import flaskr
import unittest
import tempfile


class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, self.db_filename = tempfile.mkstemp()
        flaskr.app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + self.db_filename
        flaskr.app.config['TESTING'] = True
        self.app = flaskr.app.test_client()
        flaskr.db.create_all()
        test_user = flaskr.User('test_user', 'apple0109')
        flaskr.db.session.add(test_user)
        flaskr.db.session.commit()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(self.db_filename)

    def test_unlogin_entry(self):
        rv = self.app.get('/')
        assert 'Unbelievable. No entries here so far' in rv.data

    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def test_login_logout(self):
        rv = self.login('test_user', 'apple0109')
        assert 'You were logged in' in rv.data
        rv = self.logout()
        assert 'You were logged out' in rv.data
        rv = self.login('test_userx', 'default')
        assert 'Invalid username' in rv.data
        rv = self.login('test_user', 'apple0109x')
        assert 'Invalid password' in rv.data

    def test_messages(self):
        self.login('test_user', 'apple0109')
        rv = self.app.post('/add', data=dict(title='<Hello>',
                           text='<strong>HTML</strong> allowed here'), follow_redirects=True)
        assert 'No entries here so far' not in rv.data
        assert '&lt;Hello&gt;' in rv.data
        assert '<strong>HTML</strong> allowed here' in rv.data
        assert 'test_user' in rv.data
        # assert time.strftime('%Y-%m-%d', time.localtime(time.time())) in rv.data
        rv = self.app.post('/add', data=dict(title='markdown', text=' **bold text**'), follow_redirects=True)
        assert '**bold text**' not in rv.data
        assert 'bold text' in rv.data

    def test_edit(self):
        self.login('test_user', 'apple0109')
        text = "I'm moxi ge"
        rv = self.app.post('/add', data=dict(title='<Hello>', text=text), follow_redirects=True)
        rv = self.app.get('/entry/1')
        assert text in rv.data
        text2 = "I'm moxi ge 2"
        rv = self.app.post('/entry/1/edit', data=dict(title='Hello',
                            text=text2), follow_redirects=True)

        rv = self.app.get('/entry/1')
        assert text2 in rv.data
        self.app.get('/entry/1/delete')
        rv = self.app.get('/entry/1')
        assert rv.status_code == 404

if __name__ == '__main__':
    unittest.main()
