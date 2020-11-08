from app.repository.base_repository import BaseRepository
from app.constants.database_constants import EVENT_DB_TABLE_INIT_STAT
from app.constants.database_constants import EVENT_DB_TABLE_NAME


class EventRepository(BaseRepository):
    """ Repository class for the event objects.
        Performs all database operations related to event objects.
    """

    def __init__(self):
        super().__init__(table=EVENT_DB_TABLE_NAME)

    def initialize_table(self):
        super().initialize_table(initialization_statement=EVENT_DB_TABLE_INIT_STAT)

    def create_event(self, event_data):
        """
        Create new event on database.
        :param event_data.
        """
        print(event_data)
