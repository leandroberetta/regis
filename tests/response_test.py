import unittest
from regis import error
from regis.response import generate_success_response, generate_error_response


class ResponseTest(unittest.TestCase):

    def test_generate_success_response(self):
        response = generate_success_response(['hello-world', 'postgres'])

        self.assertEqual(response, {'data': ['hello-world', 'postgres']})

    def test_generate_connection_error_response(self):
        response = generate_error_response(error.ConnectionError())

        self.assertEqual(response, {'error': {'message': 'ConnectionError', 'code': 1000}})
