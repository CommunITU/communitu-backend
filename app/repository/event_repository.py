from app.constants.database_constants import EVENT_TABLE_INIT_STAT, \
    EVENT_REGISTRATION_QUESTION_OPTION_TABLE_INIT_STAT, \
    EVENT_TABLE_NAME, EVENT_REGISTRATION_QUESTION_TABLE_INIT_STAT, \
    EVENT_REGISTRATION_CHOICE_TYPE_QUESTION_TABLE_INIT_STAT, \
    EVENT_REGISTRATION_TEXT_TYPE_QUESTION_TABLE_INIT_STAT, \
    LINKER_EVENT_USER_PARTICIPANT_TABLE_INIT_STAT, \
    EVENT_REGISTRATION_QUESTION_USER_RESPONSE_TABLE_INIT_STAT, \
    EVENT_REGISTRATION_QUESTION_TEXT_TYPE_USER_RESPONSE_TABLE_INIT_STAT, \
    EVENT_REGISTRATION_QUESTION_CHOICE_TYPE_USER_RESPONSE_TABLE_INIT_STAT, EVENT_REGISTRATION_QUESTION_TABLE_NAME, \
    EVENT_REGISTRATION_QUESTION_OPTION_TABLE_NAME, EVENT_REGISTRATION_TEXT_TYPE_QUESTION_TABLE_NAME, \
    EVENT_REGISTRATION_CHOICE_TYPE_QUESTION_TABLE_NAME, LINKER_EVENT_USER_PARTICIPANT_TABLE_NAME

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
        super().initialize_table(initialization_statement=EVENT_REGISTRATION_CHOICE_TYPE_QUESTION_TABLE_INIT_STAT)
        super().initialize_table(initialization_statement=EVENT_REGISTRATION_TEXT_TYPE_QUESTION_TABLE_INIT_STAT)

        super().initialize_table(initialization_statement=EVENT_REGISTRATION_QUESTION_OPTION_TABLE_INIT_STAT)
        super().initialize_table(initialization_statement=EVENT_REGISTRATION_QUESTION_USER_RESPONSE_TABLE_INIT_STAT)
        super().initialize_table(
            initialization_statement=EVENT_REGISTRATION_QUESTION_TEXT_TYPE_USER_RESPONSE_TABLE_INIT_STAT)
        super().initialize_table(
            initialization_statement=EVENT_REGISTRATION_QUESTION_CHOICE_TYPE_USER_RESPONSE_TABLE_INIT_STAT)

        super().initialize_table(
            initialization_statement=LINKER_EVENT_USER_PARTICIPANT_TABLE_INIT_STAT)

    @classmethod
    def create_event(cls, event_data):
        """
        Create new event on database.
        :param event_data The map that contains the event field and corresponding value.
        """

        event_table_obj = {'name': event_data['name'], 'description': event_data['description'],
                           'start_date': event_data['start_date'], 'end_date': event_data['end_date'],
                           'quota': event_data['quota'], 'location': event_data['location'],
                           'created_by': event_data['created_by'],
                           'image_url': event_data['image_url']}

        # Create event
        event_id = cls.add(data=event_table_obj, table_name=EVENT_TABLE_NAME, return_id=True)

        if 'registration_questions' in event_data:
            registration_questions = event_data['registration_questions']
            for question in registration_questions.values():
                new_question_obj = {'title': question['title'], 'explanation': question['explanation'],
                                    'is_mandatory': True, 'question_type': question['question_type'],
                                    'event_id': event_id}

                question_id = cls.add(data=new_question_obj, table_name=EVENT_REGISTRATION_QUESTION_TABLE_NAME,
                                      return_id=True)

                if question["question_type"] == "choice":
                    cls.add(data={'id': question_id},
                            table_name=EVENT_REGISTRATION_CHOICE_TYPE_QUESTION_TABLE_NAME)

                    options = question['question_options']
                    for option in options.values():
                        new_option_obj = {'option_text': option['option_text'], 'question_id': question_id}

                        cls.add(data=new_option_obj, table_name=EVENT_REGISTRATION_QUESTION_OPTION_TABLE_NAME)

                elif question["question_type"] == "text":
                    cls.add(data={'id': question_id},
                            table_name=EVENT_REGISTRATION_TEXT_TYPE_QUESTION_TABLE_NAME)

    @classmethod
    def get_all_events(cls, page, size):
        """
        :return:  All events ordered by created date.
        """
        return super().select(order_by={"created_at": "DESC"}, from_tables=[EVENT_TABLE_NAME],
                              limit=size, offset=(page - 1) * size)

    @classmethod
    def get_event_by_id(cls, id):
        """
        :return: Event
        """

        return super().select(from_tables=[EVENT_TABLE_NAME], where={"id": id})[0]

    @classmethod
    def get_user_participation_status(cls, event_id, user_id):
        """
        :return: Participation status.
        """
        event = super().select(from_tables=[LINKER_EVENT_USER_PARTICIPANT_TABLE_NAME],
                               where={"user_id": user_id, "event_id": event_id})

        return True if event else False

    @classmethod
    def participate_to_event(cls, event_id, user_id):
        """
        Create new record on Event-Participant User table.
        """
        super().add(table_name=LINKER_EVENT_USER_PARTICIPANT_TABLE_NAME,
                    data={'event_id': event_id, 'user_id': user_id})

    @classmethod
    def cancel_participation(cls, event_id, user_id):
        """
        Delete record on Event-Participant User table.
        """
        super().delete(table_name=LINKER_EVENT_USER_PARTICIPANT_TABLE_NAME,
                       where={'event_id': event_id, 'user_id': user_id})

    @classmethod
    def get_registration_questions(cls, event_id):
        """
        Delete record on Event-Participant User table.
        """

        questions_res = super().select(from_tables=[EVENT_REGISTRATION_QUESTION_TABLE_NAME],
                                       where={'event_id': event_id})
        for question in questions_res:
            if question['question_type'] == 'choice':
                question['options'] = []

        # Convert questions_res to map that contains the elements as {q_id:question}
        questions_map = {question['id']: question for question in questions_res}

        # Fetch the question options
        join_statement = """ INNER JOIN {} AS O ON O.question_id = Q.id """.format(
            EVENT_REGISTRATION_QUESTION_OPTION_TABLE_NAME)

        options = super().select(from_tables=["{} AS Q".format(EVENT_REGISTRATION_QUESTION_TABLE_NAME)],
                                 return_columns=["O.*"],
                                 join_statements=[join_statement],
                                 where={"Q.event_id": event_id})

        # Add options to corresponding question
        for option in options:
            id = option['question_id']
            questions_map[id]['options'].append(option)

        # Return all registration questions of the specified event.

        return list(questions_map.values())
