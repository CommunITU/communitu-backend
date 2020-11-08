from flask import Flask

from app.repository.event_repository import EventRepository
from app.repository.user_repository import UserRepository
from app.controllers.event_controller import event_api


def register_controllers(m_app):
    m_app.register_blueprint(event_api)  # register event controller


def init_db():
    UserRepository().initialize_table()  # init user table
    EventRepository().initialize_table()  # init event table


def init_app():
    m_app = Flask(__name__)
    register_controllers(m_app)
    init_db()
    return m_app


app = init_app()


@app.route("/")
def home_page():
    return "Hello, world!"


if __name__ == "__main__":
    app.run()
