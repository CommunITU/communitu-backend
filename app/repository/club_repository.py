from app.repository.base_repository import BaseRepository
from app.constants.database_constants import CLUB_DB_TABLE_INIT_STAT, LINKER_CLUB_EVENT_TABLE_INIT_STAT, \
    LINKER_CLUB_USER_EXECUTIVE_TABLE_INIT_STAT, CLUB_DB_TABLE_NAME, LINKER_CLUB_USER_PARTICIPANT_TABLE_INIT_STAT


class ClubRepository(BaseRepository):
    """ Repository class for the club objects.
        Performs all database operations related to clubs.
    """

    def __init__(self):
        super().__init__(table=CLUB_DB_TABLE_NAME)

    def initialize_table(self):
        # Initialize main table
        super().initialize_table(initialization_statement=CLUB_DB_TABLE_INIT_STAT)

        # Initialize linker tables
        super().initialize_table(initialization_statement=LINKER_CLUB_EVENT_TABLE_INIT_STAT)
        super().initialize_table(initialization_statement=LINKER_CLUB_USER_EXECUTIVE_TABLE_INIT_STAT)
        super().initialize_table(initialization_statement=LINKER_CLUB_USER_PARTICIPANT_TABLE_INIT_STAT)
