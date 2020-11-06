from functools import wraps
import psycopg2 as dbapi2
from psycopg2._psycopg import OperationalError

from app.constants.database_constants import DB_CONNECTION_URL
from app.constants.error_messages import DB_CONN_ERR
from app.exceptions.database_exceptions import DatabaseConnectionError

""" Database utils the for the application  """


def require_sql_connection(func):
    """
    Decorator for the functions which requires the database connection.
    Creates the database connection and passes it as an argument to given function .

    :param func: The function to be executed.
    :return: Returns the result/return value of the func.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            with dbapi2.connect(DB_CONNECTION_URL) as connection:
                result = func(connection=connection, *args, **kwargs)
            return result
        except OperationalError:
            raise DatabaseConnectionError(DB_CONN_ERR)

    return wrapper
