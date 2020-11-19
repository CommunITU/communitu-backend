from flask import Blueprint, request, make_response, jsonify

from app.exceptions.auth_exceptions import AuthCredentialsError
from app.services import auth_service
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
        user_dto = map_to_dto(user, user_model_dto)
        return make_response(jsonify({'token': jwt_token, 'user': user_dto}), 200,
                             {'WWW-Authenticate': 'Basic realm="Logged in successfully."'})
    except AuthCredentialsError as auth_error:
        return make_response(str(auth_error), 401, {'WWW-Authenticate': 'Basic realm="Login Required!"'})
