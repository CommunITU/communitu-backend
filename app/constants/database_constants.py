""" Common class for the constants related to database  """

DB_CONNECTION_URL = "postgres://postgres:postgres@localhost:5432/communitu-db"

""" Table names """
# TODO ADD ALL TABLE NAMES
EVENT_DB_TABLE_NAME = "event"
USER_DB_TABLE_NAME = "_user"
CLUB_DB_TABLE_NAME = "club"
COMMENT_DB_TABLE_NAME = "comment"
AUTHORITY_DB_TABLE_NAME = "authority"

""" Initial statements  """
# TODO CREATE TABLES ABOUT : NOTIFICATIONS, FOLLOWERS

EVENT_TABLE_INIT_STAT = """CREATE TABLE IF NOT EXISTS EVENT (
            ID SERIAL PRIMARY KEY,
            TITLE VARCHAR(255),
            EXPLANATION TEXT,
            START_DATE TIMESTAMP,
            END_DATE TIMESTAMP,
            QUOTA INTEGER,
            CREATED_AT TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            UPDATED_AT TIMESTAMP WITH TIME ZONE
            )"""

USER_TABLE_INIT_STAT = """CREATE TABLE IF NOT EXISTS _USER (
            ID SERIAL PRIMARY KEY,
            EMAIL VARCHAR(255) UNIQUE,
            PASSWORD VARCHAR (255),
            NAME VARCHAR (255),
            SURNAME VARCHAR (255),
            CREATED_AT TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            )"""

CLUB_TABLE_INIT_STAT = """CREATE TABLE IF NOT EXISTS CLUB (
            ID SERIAL PRIMARY KEY,
            NAME VARCHAR(255) UNIQUE,
            DESCRIPTION TEXT,
            CREATED_AT TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            )"""

LINKER_CLUB_EVENT_TABLE_INIT_STAT = """CREATE TABLE IF NOT EXISTS LINKER_CLUB_EVENT (
            CLUB_ID INTEGER REFERENCES club(id) ON DELETE CASCADE,
            EVENT_ID INTEGER REFERENCES event(id) ON DELETE CASCADE 
            )"""

LINKER_CLUB_USER_EXECUTIVE_TABLE_INIT_STAT = """CREATE TABLE IF NOT EXISTS LINKER_CLUB_USER_EXECUTIVE (
            CLUB_ID INTEGER REFERENCES club(id) ON DELETE CASCADE,
            USER_ID INTEGER REFERENCES _user(id) ON DELETE CASCADE 
            )"""

LINKER_CLUB_USER_PARTICIPANT_TABLE_INIT_STAT = """CREATE TABLE IF NOT EXISTS LINKER_CLUB_USER_PARTICIPANT(
            CLUB_ID INTEGER REFERENCES club(id) ON DELETE CASCADE,
            USER_ID INTEGER REFERENCES _user(id) ON DELETE CASCADE 
            )"""

COMMENT_TABLE_INIT_STAT = """CREATE TABLE IF NOT EXISTS COMMENT (
            ID SERIAL PRIMARY KEY,
            CONTENT TEXT,
            USER_ID INTEGER REFERENCES _user(id) ON DELETE CASCADE,
            EVENT_ID INTEGER REFERENCES event(id) ON DELETE CASCADE,
            CREATED_AT TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            UPDATED_AT TIMESTAMP WITH TIME ZONE
            )"""

LINKER_COMMENT_REPLY_TABLE_INIT_STAT = """CREATE TABLE IF NOT EXISTS LINKER_COMMENT_REPLY (
            COMMENT_ID INTEGER REFERENCES comment(id) ON DELETE CASCADE,
            REPLY_TO INTEGER REFERENCES comment(id) ON DELETE CASCADE 
            )"""

AUTHORITY_TABLE_INIT_STAT = """CREATE TABLE IF NOT EXISTS AUTHORITY (
            ID SERIAL PRIMARY KEY,
            AUTHORITY VARCHAR(255)
            )"""

LINKER_USER_AUTHORITY_TABLE_INIT_STAT = """CREATE TABLE IF NOT EXISTS LINKER_USER_AUTHORITY (
            USER_ID INTEGER REFERENCES _user(id) ON DELETE CASCADE,
            AUTHORITY_ID INTEGER REFERENCES authority(id) ON DELETE CASCADE 
            )"""

EVENT_REGISTRATION_QUESTION_TABLE_INIT_STAT = """CREATE TABLE IF NOT EXISTS EVENT_REGISTRATION_QUESTION (
            ID SERIAL PRIMARY KEY,
            TEXT TEXT,
            EXPLANATION TEXT,
            IS_MANDATORY BOOLEAN,
            ORDER_NO INTEGER,
            TYPE_NO INTEGER,
            EVENT_ID INTEGER REFERENCES event(id) ON DELETE CASCADE,
            CREATED_AT TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            UPDATED_AT TIMESTAMP WITH TIME ZONE
            )"""

EVENT_REGISTRATION_QUESTION_OPTION_TABLE_INIT_STAT = """CREATE TABLE IF NOT EXISTS EVENT_REGISTRATION_QUESTION_OPTION (
            ID SERIAL PRIMARY KEY,
            OPTION TEXT,
            ORDER_NO INTEGER,
            QUESTION_ID INTEGER REFERENCES event_registration_question(id) ON DELETE CASCADE
            )"""

EVENT_REGISTRATION_QUESTION_USER_TEXT_ANSWER_TABLE_INIT_STAT = """CREATE TABLE IF NOT EXISTS 
                                                            EVENT_REGISTRATION_QUESTION_USER_TEXT_ANSWER (
            QUESTION_ID INTEGER REFERENCES event_registration_question(id) ON DELETE CASCADE,
            ANSWER TEXT
            )"""

EVENT_REGISTRATION_QUESTION_USER_OPTION_ANSWER_TABLE_INIT_STAT = """CREATE TABLE IF NOT EXISTS 
                                                            EVENT_REGISTRATION_QUESTION_USER_OPTION_ANSWER (
            QUESTION_OPTION_ID INTEGER REFERENCES event_registration_question_option(id) ON DELETE CASCADE,
            USER_ID INTEGER REFERENCES _user(id) ON DELETE CASCADE
            )"""
