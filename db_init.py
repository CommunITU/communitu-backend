from app.constants.database_constants import ALL_TABLES_INIT_STATES
from app.util.db_util import require_sql_connection, clean_database, PopulateInitialDatabase


@require_sql_connection
def init_tables(connection):
    with connection.cursor() as cursor:
        for init_stat in ALL_TABLES_INIT_STATES:
            cursor.execute(init_stat)


if __name__ == "__main__":
    #clean_database()
    init_tables()
    PopulateInitialDatabase.populate()
