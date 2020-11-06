""" Contains all database-related exception classes """


class DatabaseConnectionError(Exception):
    """ Raises if database connection failed. """

    def __init__(self, msg):
        self.msg = msg
