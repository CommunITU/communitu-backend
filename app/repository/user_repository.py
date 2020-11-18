from app.constants.error_messages import AUTH_CREDENTIALS_NOT_CORRECT
from app.repository.base_repository import BaseRepository
from app.constants.database_constants import USER_DB_TABLE_INIT_STAT
from app.constants.database_constants import USER_DB_TABLE_NAME
from app.exceptions.auth_exceptions import AuthCredentialsError


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

        return user
