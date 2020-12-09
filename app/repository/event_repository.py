from app.constants.database_constants import EVENT_TABLE_INIT_STAT, EVENT_REGISTRATION_QUESTION_OPTION_TABLE_INIT_STAT
from app.constants.database_constants import EVENT_TABLE_NAME, EVENT_REGISTRATION_QUESTION_TABLE_INIT_STAT, \
    EVENT_REGISTRATION_QUESTION_USER_OPTION_ANSWER_TABLE_INIT_STAT, \
    EVENT_REGISTRATION_QUESTION_USER_TEXT_ANSWER_TABLE_INIT_STAT
from app.repository import BaseRepository


class EventRepository(BaseRepository):
    """ Repository class for the event objects.
        Performs all database operations related to event objects.
    """

    def __init__(self):
        super().__init__(table=EVENT_TABLE_NAME)

    @classmethod
    def initialize_table(cls):
        # Initialize event table and another tables connected to an event.
        super().initialize_table(initialization_statement=EVENT_TABLE_INIT_STAT)
        super().initialize_table(initialization_statement=EVENT_REGISTRATION_QUESTION_TABLE_INIT_STAT)
        super().initialize_table(initialization_statement=EVENT_REGISTRATION_QUESTION_OPTION_TABLE_INIT_STAT)
        super().initialize_table(
            initialization_statement=EVENT_REGISTRATION_QUESTION_USER_TEXT_ANSWER_TABLE_INIT_STAT)
        super().initialize_table(
            initialization_statement=EVENT_REGISTRATION_QUESTION_USER_OPTION_ANSWER_TABLE_INIT_STAT)

    @classmethod
    def create_event(cls, event_data):
        """
        Create new event on database.
        :param event_data The map that contains the event field and corresponding value.
        """
        cls.create(event_data)

    @classmethod
    def get_all_events(cls):
        """
        :return:  All events ordered by created date.
        """
        return super().select(order_by={"created_at": "DESC"})
