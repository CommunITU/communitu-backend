from psycopg2._psycopg import IntegrityError

from app.repository.event_repository import EventRepository
from flask import Blueprint, request, jsonify, make_response

from app.repository.user_repository import UserRepository
from app.services.auth_service import require_token
from app.util.map_to_dto import map_to_dto, event_model_dto

event_api = Blueprint('event_api', __name__)
event_repo = EventRepository
user_repo = UserRepository


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


@event_api.route("/events/<event_id>/participants/<user_id>", methods=['GET'])
def get_user_participation_status(event_id, user_id):
    """
    :return: Return whether the user is participated to given event or not.
    """

    try:
        status = event_repo.get_user_participation_status(event_id, user_id)
    except Exception as e:
        return make_response(jsonify({'message': 'An error occurred!'}), 400)

    return make_response(
        jsonify({'participationStatus': status, 'message': 'Participation status fetched successfully!'}), 200)


@event_api.route("/events/<event_id>/participants", methods=['POST'])
@require_token(request)
def participate_to_event(user_id, event_id):
    """
    Receive HTTP requests to add user to participants of given event.

    :return: Configured HTTP response
    """

    # Get user's responses to event registration questions.
    user_responses = None
    if 'user_responses' in request.get_json():
        user_responses = request.get_json()['user_responses']

    try:
        event_repo.participate_to_event(event_id, user_id)
        if user_responses:
            user_repo.save_registration_questions_responses(user_responses, user_id)

    except Exception as e:
        return make_response(jsonify({'message': 'An error occurred!'}), 400)

    return make_response(
        jsonify({'message': 'User participation performed successfully!'}), 200)


@event_api.route("/events/<event_id>/participants", methods=['DELETE'])
@require_token(request)
def cancel_participation(user_id, event_id):
    """
    Receive HTTP requests to cancel user participation for the given event.

    :return: Configured HTTP response
    """

    try:
        # Get registration question ids of the event
        registration_questions = event_repo.get_registration_questions(event_id, get_question_options=False,
                                                                       return_columns=['id'])

        # Delete user's responses linked with reg. questions of the event.
        user_repo.delete_registration_questions_responses(registration_questions, user_id)

        # Cancel participation
        event_repo.cancel_participation(event_id, user_id)

    except Exception as e:
        return make_response(jsonify({'message': 'An error occurred!'}), 400)

    return make_response(
        jsonify({'message': 'User participation cancelled successfully!'}), 200)


@event_api.route("/events/<event_id>/participants", methods=['GET'])
def get_event_participants(event_id):
    """
    Receive HTTP requests to fetch participants of event.

    :return: Configured HTTP response contains the participants data.
    """

    if 'return_params' in request.args:
        return_params = request.args['return_params'].split(',')

    try:
        participants = event_repo.get_event_participants(event_id, return_columns=return_params)

    except Exception as e:
        return make_response(jsonify({'message': 'An error occurred while fetching participants!'}), 400)

    return make_response(
        jsonify({'participants': participants, 'message': 'Event participants fetched successfully!'}), 200)


@event_api.route("/events/<event_id>/reg_questions", methods=['GET'])
@require_token(request)
def get_registration_questions(event_id):
    """
    :return: Registration questions of given event.
    """

    try:
        questions = event_repo.get_registration_questions(event_id)
    except Exception as e:
        print(e)
        return make_response(jsonify({'message': 'An error occurred!'}), 400)

    return make_response(
        jsonify({'registration_questions': questions, 'message': 'Registration questions fetched successfully!'}), 200)


@event_api.route("/events/<event_id>/comments", methods=['GET'])
def get_event_comments(event_id):
    """
    :return: Comments of given event.
    """

    try:
        comments = event_repo.get_event_comments_by_id(event_id)
    except Exception as e:
        print(e)
        return make_response(jsonify({'message': 'An error occurred!'}), 400)

    return make_response(
        jsonify({'comments': comments, 'message': 'Comments fetched successfully!'}), 200)


@event_api.route("/events/<event_id>/comments", methods=['POST'])
@require_token(request)
def add_event_comment(user_id, event_id):
    """
    Receives requests to create new event comment.
    """

    try:
        comment = request.get_json()['comment']
        comment_data = {'content': comment, 'user_id': user_id, 'event_id': event_id}
        event_repo.add_event_comment(comment_data=comment_data)

    except Exception as e:
        print(e)
        return make_response(jsonify({'message': 'An error occurred!'}), 400)

    return make_response(
        jsonify({'message': 'Comment created successfully!'}), 200)
