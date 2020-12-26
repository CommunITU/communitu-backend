import datetime
from psycopg2._psycopg import OperationalError
from functools import wraps
import psycopg2 as dbapi2
from app.constants.database_constants import DB_CONNECTION_URL
from app.constants.error_messages import DB_CONN_ERR
from app.exceptions.database_exceptions import DatabaseConnectionError

""" Database utils the for the application  """


def require_sql_connection(func):
    """
    Decorator for the functions which require the database connection.
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


@require_sql_connection
def clean_database(connection):
    """
    Remove all tables in database
    """
    with connection.cursor() as cursor:
        cursor.execute("DROP SCHEMA public CASCADE; CREATE SCHEMA public; ")


class PopulateInitialDatabase:
    """
        Populate database with the fake data for the initial state of the program.
    """

    @classmethod
    def populate(cls):
        from app.repository.user_repository import UserRepository as user_repo
        from app.repository.club_repository import ClubRepository as club_repo
        from app.repository.event_repository import EventRepository as event_repo
        from app.repository.authority_repository import AuthorityRepository as auth_repo
        cls.__user_repo = user_repo
        cls.__club_repo = club_repo
        cls.__event_repo = event_repo
        cls.__auth_repo = auth_repo

        cls.__populate_users()
        cls.__populate_clubs()
        cls.__populate_events()
        cls.__populate_authorities()
        # todo: IMPLEMENT RELATIONS ON EVENTS.

    @classmethod
    def __populate_users(cls):

        users = ({"email": "umut265@gmail.com", "password": "deneme", "name": "Umut Emre", "surname": "Bayramoglu"},
                 {"email": "uebayramoglu@gmail.com", "password": "deneme", "name": "Umut Emre 2",
                  "surname": "Bayramoglu 2"})

        for user in users:
            cls.__user_repo.create_user(user_data=user)

    @classmethod
    def __populate_clubs(cls):

        clubs = ({"name": "My Club 1", "description": "Hello My first club", "email": "umut265@gmail.com"},
                 {"name": "My Club 2", "description": "Hello My second club", "email": "umut265@gmail.com"})

        cls.__club_repo.create_club(club_data=clubs[0], user_id_who_created=1)
        cls.__club_repo.create_club(club_data=clubs[1], user_id_who_created=2)

    @classmethod
    def __populate_events(cls):

        events = ({"title": "My Event 1", "explanation": "Event description 1", "quota": 100, "created_by": 1,
                   "start_date": datetime.datetime.now(), "image_url": "event6.png",
                   "end_date": datetime.datetime.now() + datetime.timedelta(hours=2)},
                  {"title": "My Event 2", "explanation": "Event description 2", "quota": 300, "created_by": 2,
                   "start_date": datetime.datetime.now(), "image_url": "event5.png",
                   "end_date": datetime.datetime.now() + datetime.timedelta(hours=2)},
                  {"title": "My Event 3", "explanation": "Event description 3", "quota": 90, "created_by": 1,
                   "start_date": datetime.datetime.now(), "image_url": "event4.png",
                   "end_date": datetime.datetime.now() + datetime.timedelta(hours=2)},
                  {"title": "Youtube Talk", "explanation": "Event description 1", "quota": 65, "created_by": 1,
                   "start_date": datetime.datetime.now(), "image_url": "event3.png",
                   "end_date": datetime.datetime.now() + datetime.timedelta(hours=2)},
                  {"title": "Neuropsychology Day", "explanation": "Event description 2", "quota": 30, "created_by": 2,
                   "start_date": datetime.datetime.now(), "image_url": "event2.png",
                   "end_date": datetime.datetime.now() + datetime.timedelta(hours=2)},
                  {"title": "gRPC Workshop", "explanation": "Event description 3", "quota": 70, "created_by": 1,
                   "start_date": datetime.datetime.now(), "image_url": "event1.png",
                   "end_date": datetime.datetime.now() + datetime.timedelta(hours=2)}
                  )

        cls.__event_repo.create_event(event_data=events[0])
        cls.__event_repo.create_event(event_data=events[1])
        cls.__event_repo.create_event(event_data=events[2])
        cls.__event_repo.create_event(event_data=events[3])
        cls.__event_repo.create_event(event_data=events[4])
        cls.__event_repo.create_event(event_data=events[5])

    @classmethod
    def __populate_authorities(cls):

        authorities = ({"authority": "ADMIN"},
                       {"authority": "USER"})

        for authority in authorities:
            cls.__auth_repo.create_authority(authority)

        cls.__auth_repo.set_authority_of_user(authority="ADMIN", user_id=1)
        cls.__auth_repo.set_authority_of_user(authority="USER", user_id=2)
