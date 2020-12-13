import os

""" Common class for the constants related to database  """

DB_CONNECTION_URL = "postgres://postgres:postgres@localhost:5432/communitu-db"
# DB_CONNECTION_URL = "postgres://octzatlxqcygjs:561356912cd3a347f11e24eb2fb215a29af9025d942c55b6e733e9048af6bafc@ec2-52-44-235-121.compute-1.amazonaws.com:5432/d5k5c10dtjsul9"

""" Table names """
EVENT_TABLE_NAME = "event"
USER_TABLE_NAME = "_user"
CLUB_TABLE_NAME = "club"
COMMENT_TABLE_NAME = "comment"
AUTHORITY_TABLE_NAME = "authority"
NOTIFICATION_TABLE_NAME = "notification"
NOTIFICATION_TYPE_TABLE_NAME = "NOTIFICATION_TYPE"
LINKER_CLUB_USER_EXECUTIVE_TABLE_NAME = "LINKER_CLUB_USER_EXECUTIVE"
LINKER_CLUB_USER_PARTICIPANT_TABLE_NAME = "LINKER_CLUB_USER_PARTICIPANT"
LINKER_COMMENT_REPLY_TABLE_NAME = "LINKER_COMMENT_REPLY"
LINKER_USER_AUTHORITY_TABLE_NAME = "LINKER_USER_AUTHORITY"
LINKER_EVENT_USER_PARTICIPANT_TABLE_NAME = "LINKER_EVENT_USER_PARTICIPANT"
EVENT_REGISTRATION_QUESTION_TABLE_NAME = "EVENT_REGISTRATION_QUESTION"
EVENT_REGISTRATION_QUESTION_OPTION_TABLE_NAME = "EVENT_REGISTRATION_QUESTION_OPTION"
EVENT_REGISTRATION_QUESTION_USER_OPTION_ANSWER_TABLE_NAME = "EVENT_REGISTRATION_QUESTION_USER_OPTION_ANSWER"
EVENT_REGISTRATION_QUESTION_USER_TEXT_ANSWER_TABLE_NAME = "EVENT_REGISTRATION_QUESTION_USER_TEXT_ANSWER"

""" All tables ordered by most dependent to less dependent table """
ALL_TABLES_ = [LINKER_CLUB_USER_EXECUTIVE_TABLE_NAME,
               LINKER_CLUB_USER_PARTICIPANT_TABLE_NAME,
               LINKER_COMMENT_REPLY_TABLE_NAME,
               LINKER_USER_AUTHORITY_TABLE_NAME,
               LINKER_EVENT_USER_PARTICIPANT_TABLE_NAME,
               EVENT_REGISTRATION_QUESTION_USER_TEXT_ANSWER_TABLE_NAME,
               EVENT_REGISTRATION_QUESTION_USER_OPTION_ANSWER_TABLE_NAME,
               EVENT_REGISTRATION_QUESTION_OPTION_TABLE_NAME,
               EVENT_REGISTRATION_QUESTION_TABLE_NAME,
               NOTIFICATION_TYPE_TABLE_NAME,
               NOTIFICATION_TABLE_NAME,
               AUTHORITY_TABLE_NAME,
               COMMENT_TABLE_NAME,
               CLUB_TABLE_NAME,
               USER_TABLE_NAME,
               EVENT_TABLE_NAME]

""" Initial statements  """
EVENT_TABLE_INIT_STAT = """CREATE TABLE IF NOT EXISTS EVENT (
            ID SERIAL PRIMARY KEY,
            TITLE VARCHAR(255),
            EXPLANATION TEXT,
            START_DATE TIMESTAMP,
            END_DATE TIMESTAMP,
            QUOTA INTEGER,
            CREATED_BY INTEGER REFERENCES club(id) ON DELETE CASCADE,
            CREATED_AT TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            UPDATED_AT TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
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
            PROFILE_PHOTO_URL TEXT,
            HEADER_PHOTO_URL TEXT,
            EMAIL TEXT,
            TWITTER_URL TEXT,
            INSTAGRAM_URL TEXT,
            FACEBOOK_URL TEXT,
            DISCORD_URL TEXT,
            TELEGRAM_URL TEXT,
            CREATED_BY INTEGER REFERENCES _user(id) ON DELETE CASCADE,
            CREATED_AT TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            )"""

LINKER_CLUB_USER_EXECUTIVE_TABLE_INIT_STAT = """CREATE TABLE IF NOT EXISTS LINKER_CLUB_USER_EXECUTIVE (
            CLUB_ID INTEGER REFERENCES club(id) ON DELETE CASCADE,
            USER_ID INTEGER REFERENCES _user(id) ON DELETE CASCADE,
            PRIMARY KEY (CLUB_ID, USER_ID)
            )"""

LINKER_CLUB_USER_PARTICIPANT_TABLE_INIT_STAT = """CREATE TABLE IF NOT EXISTS LINKER_CLUB_USER_PARTICIPANT(
            CLUB_ID INTEGER REFERENCES club(id) ON DELETE CASCADE,
            USER_ID INTEGER REFERENCES _user(id) ON DELETE CASCADE,
            PRIMARY KEY (CLUB_ID, USER_ID)
            )"""

LINKER_EVENT_USER_PARTICIPANT_TABLE_INIT_STAT = """CREATE TABLE IF NOT EXISTS LINKER_EVENT_USER_PARTICIPANT(
            EVENT_ID INTEGER REFERENCES event(id) ON DELETE CASCADE,
            USER_ID INTEGER REFERENCES _user(id) ON DELETE CASCADE,
            PRIMARY KEY (EVENT_ID, USER_ID)
            )"""

COMMENT_TABLE_INIT_STAT = """CREATE TABLE IF NOT EXISTS COMMENT (
            ID SERIAL PRIMARY KEY,
            CONTENT TEXT,
            USER_ID INTEGER REFERENCES _user(id) ON DELETE CASCADE,
            EVENT_ID INTEGER REFERENCES event(id) ON DELETE CASCADE,
            CREATED_AT TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            UPDATED_AT TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            )"""

LINKER_COMMENT_REPLY_TABLE_INIT_STAT = """CREATE TABLE IF NOT EXISTS LINKER_COMMENT_REPLY (
            COMMENT_ID INTEGER REFERENCES comment(id) ON DELETE CASCADE,
            REPLY_TO INTEGER REFERENCES comment(id) ON DELETE CASCADE,
            PRIMARY KEY (COMMENT_ID, REPLY_TO)
            )"""

AUTHORITY_TABLE_INIT_STAT = """CREATE TABLE IF NOT EXISTS AUTHORITY (
            ID SERIAL PRIMARY KEY,
            AUTHORITY VARCHAR(255)
            )"""

LINKER_USER_AUTHORITY_TABLE_INIT_STAT = """CREATE TABLE IF NOT EXISTS LINKER_USER_AUTHORITY (
            USER_ID INTEGER REFERENCES _user(id) ON DELETE CASCADE,
            AUTHORITY_ID INTEGER REFERENCES authority(id) ON DELETE CASCADE,
            PRIMARY KEY (USER_ID, AUTHORITY_ID)
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
            UPDATED_AT TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
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

NOTIFICATION_TABLE_INIT_STAT = """CREATE TABLE IF NOT EXISTS NOTIFICATION (
            ID SERIAL PRIMARY KEY,
            AVATAR_URL TEXT,
            SENDER_URL VARCHAR(255),
            SENDER_NAME VARCHAR(255),
            RECIPIENT_ID INTEGER REFERENCES _user(id) ON DELETE CASCADE,
            NOTIFICATION_TYPE INTEGER REFERENCES notification_type(id) ON DELETE CASCADE,
            IS_READ BOOLEAN,
            CREATED_AT TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            )"""

NOTIFICATION_TYPE_TABLE_INIT_STAT = """CREATE TABLE IF NOT EXISTS NOTIFICATION_TYPE (
            ID SERIAL PRIMARY KEY,
            TYPE TEXT,
            MESSAGE TEXT
            )"""
