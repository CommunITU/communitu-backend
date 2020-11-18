from app.repository.event_repository import EventRepository
from flask import Blueprint, request

from app.services.auth_service import require_token

event_api = Blueprint('event_api', __name__)
er = EventRepository()


@event_api.route("/events", methods=['POST'])
@require_token(request)
def create_event():
    """
    Handle api requests to create new event.

    :Request body:
    {
        title: string,
        description: string,
        start_date: timestamp,
        end_date: timestamp,
        quota: integer,
        owner_id: owner user id
    }
    :return: HTTP Status
    """
    er.create_event(request.get_json())
    return "ok"


@event_api.route("/events", methods=['GET'])
def get_all_events():
    print(er.get_all_events())
    return "ok"
