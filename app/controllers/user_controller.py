import psycopg2
from flask import Blueprint, request, make_response, jsonify

from app.repository.user_repository import UserRepository
from app.services.auth_service import require_token

user_api = Blueprint('user_api', __name__)
user_repo = UserRepository


@user_api.route("/users/<user_id>", methods=['GET'])
def get_user_by_id(user_id):
    try:
        user = user_repo.get_user_by_id(user_id)
    except Exception as e:
        print(e)
        return make_response(jsonify({'message': "An error occurred while fetching user!"}), 400)

    return make_response(jsonify({'user': user, 'message': "User fetched successfully!"}), 200)


@user_api.route("/users/<user_id>", methods=['DELETE'])
@require_token(request)
def delete_user_by_id(user_id):
    try:
        user_repo.delete_user_by_id(user_id)
    except Exception as e:
        print(e)
        return make_response(jsonify({'message': "An error occurred while deleting user!"}), 400)

    return make_response(jsonify({'message': "User deleted successfully!"}), 200)


@user_api.route("/users/<user_id>", methods=['PUT'])
def update_user_by_id(user_id):
    try:
        user_data = request.get_json()['user']
        user_repo.update_user_by_id(user_data)
    except Exception as e:
        print(e)
        return make_response(jsonify({'message': "An error occurred while updating user!"}), 400)

    return make_response(jsonify({'message': "User updated successfully!"}), 200)


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

            extra_fields = None
            if 'extra_fields' in args:
                extra_fields = args['extra_fields'].split(',')

            clubs = user_repo.get_clubs_executed_by_user(user_id=user_id, return_columns=fields,
                                                         extra_fields=extra_fields)
            return make_response(jsonify({"clubs": clubs, 'message': "Clubs fetched successfully!"}), 200)

        except psycopg2.errors.UndefinedColumn as e:
            print(e)
            return make_response(jsonify({'message': "Field parameters are not correct!"}), 400)

        except Exception as e:
            print(e)
            return make_response(jsonify({'message': "An error occurred while fetching clubs!"}), 400)
    else:
        return make_response(jsonify({'message': "Role parameter is not correct!"}), 400)
