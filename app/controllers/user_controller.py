import psycopg2
from psycopg2._psycopg import IntegrityError
from flask import Blueprint, request, make_response, jsonify

from app.repository.user_repository import UserRepository

user_api = Blueprint('user_api', __name__)
user_repo = UserRepository


@user_api.route("/users/<user_id>/clubs", methods=['GET'])
def get_clubs_of_user(user_id):
    # Parse request parameters
    args = request.args

    if 'role' in args:
        user_role = args['role']
    else:
        return make_response(jsonify({'message': "Role parameter should be specified!"}), 400)

    if user_role == "participant":
        # TODO: get clubs that user participated
        pass
    elif user_role == "executive":

        if 'fields' not in args:
            return make_response({'message': "Fields should be specified! "}, 400)

        try:
            fields = args['fields'].split(",")
            clubs = user_repo.get_clubs_executed_by_user(user_id=user_id, return_columns=fields)
            return make_response(jsonify({"clubs": clubs, 'message': "Clubs fetched successfully!"}), 200)

        except psycopg2.errors.UndefinedColumn:
            return make_response(jsonify({'message': "Field parameters are not correct!"}), 400)
    else:
        return make_response(jsonify({'message': "Role parameter is not correct!"}), 400)