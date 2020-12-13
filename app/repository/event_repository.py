from app.constants.database_constants import EVENT_TABLE_INIT_STAT, \
    EVENT_REGISTRATION_QUESTION_OPTION_TABLE_INIT_STAT, \
    EVENT_TABLE_NAME, EVENT_REGISTRATION_QUESTION_TABLE_INIT_STAT, \
    EVENT_REGISTRATION_QUESTION_USER_OPTION_ANSWER_TABLE_INIT_STAT, \
    EVENT_REGISTRATION_QUESTION_USER_TEXT_ANSWER_TABLE_INIT_STAT, \
    LINKER_EVENT_USER_PARTICIPANT_TABLE_NAME, \
    LINKER_EVENT_USER_PARTICIPANT_TABLE_INIT_STAT

from app.repository import BaseRepository


class EventRepository(BaseRepository):
    """ Repository class for the event objects.
        Performs all database operations related to event objects.
    """

    @classmethod
    def __init__(cls):
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
        super().initialize_table(
            initialization_statement=LINKER_EVENT_USER_PARTICIPANT_TABLE_INIT_STAT)

    @classmethod
    def create_event(cls, event_data, owner_club_id):
        """
        Create new event on database.
        :param event_data The map that contains the event field and corresponding value.
        :param owner_club_id    Id of owner club
        """
        # Create event
        event_id = cls.add(event_data, table_name=EVENT_TABLE_NAME, return_id=True)

        # TODO: EVENT DATA SHOULD CONTAIN OWNER_CLUB_ID

        # # Link event with owner club
        # map_event_club = {"club_id": owner_club_id, "event_id": event_id}
        # cls.add(map_event_club, table_name=LINKER_CLUB_EVENT_CREATED_BY_TABLE_NAME)

    @classmethod
    def get_all_events(cls):
        """
        :return:  All events ordered by created date.
        """
        return super().select(order_by={"created_at": "DESC"})
