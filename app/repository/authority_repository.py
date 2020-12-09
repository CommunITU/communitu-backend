from app.constants.database_constants import AUTHORITY_TABLE_NAME, AUTHORITY_TABLE_INIT_STAT, \
    LINKER_USER_AUTHORITY_TABLE_INIT_STAT
from app.repository import BaseRepository


class AuthorityRepository(BaseRepository):
    """
        Repository class for the user authorities.
    """

    def __init__(self):
        super().__init__(table=AUTHORITY_TABLE_NAME)

    @classmethod
    def initialize_table(cls):
        # Initialize main table
        super().initialize_table(initialization_statement=AUTHORITY_TABLE_INIT_STAT)

        # Initialize linker tables
        super().initialize_table(initialization_statement=LINKER_USER_AUTHORITY_TABLE_INIT_STAT)

    @classmethod
    def create_authority(cls, authority):
        super().add(authority, table_name=AUTHORITY_TABLE_NAME)
