from app.repository.base_repository import BaseRepository
from app.constants.database_constants import AUTHORITY_DB_TABLE_NAME, AUTHORITY_TABLE_INIT_STAT, \
    LINKER_USER_AUTHORITY_TABLE_INIT_STAT


class AuthorityRepository(BaseRepository):
    """
        Repository class for the user authorities.
    """

    def __init__(self):
        super().__init__(table=AUTHORITY_DB_TABLE_NAME)

    def initialize_table(self):
        # Initialize main table
        super().initialize_table(initialization_statement=AUTHORITY_TABLE_INIT_STAT)

        # Initialize linker tables
        super().initialize_table(initialization_statement=LINKER_USER_AUTHORITY_TABLE_INIT_STAT)
