from flask import Flask
from flask_cors import CORS

from app.constants.app_constants import TOKEN_SECRET_KEY
from app.controllers.auth_controller import auth_api
from app.controllers.club_controller import club_api
from app.controllers.event_controller import event_api
from app.repository.authority_repository import AuthorityRepository
from app.repository.club_repository import ClubRepository
from app.repository.comment_repository import CommentRepository
from app.repository.event_repository import EventRepository
from app.repository.notification_repository import NotificationRepository
from app.repository.user_repository import UserRepository
from app.util.db_util import PopulateInitialDatabase, clean_database


def register_controllers(m_app):
    m_app.register_blueprint(event_api)  # register event controller
    m_app.register_blueprint(auth_api)  # register auth controller
    m_app.register_blueprint(club_api)  # register club controller


def init_db():
    """ Initialize database """

    """ Remove old data. It is a config for the development, not production """
    clean_database()

    """ Initialize tables """
    UserRepository.initialize_table()
    AuthorityRepository.initialize_table()
    ClubRepository.initialize_table()
    EventRepository.initialize_table()
    NotificationRepository.initialize_table()
    CommentRepository.initialize_table()

    """ Populate database """
    PopulateInitialDatabase.populate()


def init_app():
    m_app = Flask(__name__)
    CORS(m_app, resources={r"/*": {"origins": "*"}})
    m_app.config['CORS_HEADERS'] = 'Content-Type'
    m_app.config['SECRET_KEY'] = TOKEN_SECRET_KEY
    init_db()
    register_controllers(m_app)
    return m_app


app = init_app()


@app.route("/")
def home_page():
    return "Hello, world!"


if __name__ == "__main__":
    app.run()
