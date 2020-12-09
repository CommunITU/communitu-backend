from app.constants.database_constants import NOTIFICATION_TABLE_NAME, NOTIFICATION_TYPE_TABLE_INIT_STAT, \
    NOTIFICATION_TABLE_INIT_STAT
from app.repository import BaseRepository


class NotificationRepository(BaseRepository):
    """
        Repository class for the notifications.
    """

    def __init__(self):
        super().__init__(table=NOTIFICATION_TABLE_NAME)

    @classmethod
    def initialize_table(cls):
        # Initialize main tables
        super().initialize_table(initialization_statement=NOTIFICATION_TYPE_TABLE_INIT_STAT)
        super().initialize_table(initialization_statement=NOTIFICATION_TABLE_INIT_STAT)

