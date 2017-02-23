import unittest
from unittest import mock

import sys, os

print(os.path.dirname(__file__))
sys.path.insert(0, os.path.dirname(__file__))

import requests
from regis import error
from regis.registry import Registry


class TestRegistry(unittest.TestCase):

    def test_create_minimal_configured_registry(self):
        registry = Registry()

        self.assertEqual(registry.host, 'localhost')
        self.assertEqual(registry.port, 5000)

    def test_create_registry_with_credentials(self):
        registry = Registry()

        registry.set_credentials('username', 'password')

        self.assertEqual(registry.username, 'username')
        self.assertEqual(registry.password, 'password')

        self.assertIn('auth', registry.http_params)

    def test_create_registry_with_ssl(self):
        registry = Registry()

        registry.set_ssl_certificate('/path/to/ssl/cert.crt')

        self.assertEqual(registry.ssl, '/path/to/ssl/cert.crt')
        self.assertEqual(registry.http_params['verify'], '/path/to/ssl/cert.crt')

    def test_create_registry_ignoring_ssl(self):
        registry = Registry()

        registry.ignore_ssl()

        self.assertEqual(registry.ssl, False)
        self.assertEqual(registry.http_params['verify'], False)

    def test_http_params_contains_docker_v2_header(self):
        registry = Registry()

        self.assertEqual(registry.http_params['headers']['Accept'],
                         'application/vnd.docker.distribution.manifest.v2+json')

    def test_get_url_with_https(self):
        registry = Registry()

        registry.set_credentials('username', 'password')

        url = registry.get_url('_catalog')

        self.assertEqual(url, 'https://localhost:5000/v2/_catalog')

    def test_get_url_with_http(self):
        registry = Registry()

        url = registry.get_url('_catalog')

        self.assertEqual(url, 'http://localhost:5000/v2/_catalog')

    def request_get_mock_success(*args, **kwargs):

        class MockResponse:

            def __init__(self, data):
                self.data = data

            def json(self):
                return self.data

        if '_catalog' in args[0]:
            return MockResponse({'repositories': ['hello-world', 'postgres']})

    @mock.patch('requests.get', side_effect=request_get_mock_success)
    def test_get_images(self, mock_obj):
        registry = Registry()

        images_reponse = registry.get_images()

        self.assertEqual(images_reponse, ['hello-world', 'postgres'])
        self.assertIn(mock.call(registry.get_url('_catalog'), **registry.http_params), mock_obj.call_args_list)

    def request_get_mock_error(*args, **kwargs):

        if '_catalog' in args[0]:
            raise requests.exceptions.ConnectionError

    @mock.patch('requests.get', side_effect=request_get_mock_error)
    def test_get_images_with_connection_error(self, mock_obj):
        registry = Registry()

        self.assertRaises(error.ConnectionError, registry.get_images)
        self.assertIn(mock.call(registry.get_url('_catalog'), **registry.http_params), mock_obj.call_args_list)
