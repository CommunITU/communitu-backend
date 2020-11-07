from flask import Flask
from app.repository.event_repository import EventRepository
from app.repository.user_repository import UserRepository


def init_app():
    UserRepository().initialize_table()  # init user table
    EventRepository().initialize_table()  # init event table
    return Flask(__name__)


app = init_app()


@app.route("/")
def home_page():
    return "Hello, world!"


if __name__ == "__main__":
    app.run()
