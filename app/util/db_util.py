import datetime
import os

from psycopg2._psycopg import OperationalError
from functools import wraps
import psycopg2 as dbapi2
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
            with dbapi2.connect(os.environ['DATABASE_URL']) as connection:
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

    @classmethod
    def __populate_users(cls):

        users = ({"email": "umut265@gmail.com", "password": "deneme", "name": "Umut Emre", "surname": "Bayramoglu",
                  'about_me': "Hello Everyone !", 'contact': "@uebayramoglu",
                  "profile_photo_url": "https://firebasestorage.googleapis.com/v0/b/communitu.appspot.com/o/images%2Fapp_images%2Fprofile_pic.png?alt=media&token=0d79339e-845c-4e42-ac87-4a674722f9b6"},
                 {"email": "uebayramoglu@gmail.com", "password": "deneme", "name": "Red",
                  "surname": "John", 'about_me': "Hello Everyone !", 'contact': "@uebayramoglu",
                  "profile_photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/04/Red-John-Smiley-Face.png/444px-Red-John-Smiley-Face.png"})

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

        event_text = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus interdum neque ut nisi 
        convallis porttitor. Curabitur nec lectus euismod, semper diam nec, dictum tellus. Nullam varius pellentesque 
        orci cursus facilisis.Aenean libero dolor, vehicula vel faucibus a, suscipit id eros. Phasellus a elit a quam 
        vehicula tempor. Integer maximus diam malesuadasodales commodo. Aliquam arcu massa, dictum quis eros ut, 
        finibus placerat nisi. Aliquam dui massa, vestibulum at nulla euismod,aliquet congue lacus. 
        Donec nec nulla consequat, congue neque at, gravida purus. Phasellus nisl erat, facilisis vitae neque sit amet,
         tincidunt iaculis tellus. Ut sed turpis in urna mollis sodales.
        In non lobortis tortor. Curabitur id dictum metus. Duis vel lobortis massa. Duis laoreet mi eget ornare aliquet. 
        Nam viverra ullamcorper risus. Mauris mattis ligula vitae nulla ullamcorper fermentum. Curabitur pharetra 
        imperdiet nisi a aliquam. Suspendisse ac dui neque placerat cursus elementum in orci. Phasellus id egestas elit,
         at lacinia est. Vivamus semper nunc sed diam lobortis pellentesquePhasellus elit odio, tristique vel dapibus 
         nec, semper sed justo. Aliquam suscipit eros ante, sed vehicula metus commodo ac. Morbi blandit nulla massa, 
         vitae consequat ligula pellentesque hendrerit. Aenean venenatis varius turpis a facilisis. In tempus quis leo 
         ut bibendum. Sed feugiat, nulla ut vestibulum cursus, eros metus porta nibh, vel dictum quam massa eu enim. 
         Mauris consequat pharetra orci, id pulvinar odio interdum et. Donec quis tincidunt tortor, sed pulvinar libero.
          Praesent facilisis auctor enim, eu varius orci venenatis ut. Etiam molestie elit a dui pellentesque lacinia. 
          Sed posuere bibendum."""

        events = ({"name": "My Event 1", "description": event_text, "quota": 100, "created_by": 1,
                   "start_date": datetime.datetime.now(),
                   "image_url": "https://firebasestorage.googleapis.com/v0/b/communitu.appspot.com/o/images%2Fevents%2Fevent1.png?alt=media&token=d6de8e88-c2f9-4be5-8bb3-9edb7528b8db",
                   "location": "Online",
                   "header_photo_url": None, "end_date": datetime.datetime.now() + datetime.timedelta(hours=2)},
                  {"name": "My Event 2", "description": event_text, "quota": 300, "created_by": 1,
                   "start_date": datetime.datetime.now(),
                   "image_url": "https://firebasestorage.googleapis.com/v0/b/communitu.appspot.com/o/images%2Fevents%2Fevent4.png?alt=media&token=2ea1b542-0efb-460f-89c3-e8020e3a8b13",
                   "location": "Online",
                   "header_photo_url": None, "end_date": datetime.datetime.now() + datetime.timedelta(hours=2)},
                  {"name": "My Event 3", "description": event_text, "quota": 90, "created_by": 1,
                   "start_date": datetime.datetime.now(),
                   "image_url": "https://firebasestorage.googleapis.com/v0/b/communitu.appspot.com/o/images%2Fevents%2Fevent6.png?alt=media&token=54ec616c-226f-4476-a7ef-da76ef95559b",
                   "location": "Online",
                   "header_photo_url": None, "end_date": datetime.datetime.now() + datetime.timedelta(hours=2)},
                  {"name": "Youtube Talk", "description": event_text, "quota": 65, "created_by": 1,
                   "start_date": datetime.datetime.now(),
                   "image_url": "https://firebasestorage.googleapis.com/v0/b/communitu.appspot.com/o/images%2Fevents%2Fevent3.png?alt=media&token=a5d207dd-ab71-4be0-8fa8-f725c7249bcd",
                   "location": "Online",
                   "header_photo_url": None, "end_date": datetime.datetime.now() + datetime.timedelta(hours=2)},
                  {"name": "Neuropsychology Day", "description": event_text, "quota": 30, "created_by": 1,
                   "start_date": datetime.datetime.now(),
                   "image_url": "https://firebasestorage.googleapis.com/v0/b/communitu.appspot.com/o/images%2Fevents%2Fevent6.png?alt=media&token=54ec616c-226f-4476-a7ef-da76ef95559b",
                   "location": "Online",
                   "header_photo_url": None, "end_date": datetime.datetime.now() + datetime.timedelta(hours=2)},
                  {"name": "gRPC Workshop", "description": event_text, "quota": 70, "created_by": 1,
                   "start_date": datetime.datetime.now(),
                   "image_url": "https://firebasestorage.googleapis.com/v0/b/communitu.appspot.com/o/images%2Fevents%2Fevent1.png?alt=media&token=d6de8e88-c2f9-4be5-8bb3-9edb7528b8db",
                   "location": "Online",
                   "header_photo_url": None, "end_date": datetime.datetime.now() + datetime.timedelta(hours=2)}
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
