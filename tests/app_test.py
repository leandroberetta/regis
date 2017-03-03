import unittest
import app
import flask
from unittest.mock import MagicMock, patch
from regis.registry import Registry


class AppTest(unittest.TestCase):

    def setUp(self):
        app.app.config['TESTING'] = True
        self.app = app.app.test_client()

    def test_flask_object(self):
        self.assertIsInstance(app.app, flask.Flask)

    def test_validate_error_in_browser(self):
        url = b'http://hostname:6000/v2'

        registry = Registry(host='hostname', port=6000)
        setattr(app, 'registry', registry)

        rv = self.app.get('/')

        self.assertIn(b'Error', rv.data)

    def test_validate_registry_url_in_browser(self):
        url = b'http://hostname:6000/v2'

        registry = Registry(host='hostname', port=6000)
        registry.get_images = MagicMock(return_value=({}, None))
        setattr(app, 'registry', registry)

        rv = self.app.get('/')

        self.assertIn(url, rv.data)

    def test_validate_images_in_browser(self):
        images = [b'httpd', b'nginx']

        registry = Registry()
        registry.get_images = MagicMock(return_value=({'httpd', 'nginx'}, None))
        setattr(app, 'registry', registry)

        rv = self.app.get('/')

        self.assertIn(images[0], rv.data)
        self.assertIn(images[1], rv.data)

    def test_validate_get_images_with_link_not_none(self):
        images = [b'httpd', b'nginx', b'python', b'java']

        registry = Registry()
        registry.get_images = MagicMock(return_value=({'httpd', 'nginx'}, None))
        setattr(app, 'registry', registry)

        rv = self.app.get('/')

        self.assertIn(images[0], rv.data)
        self.assertIn(images[1], rv.data)

    def test_escape_tag(self):
        tag = 'redhat/fuse:6.3.0'

        escaped_tag = app.escape_tag(tag)

        self.assertEqual(escaped_tag, 'redhat_fuse:6_3_0')