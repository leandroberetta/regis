from enum import Enum


class Errors(Enum):
    CONNECTION_ERROR = (1000, "ConnectionError")
    INTEGRITY_ERROR = (1001, "IntegrityError")


class Error(Exception):
    """ Base class for errors. """

    def __init__(self, code, message):
        self.code = code
        self.message = message

    def __str__(self):
        return 'Error: {0} - {1}'.format(self.code, self.message)


class ConnectionError(Error):

    def __init__(self):
        super().__init__(*Errors.CONNECTION_ERROR.value)


class IntegrityError(Error):

    def __init__(self):
        super().__init__(*Errors.INTEGRITY_ERROR.value)
