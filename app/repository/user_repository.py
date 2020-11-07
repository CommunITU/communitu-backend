from app.repository.base_repository import BaseRepository
from app.constants.database_constants import USER_DB_TABLE_INIT_STAT
from app.constants.database_constants import USER_DB_TABLE_NAME


class UserRepository(BaseRepository):
    """ Repository class for the user objects.
        Performs all database operations related to user objects.
    """

    def __init__(self):
        super().__init__(table=USER_DB_TABLE_NAME)

    def initialize_table(self):
        super().initialize_table(initialization_statement=USER_DB_TABLE_INIT_STAT)
