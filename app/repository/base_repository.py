from app.util.db_util import require_sql_connection


class BaseRepository:
    """ Base class for the repositories"""

    @classmethod
    def __init__(cls, table):
        cls.table = table

    @classmethod
    @require_sql_connection
    def initialize_table(cls, connection, initialization_statement):
        """

        :param connection:          Provided by @require_sql_decorator. Do not specify in function calls explicitly.
        :param initialization_statement:    Init. statement of the table.
        """
        with connection.cursor() as cursor:
            cursor.execute(initialization_statement)

    @classmethod
    @require_sql_connection
    def add(cls, data, connection=None, table_name=None, return_id=False):
        """
        Creates new record on database based on passed data.

        :param data:        The dictionary that contains the data of the record will be created.
        :param connection:  Provided by @require_sql_decorator. Do not specify in function calls explicitly.
        :param table_name:  The table that new record to be added to.
        :param return_id:   Return id of added record if true,
        """
        with connection.cursor() as cursor:
            create_statement = """INSERT INTO {}({}) VALUES({})
                                """.format(table_name if table_name else cls.table,
                                           str.join(", ", data.keys()),
                                           str.join(", ", ["'{}'".format(str(val)) for val in data.values()]))
            if return_id:
                create_statement += " RETURNING id"

            cursor.execute(create_statement)
            return cursor.fetchone()[0] if return_id else None

    @classmethod
    @require_sql_connection
    def delete(cls, connection=None, table_name=None, where={}):
        """
        Creates new record on database based on passed data.

        :param connection:  Provided by @require_sql_decorator. Do not specify in function calls explicitly.
        :param table_name:  The table that new record to be deleted to.
        :param where:       The conditions of delete query.
        """
        with connection.cursor() as cursor:
            create_statement = """DELETE FROM {} WHERE {}
                                   """.format(table_name if table_name else cls.table,
                                              str.join(" AND ", ["{}='{}'".format(w, where[w]) for w in where.keys()]))

            cursor.execute(create_statement)

    @classmethod
    @require_sql_connection
    def update(cls, connection=None, table_name=None, set={}, where={}):
        """
        Updates the database record

        :param connection:  Provided by @require_sql_decorator. Do not specify in function calls explicitly.
        :param table_name:  The table that record to be updated in.
        :param set:         The new values of the record
        :param where:       The conditions of update query.
        """
        with connection.cursor() as cursor:
            create_statement = """UPDATE {} SET {} WHERE {}
                                      """.format(table_name if table_name else cls.table,
                                                 str.join(" , ",
                                                          ["{} ='{}'".format(c, set[c]) for c in set.keys()]),
                                                 str.join(" AND ",
                                                          ["{}='{}'".format(w, where[w]) for w in where.keys()]))

            cursor.execute(create_statement)

    @classmethod
    @require_sql_connection
    def select(cls, connection=None, return_columns=[], from_tables=[], join_statements=[],
               where={}, limit=None, offset=None, order_by={}):
        """
        Query the database based on specified conditions.

        :param connection:          Provided by @require_sql_decorator. Do not specify in function calls explicitly.
        :param return_columns:      The list of wanted column names.
        :param from_tables:         The list of table names that columns are to be selected from. Multiple tables names
                                    are usually required in 'JOIN' queries. So, not necessary to pass that argument if
                                    only one table (self.table) will be queried.
        :param join_statements      Array of hard-coded join statements.
        :param where:               The dictionary of where conditions. The column names should be specified as key and
                                    conditions as value.
        :param limit:               The number of records that will be returned.
        :param offset               Number of row to be skipped
        :param order_by:            The dictionary of order by conditions. The keys of dictionary should be the
                                    column names, values should be 'ASC' or 'DESC'.

        :return: Query result
        """
        with connection.cursor() as cursor:

            # Add 'select' clause
            select_statement = " SELECT {}".format(str.join(", ", return_columns) if return_columns else "* ")

            # Add 'from' clause
            select_statement += " FROM {}".format((str.join(", ", from_tables)) if from_tables else cls.table)

            # Add join statements
            if join_statements:
                select_statement += " {}".format(str.join(" ", join_statements))

            # Add 'where' clause
            if where:
                select_statement += " WHERE " + str.join(" AND ", ["{}='{}'".format(w, where[w]) for w in where.keys()])

            # Add 'order_by' clause
            if order_by:
                select_statement += " ORDER BY " + str.join(" ,",
                                                            ["{} {}".format(o, order_by[o]) for o in order_by.keys()])

            # Add 'limit' clause
            if limit:
                select_statement += " LIMIT " + str(limit)

            # Add 'offset' clause
            if offset:
                select_statement += " OFFSET " + str(offset)

            cursor.execute(select_statement)
            result = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]

            # Map columns names with the columns values which are in the result array.
            result_dict = [dict(map(lambda x, y: (x, y), column_names, event)) for event in result]
            return result_dict
