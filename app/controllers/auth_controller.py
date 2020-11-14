from flask import Blueprint, request

auth_api = Blueprint('auth_api', __name__)


@auth_api.route("/auth/login", methods=['POST'])
def login():

    return "ok"
