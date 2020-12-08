from app.repository.event_repository import EventRepository
from flask import Blueprint, request, jsonify, make_response

from app.services.auth_service import require_token
from app.util.map_to_dto import map_to_dto, event_model_dto

event_api = Blueprint('event_api', __name__)
er = EventRepository


@event_api.route("/events", methods=['POST'])
@require_token(request)
def create_event(user_id=""):
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
    print(user_id)
    # er.create_event(request.get_json())
    return "ok"


@event_api.route("/events", methods=['GET'])
def get_all_events():
    """
    :return: All created events.
    """
    # Get all events.
    all_events = er.get_all_events()

    # Convert fetched events to data transfer object.
    dto_list = [map_to_dto(event, event_model_dto) for event in all_events]
    return make_response(jsonify(dto_list), 200)
