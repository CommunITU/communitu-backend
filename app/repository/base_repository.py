from app.util.db_utils import require_sql_connection


class BaseRepository:
    """ Base class for the repositories"""

    def __init__(self, table):
        self.table = table

    @require_sql_connection
    def initialize_table(self, connection, initialization_statement):
        with connection.cursor() as cursor:
            cursor.execute(initialization_statement)

    @require_sql_connection
    def create(self, data, connection=None):
        with connection.cursor() as cursor:
            create_statement = """INSERT INTO {}({}) VALUES({})
                                """.format(self.table, str.join(", ", data.keys()),
                                           str.join(", ", ["'{}'".format(str(val)) for val in data.values()]))
            cursor.execute(create_statement)
            print("[OK] Created new event: {} ".format(data["title"]))
