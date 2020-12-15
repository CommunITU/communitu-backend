from app.constants.database_constants import AUTHORITY_TABLE_NAME, AUTHORITY_TABLE_INIT_STAT, \
    LINKER_USER_AUTHORITY_TABLE_INIT_STAT, \
    LINKER_USER_AUTHORITY_TABLE_NAME
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
    def create_authority(cls, authority_data):
        super().add(data=authority_data, table_name=AUTHORITY_TABLE_NAME)

    @classmethod
    def get_authority_id_by_name(cls, authority_name):
        id = super().select(from_tables=[AUTHORITY_TABLE_NAME], return_columns=["id"],
                            where={"authority": authority_name})[0]["id"]
        return id

    @classmethod
    def set_authority_of_user(cls, authority, user_id):
        authority_id = cls.get_authority_id_by_name(authority)

        map_user_auth = {"user_id": user_id, "authority_id": authority_id}
        super().add(map_user_auth, table_name=LINKER_USER_AUTHORITY_TABLE_NAME)
