from psycopg2._psycopg import IntegrityError
from flask import Blueprint, request, make_response, jsonify

from app.repository.user_repository import UserRepository

user_api = Blueprint('user_api', __name__)
user_repo = UserRepository


@user_api.route("/users/<user_id>/clubs", methods=['GET'])
def get_clubs_of_user(user_id):
    # Parse request parameters
    args = request.args
    user_role = args['role']

    if user_role == "participant":
        # TODO: get clubs that user participated
        pass
    elif user_role == "executive":
        # TODO: get clubs executed by given user
        clubs = user_repo.get_clubs_executed_by_user(user_id=user_id)
        pass

    else:
        return make_response(jsonify({'message': "Role parameter is not correct!"}), 400)

    return "okey"