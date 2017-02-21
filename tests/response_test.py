import unittest
from response import Error, generate_success_response, generate_error_response


class TestResponse(unittest.TestCase):

    def test_generate_success_response(self):
        response = generate_success_response(['hello-world', 'postgres'])

        self.assertEqual(response, {'data': ['hello-world', 'postgres']})

    def test_generate_connection_error_response(self):
        response = generate_error_response(Error.CONNECTION_ERROR)

        self.assertEqual(response, {'error': {'message': 'ConnectionError', 'code': 1000}})

if __name__ == '__main__':
    unittest.main()
