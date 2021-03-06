""" Contains exception classes related with the authentication problems """


class AuthCredentialsError(Exception):
    """ Raises if credentials are not correct. """

    def __init__(self, msg):
        self.msg = msg


class UserNotAuthenticatedError(Exception):
    """   Raises if user is not authenticated. """

    def __init__(self, msg):
        self.msg = msg


class NoSuchUserError(Exception):
    """   Raises if there is not an user with given parameters """

    def __init__(self, msg):
        self.msg = msg
