import unittest
import app
import flask


class AppTest(unittest.TestCase):

    def test_flask_object(self):
        self.assertIsInstance(app.app, flask.Flask)
