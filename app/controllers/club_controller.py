from psycopg2._psycopg import IntegrityError

from app.repository.club_repository import ClubRepository
from flask import Blueprint, request, make_response, jsonify

from app.services.auth_service import require_token

club_api = Blueprint('club_api', __name__)
club_repo = ClubRepository


@club_api.route("/clubs", methods=['POST'])
@require_token(request)
def create_club(user_id=""):
    club_data = request.get_json()
    try:
        club_repo.create_club(club_data, user_id)
    except IntegrityError:
        return make_response(jsonify({'errors': ["Club name already exists!", ]}), 400)

    return make_response(jsonify({'message': "Club created successfully!"}), 200)


@club_api.route("/clubs/<club_id>", methods=['GET'])
@require_token(request)
def get_club_by_id(club_id):
    club_data = request.get_json()
    try:
        club = club_repo.get_club_by_id(club_data)
    except Exception as e:
        print(e)
        return make_response(jsonify({'club': club, 'message': "An error occurred while getting event!"}), 400)

    return make_response(jsonify({'message': "Club fetched successfully!"}), 200)


@club_api.route("/clubs/<club_id>", methods=['DELETE'])
def delete_club_by_id(club_id):
    try:
        club_repo.delete_club_by_id(club_id)
    except Exception as e:
        print(e)
        return make_response(jsonify({'message': "An error occurred while deleting event!"}), 400)

    return make_response(jsonify({'message': "Club deleted successfully!"}), 200)


@club_api.route("/clubs/<club_id>", methods=['PUT'])
@require_token(request)
def update_club_by_id(club_id):
    club_data = request.get_json()
    try:
        club_repo.update_club_by_id(club_data)
    except Exception as e:
        print(e)
        return make_response(jsonify({'message': "An error occurred while updating event!"}), 400)

    return make_response(jsonify({'message': "Club updated successfully!"}), 200)
