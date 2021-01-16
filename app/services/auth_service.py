import inspect
from functools import wraps

from flask import current_app, make_response

from app.exceptions.auth_exceptions import NoSuchUserError
from app.repository.user_repository import UserRepository
import jwt
import datetime

user_repo = UserRepository()


def require_token(request):
    """
    Decorator function to check Jwt token is valid or not.
    This decorator must be used with functions that requires login permission.
    :param request: Http request
    """

    def inside_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            headers = request.headers
            if "Authorization" not in headers:
                return make_response({'message': "Token is not correct."}, 403,
                                     {'WWW-Authenticate': 'Basic realm="Token is not correct."'})

            token = headers['Authorization'].replace("Bearer ", "")
            if not token:
                return make_response({'message': "Token is not correct."}, 403,
                                     {'WWW-Authenticate': 'Basic realm="Token is not correct."'})
            try:
                token_data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
                user_email = token_data['username']

                required_params = {}
                func_params = inspect.getfullargspec(func).args
                if func_params.__contains__("user_id"):
                    required_params['user_id'] = user_repo.get_user_id_by_email(email=user_email)
                if func_params.__contains__("user_email"):
                    required_params['user_email'] = user_email
                if func_params.__contains__("user"):
                    required_params['user'] = user_repo.get_user_by_email(email=user_email)

            except NoSuchUserError as e:
                return make_response({'message': str(e)}, 403,
                                     {'WWW-Authenticate': 'Basic realm="No such user with given email."'})
            except Exception as e:
                return make_response({'message': str(e)}, 403, {'WWW-Authenticate': 'Basic realm="Token is not correct."'})
            res = func(*args, **kwargs, **required_params)  # If token is valid, execute the real function

            return res

        return wrapper

    return inside_decorator


def login(email, password):
    """
    If the credentials are correct, it generates the JWT token.
    :param email
    :param password
    :return: A dictionary that contains the token and authenticated user data.
    """
    user = user_repo.authenticate(email, password)
    claims = {'username': email, 'exp': datetime.datetime.utcnow() + datetime.timedelta(weeks=2)}
    token = jwt.encode(
        claims, current_app.config['SECRET_KEY'], algorithm='HS256').decode('UTF-8')
    return {'token': token, 'user': user}


def login_with_token(token):
    """
       If the JWT token is valid, perform authentication of user.
       :param token
       :return: Authenticated user data.
       """
    data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
    user = user_repo.get_user_by_email(data['username'])
    return {'user': user}


def register(user_data):
    """
        Create new user
        :return: A dictionary that contains user data (name, email, password).
    """
    user_repo.create_user({"name": user_data['name'], "email": user_data['email'], "password": user_data['password']})
