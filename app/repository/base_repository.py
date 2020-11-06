from app.util.db_utils import require_sql_connection


class BaseRepository:
    """ Base class for the repositories"""

    def __init__(self, table):
        self.table = table

    @require_sql_connection
    def initialize_table(self, connection, initialization_statement):
        with connection.cursor() as cursor:
            cursor.execute(initialization_statement)
