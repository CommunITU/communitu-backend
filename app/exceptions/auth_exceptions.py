""" Contains exception classes related with the authentication problems """


class AuthCredentialsError(Exception):
    """ Raises if credentials are not correct. """

    def __init__(self, msg):
        self.msg = msg
