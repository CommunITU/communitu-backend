""" Common class for the constants related to database  """

DB_CONNECTION_URL = "postgres://postgres:postgres@localhost:5432/communitu-db"

EVENTS_DB_TABLE_NAME = "event"
EVENTS_DB_TABLE_INIT_STAT = """CREATE TABLE IF NOT EXISTS EVENT (
            ID SERIAL PRIMARY KEY,
            TITLE TEXT,
            DESCRIPTION TEXT,
            START_DATE DATE,
            END_DATE DATE,
            CREATE_DATE DATE,
            UPDATE_DATE DATE,
            QUOTA INTEGER
            )"""
