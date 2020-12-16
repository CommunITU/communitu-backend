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
