from app.constants.database_constants import CLUB_TABLE_INIT_STAT, \
    LINKER_CLUB_USER_EXECUTIVE_TABLE_INIT_STAT, CLUB_TABLE_NAME, \
    LINKER_CLUB_USER_CREATED_BY_TABLE_NAME, \
    LINKER_CLUB_USER_CREATED_BY_TABLE_INIT_STAT, \
    LINKER_CLUB_USER_PARTICIPANT_TABLE_INIT_STAT

from app.repository import BaseRepository


class ClubRepository(BaseRepository):
    """ Repository class for the club objects.
        Performs all database operations related to clubs.
    """

    def __init__(self):
        super().__init__(table=CLUB_TABLE_NAME)

    @classmethod
    def initialize_table(cls):
        # Initialize main table
        super().initialize_table(initialization_statement=CLUB_TABLE_INIT_STAT)

        # Initialize linker tables
        super().initialize_table(initialization_statement=LINKER_CLUB_USER_CREATED_BY_TABLE_INIT_STAT)
        super().initialize_table(initialization_statement=LINKER_CLUB_USER_EXECUTIVE_TABLE_INIT_STAT)
        super().initialize_table(initialization_statement=LINKER_CLUB_USER_PARTICIPANT_TABLE_INIT_STAT)

    @classmethod
    def create_club(cls, club_data, user_id_who_created):
        club_id = super().add(club_data, table_name=CLUB_TABLE_NAME, return_id=True)
        map_user_club = {"user_id": user_id_who_created,
                         "club_id": club_id}

        # Link the club with the user who created.
        super().add(map_user_club, table_name=LINKER_CLUB_USER_CREATED_BY_TABLE_NAME)
