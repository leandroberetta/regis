from enum import Enum


class Errors(Enum):
    CONNECTION_ERROR = (1000, "ConnectionError")
    INTEGRITY_ERROR = (1001, "IntegrityError")
    NOT_FOUND_ERROR = (1002, "NotFoundError")


class Error(Exception):

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


class NotFoundError(Error):

    def __init__(self):
        super().__init__(*Errors.NOT_FOUND_ERROR.value)
