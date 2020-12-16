from app.repository import BaseRepository
from app.constants.error_messages import AUTH_CREDENTIALS_NOT_CORRECT, NO_SUCH_USER_WITH_GIVEN_EMAIL
from app.constants.database_constants import USER_TABLE_INIT_STAT
from app.constants.database_constants import USER_TABLE_NAME
from app.exceptions.auth_exceptions import AuthCredentialsError, NoSuchUserError


class UserRepository(BaseRepository):
    """ Repository class for the user objects.
        Performs all database operations related to user objects.
    """

    def __init__(self):
        super().__init__(table=USER_TABLE_NAME)

    @classmethod
    def initialize_table(cls):
        super().initialize_table(initialization_statement=USER_TABLE_INIT_STAT)

    @classmethod
    def create_user(cls, user_data):
        """
        Create new event on database.
        :param user_data The map that contains the user field and corresponding value.
        """
        cls.add(user_data, table_name=USER_TABLE_NAME)

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

    def get_user_id_by_email(self, email):
        """
        Get user ID by email.

        :raise: NoSuchUserError if there is not an user with given email.
        """

        user_id = super().select(where={"email": email}, return_columns=["id"])
        if not user_id:
            raise NoSuchUserError(NO_SUCH_USER_WITH_GIVEN_EMAIL)

        return user_id.__getitem__(0)["id"]
