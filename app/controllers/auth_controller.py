from flask import Blueprint, request

from app.services import auth_service

auth_api = Blueprint('auth_api', __name__)


@auth_api.route("/auth/login", methods=['POST'])
def login():
    """
    Login with email and password.
    :Request body : { email : string, password: string }

    :return: HTTP Status
    """

    data = request.get_json()

    return auth_service.login(data['email'], data['password'])
