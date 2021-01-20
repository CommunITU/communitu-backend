from flask import Blueprint, request, make_response, jsonify
from jwt import DecodeError
from psycopg2._psycopg import IntegrityError

from app.exceptions.auth_exceptions import AuthCredentialsError, NoSuchUserError
from app.services import auth_service
from app.services.auth_service import require_token
from app.util.map_to_dto import user_model_dto, map_to_dto

auth_api = Blueprint('auth_api', __name__)


@auth_api.route("/auth/login", methods=['POST'])
def login():
    """
    Login with email and password.
    :Request body : { email : string, password: string }

    :return: JWT token and logged-in user data as Http Response.
    """

    data = request.get_json()
    try:
        login_data = auth_service.login(data['email'], data['password'])
        jwt_token = login_data['token']
        user = login_data['user']
        return make_response(jsonify({'token': jwt_token, 'user': user}), 200,
                             {'WWW-Authenticate': 'Basic realm="Logged in successfully."'})
    except AuthCredentialsError as auth_error:
        return make_response(jsonify({'message': str(auth_error).strip()}), 401,
                             {'WWW-Authenticate': 'Basic realm="Login Required!"'})
    except Exception as error:
        return make_response(jsonify({'message': str(error).strip()}), 401,
                             {'WWW-Authenticate': 'Basic realm="Login Required!"'})


@auth_api.route("/auth/register", methods=['POST'])
def register():
    """
    Login with email and password.
    :Request body : { email : string, password: string }

    :return: JWT token and logged-in user data as Http Response.
    """

    user_data = request.get_json()
    try:
        auth_service.register(user_data)  # Register
        return make_response(jsonify({'message': "Account created successfully!"}), 200)

    except IntegrityError:
        return make_response(jsonify({'message': "Email already exists!"}), 400)

    except Exception as error:
        return make_response(jsonify({'message': str(error).strip()}), 400)


@auth_api.route("/auth/login_with_token", methods=['POST'])
@require_token(request)
def login_with_token(user):
    """
    Login with JWT token.
    :Request body : { token: string }

    :return: Logged-in user data
    """
    try:
        user_dto = map_to_dto(user, user_model_dto)  # Map 'user dao' to 'user dto'
        return make_response(jsonify({'user': user_dto}), 200,
                             {'WWW-Authenticate': 'Basic realm="Logged in successfully."'})
    except DecodeError as error:
        print(error)
        return make_response(jsonify({'message': str(error).strip()}), 401,
                             {'WWW-Authenticate': 'Basic realm="Token decode error!"'})

    except NoSuchUserError as error:
        print(error)
        return make_response(jsonify({'message': str(error).strip()}), 401,
                             {'WWW-Authenticate': 'Basic realm="Credentials are not correct!"'})
