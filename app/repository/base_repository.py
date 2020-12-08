from app.util.db_utils import require_sql_connection


class BaseRepository:
    """ Base class for the repositories"""

    def __init__(self, table):
        self.table = table

    @classmethod
    @require_sql_connection
    def initialize_table(cls, connection, initialization_statement):
        """

        :param connection:          Provided by @require_sql_decorator. Do not specify in function calls explicitly.
        :param initialization_statement:    Init. statement of the table.
        """
        with connection.cursor() as cursor:
            cursor.execute(initialization_statement)

    def populate_table(self, initial_data):
        """
        Populate table with initial data.
        :param initial_data:    An array structure contains initial data for the table
        """

        for row in initial_data:
            self.create(row)

    @require_sql_connection
    def create(self, data, connection=None):
        """
        Creates new record on database based on passed data.

        :param data:        The dictionary that contains the data of the record will be created.
        :param connection:  Provided by @require_sql_decorator. Do not specify in function calls explicitly.
        """
        with connection.cursor() as cursor:
            create_statement = """INSERT INTO {}({}) VALUES({})
                                """.format(self.table, str.join(", ", data.keys()),
                                           str.join(", ", ["'{}'".format(str(val)) for val in data.values()]))
            cursor.execute(create_statement)

    @require_sql_connection
    def select(self, connection=None, return_columns=[], from_tables=[],
               where={}, limit=None, order_by={}):
        """
        Query the database based on specified conditions.

        :param connection:          Provided by @require_sql_decorator. Do not specify in function calls explicitly.
        :param return_columns:      The list of wanted column names.
        :param from_tables:         The list of table names that columns are to be selected from. Multiple tables names
                                    are usually required in 'JOIN' queries. So, not necessary to pass that argument if
                                    only one table (self.table) will be queried.
        :param where:               The dictionary of where conditions. The column names should be specified as key and
                                    conditions as value.
        :param limit:               The number of records that will be returned.
        :param order_by:            The dictionary of order by conditions. The keys of dictionary should be the
                                    column names, values should be 'ASC' or 'DESC'.

        :return: Query result
        """
        with connection.cursor() as cursor:

            # Add 'select' clause
            select_statement = " SELECT {}".format(str.join(", ", return_columns) if return_columns else "* ")

            # Add 'from' clause
            select_statement += " FROM {}".format((str.join(", ", from_tables)) if from_tables else self.table)

            # Add 'where' clause
            if where:
                select_statement += " WHERE " + str.join(" AND ", ["{}='{}'".format(w, where[w]) for w in where.keys()])

            # Add 'limit' clause
            if limit:
                select_statement += " LIMIT " + str(limit)

            # Add 'order_by' clause
            if order_by:
                select_statement += " ORDER BY " + str.join(" ,",
                                                            ["{} {}".format(o, order_by[o]) for o in order_by.keys()])
            cursor.execute(select_statement)
            result = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]

            # Map columns names with the columns values which are in the result array.
            result_dict = [dict(map(lambda x, y: (x, y), column_names, event)) for event in result]
            return result_dict
