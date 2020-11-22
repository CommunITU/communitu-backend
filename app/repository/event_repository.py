from app.repository.base_repository import BaseRepository
from app.constants.database_constants import EVENT_TABLE_INIT_STAT, EVENT_REGISTRATION_QUESTION_OPTION_TABLE_INIT_STAT
from app.constants.database_constants import EVENT_DB_TABLE_NAME, EVENT_REGISTRATION_QUESTION_TABLE_INIT_STAT, \
    EVENT_REGISTRATION_QUESTION_USER_OPTION_ANSWER_TABLE_INIT_STAT, \
    EVENT_REGISTRATION_QUESTION_USER_TEXT_ANSWER_TABLE_INIT_STAT


class EventRepository(BaseRepository):
    """ Repository class for the event objects.
        Performs all database operations related to event objects.
    """

    def __init__(self):
        super().__init__(table=EVENT_DB_TABLE_NAME)

    def initialize_table(self):
        # Initialize event table and another tables connected to an event.
        super().initialize_table(initialization_statement=EVENT_TABLE_INIT_STAT)
        super().initialize_table(initialization_statement=EVENT_REGISTRATION_QUESTION_TABLE_INIT_STAT)
        super().initialize_table(initialization_statement=EVENT_REGISTRATION_QUESTION_OPTION_TABLE_INIT_STAT)
        super().initialize_table(
            initialization_statement=EVENT_REGISTRATION_QUESTION_USER_TEXT_ANSWER_TABLE_INIT_STAT)
        super().initialize_table(
            initialization_statement=EVENT_REGISTRATION_QUESTION_USER_OPTION_ANSWER_TABLE_INIT_STAT)

    def create_event(self, event_data):
        """
        Create new event on database.
        :param event_data.
        """
        super().create(event_data)

    def get_all_events(self):
        """
        :return:  All events ordered by created date.
        """
        return super().select(order_by={"created_at": "DESC"})
