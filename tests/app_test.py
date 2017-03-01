import unittest
import app
import flask


class AppTest(unittest.TestCase):

    def setUp(self):
        app.app.config['TESTING'] = True
        self.app = app.app.test_client()

    def test_flask_object(self):
        self.assertIsInstance(app.app, flask.Flask)

    def test_validate_registry_url_in_browser(self):
        url = b'http://localhost:5000/v2'

        rv = self.app.get('/')

        self.assertIn(url, rv.data)