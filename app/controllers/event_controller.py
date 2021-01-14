from psycopg2._psycopg import IntegrityError

from app.repository.event_repository import EventRepository
from flask import Blueprint, request, jsonify, make_response

from app.services.auth_service import require_token
from app.util.map_to_dto import map_to_dto, event_model_dto

event_api = Blueprint('event_api', __name__)
event_repo = EventRepository


@event_api.route("/events", methods=['POST'])
@require_token(request)
def create_event(user_id=""):
    """
    Handle api requests to create new event.

    :Request body:
    {
        name: string,
        description: string,
        start_date: timestamp,
        end_date: timestamp,
        location: string,
        club_selection, integer,
        quota: integer,
        registration_questions: array
    }
    :return: HTTP Status
    """
    req_json = request.get_json()

    event_data = req_json['event_data']

    try:
        event_repo.create_event(event_data)
    except Exception as e:
        return make_response(jsonify({'message': "Database error occurred!"}), 400)

    return make_response(jsonify({'message': "Club created successfully!"}), 200)


@event_api.route("/events", methods=['GET'])
def get_all_events():
    """
    :return: All created events.
    """

    # Parse request parameters
    args = request.args
    page = args['page']
    size = args['size']

    # Get all events.
    all_events = event_repo.get_all_events(page=int(page), size=int(size))

    # Convert fetched events to data transfer object.
    dto_list = [map_to_dto(event, event_model_dto) for event in all_events]
    return make_response(jsonify(dto_list), 200)


@event_api.route("/events/<event_id>", methods=['GET'])
def get_event(event_id):
    """
    :return: Event corresponds to passed id.
    """

    # Get event
    try:
        event = event_repo.get_event_by_id(event_id)
    except Exception as e:
        return make_response(jsonify({'message': 'An error occurred!'}), 400)

    # Convert fetched events to data transfer object.
    dto_list = map_to_dto(event, event_model_dto)

    return make_response(jsonify({'event': dto_list, 'message': 'Event fetched successfully!'}), 200)
