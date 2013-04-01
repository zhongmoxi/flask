import os
import flaskr
import unittest
import tempfile

class FlaskrTestCase(unittest.TestCase):
    def setUp(self):
        self.app = flaskr.app.test_client()
    
    def test_show_entry(self):
        rv = self.app.get('/')
        assert 'moxi'

if __name__ == '__main__':
    unittest.main()
