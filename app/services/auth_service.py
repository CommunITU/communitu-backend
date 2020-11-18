from functools import wraps

from flask import current_app, make_response

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
                return make_response("Token is not correct.", 403,
                                     {'WWW-Authenticate': 'Basic realm="Token is not correct."'})

            token = headers['Authorization'].replace("Bearer ", "")
            if not token:
                return make_response("Token is not correct.", 403,
                                     {'WWW-Authenticate': 'Basic realm="Token is not correct."'})
            try:
                data = jwt.decode(token, current_app.config['SECRET_KEY'])
                print(data)
            except Exception as e:
                return make_response(str(e), 403, {'WWW-Authenticate': 'Basic realm="Token is not correct."'})

            res = func(*args, **kwargs)  # If token is valid, execute the real function
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
