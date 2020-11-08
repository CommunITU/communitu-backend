from app.repository.event_repository import EventRepository
from flask import Blueprint, request

event_api = Blueprint('event_api', __name__)
er = EventRepository()


@event_api.route("/events", methods=['POST'])
def create_event():
    er.create_event(request.get_json())
    return "ok"
