""" Common class for the constants related to database  """

DB_CONNECTION_URL = "postgres://postgres:postgres@localhost:5432/communitu-db"

""" Table names """
EVENT_DB_TABLE_NAME = "event"
USER_DB_TABLE_NAME = "_user"

""" Initial statements  """
EVENT_DB_TABLE_INIT_STAT = """CREATE TABLE IF NOT EXISTS EVENT (
            ID SERIAL PRIMARY KEY,
            TITLE VARCHAR(60),
            EXPLANATION TEXT,
            START_DATE TIMESTAMP,
            END_DATE TIMESTAMP,
            CREATED_AT TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            UPDATED_AT TIMESTAMP,
            QUOTA INTEGER,
            OWNER_ID INTEGER REFERENCES _user(id) ON DELETE CASCADE
            )"""

USER_DB_TABLE_INIT_STAT = """CREATE TABLE IF NOT EXISTS _USER (
            ID SERIAL PRIMARY KEY,
            EMAIL VARCHAR(254) UNIQUE,
            PASSWORD VARCHAR (60),
            NAME VARCHAR (60),
            SURNAME VARCHAR (60),
            CREATED_AT TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            )"""
