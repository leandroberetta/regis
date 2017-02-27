import unittest
from regis import error


class ErrorTest(unittest.TestCase):

    def test_to_str(self):
        err = error.ConnectionError()

        self.assertEqual(err.__str__(), 'Error: 1000 - ConnectionError')


