from flask import Flask

from app.models.event_model import EventModel
from app.repository.event_repository import EventRepository


def create_app():
    app = Flask(__name__)
    return app


app = create_app()


@app.route("/")
def home_page():
    event = EventModel("Forencics Training", "Event description", "6 ekim", "11 ekim", 21)
    EventRepository().initialize_table()
    return "Hello, world!"


if __name__ == "__main__":
    app.run()
