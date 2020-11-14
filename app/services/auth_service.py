from app.exceptions.auth_exceptions import AuthCredentialsError
from app.repository.user_repository import UserRepository

user_repo = UserRepository()


def login(email, password):
    try:
        user_repo.authenticate(email, password)  # Check credentials
        # TODO: Generate JWT Token.

    except AuthCredentialsError:
        return "failed"



