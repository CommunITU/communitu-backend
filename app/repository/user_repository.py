from app.constants.error_messages import AUTH_CREDENTIALS_NOT_CORRECT, NO_SUCH_USER_WITH_GIVEN_EMAIL
from app.repository.base_repository import BaseRepository
from app.constants.database_constants import USER_DB_TABLE_INIT_STAT
from app.constants.database_constants import USER_DB_TABLE_NAME
from app.exceptions.auth_exceptions import AuthCredentialsError, NoSuchUserError


class UserRepository(BaseRepository):
    """ Repository class for the user objects.
        Performs all database operations related to user objects.
    """

    def __init__(self):
        super().__init__(table=USER_DB_TABLE_NAME)

    def initialize_table(self):
        super().initialize_table(initialization_statement=USER_DB_TABLE_INIT_STAT)

    def authenticate(self, email, password):
        """
        Check given credentials.

        @:raise AuthCredentialsError if credentials are not correct.
        """

        user = super().select(where={"email": email, "password": password})
        if not user:
            raise AuthCredentialsError(AUTH_CREDENTIALS_NOT_CORRECT)

        return user.__getitem__(0)

    def get_user_by_email(self, email):
        """
        Get user by email.

        :raise: NoSuchUserError if there is not an user with given email.
        """

        user = super().select(where={"email": email})
        if not user:
            raise NoSuchUserError(NO_SUCH_USER_WITH_GIVEN_EMAIL)

        return user.__getitem__(0)
