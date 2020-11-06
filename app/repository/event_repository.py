from app.repository.base_repository import BaseRepository
from app.constants.database_constants import EVENTS_DB_TABLE_INIT_STAT
from app.constants.database_constants import EVENTS_DB_TABLE_NAME


class EventRepository(BaseRepository):
    def __init__(self):
        super().__init__(table=EVENTS_DB_TABLE_NAME)

    def initialize_table(self):
        super().initialize_table(initialization_statement=EVENTS_DB_TABLE_INIT_STAT)
