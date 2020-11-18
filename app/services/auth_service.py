from flask import current_app

from app.repository.user_repository import UserRepository
import jwt
import datetime

user_repo = UserRepository()


def login(email, password):
    user = user_repo.authenticate(email, password)
    claims = {'username': email, 'exp': datetime.datetime.utcnow() + datetime.timedelta(weeks=2)}
    token = jwt.encode(
        claims, current_app.config['SECRET_KEY'], algorithm='HS256').decode('UTF-8')
    return {'token': token, 'user': user}
