from app.repository import BaseRepository
from app.constants.error_messages import AUTH_CREDENTIALS_NOT_CORRECT, NO_SUCH_USER_WITH_GIVEN_EMAIL
from app.constants.database_constants import USER_TABLE_INIT_STAT, CLUB_TABLE_NAME, \
    LINKER_CLUB_USER_EXECUTIVE_TABLE_NAME, EVENT_REGISTRATION_QUESTION_USER_RESPONSE_TABLE_NAME, \
    EVENT_REGISTRATION_QUESTION_TEXT_TYPE_USER_RESPONSE_TABLE_NAME, \
    EVENT_REGISTRATION_QUESTION_CHOICE_TYPE_USER_RESPONSE_TABLE_NAME, LINKER_CLUB_USER_PARTICIPANT_TABLE_NAME, \
    EVENT_TABLE_NAME
from app.constants.database_constants import USER_TABLE_NAME
from app.exceptions.auth_exceptions import AuthCredentialsError, NoSuchUserError


class UserRepository(BaseRepository):
    """ Repository class for the user objects.
        Performs all database operations related to user objects.
    """

    def __init__(self):
        super().__init__(table=USER_TABLE_NAME)

    @classmethod
    def initialize_table(cls):
        super().initialize_table(initialization_statement=USER_TABLE_INIT_STAT)

    @classmethod
    def create_user(cls, user_data):
        """
        Create new event on database.
        :param user_data The map that contains the user field and corresponding value.
        """
        cls.add(user_data, table_name=USER_TABLE_NAME)

    def authenticate(self, email, password):
        """
        Check given credentials.

        @:raise AuthCredentialsError if credentials are not correct.
        """

        user = super().select(where={"email": email, "password": password})
        if not user:
            raise AuthCredentialsError(AUTH_CREDENTIALS_NOT_CORRECT)

        return user.__getitem__(0)

    def get_user_by_email(self, email):
        """
        Get user by email.

        :raise: NoSuchUserError if there is not an user with given email.
        """

        user = super().select(where={"email": email})
        if not user:
            raise NoSuchUserError(NO_SUCH_USER_WITH_GIVEN_EMAIL)

        return user.__getitem__(0)

    def get_user_id_by_email(self, email):
        """
        Get user ID by email.

        :raise: NoSuchUserError if there is not an user with given email.
        """

        user_id = super().select(where={"email": email}, return_columns=["id"])
        if not user_id:
            raise NoSuchUserError(NO_SUCH_USER_WITH_GIVEN_EMAIL)

        return user_id.__getitem__(0)["id"]

    @classmethod
    def get_clubs_executed_by_user(cls, user_id, return_columns, extra_fields):
        """
            Return the clubs executed by user.

        :param user_id: Executive user id
        :param return_columns: The columns that will be returned
        :return: List of clubs
        """

        from_statements = [" club  as c "]
        return_columns = ["c.{}".format(column) for column in return_columns]
        join_statements = []

        get_clubs_join = " JOIN {} as cue ON cue.club_id = c.id AND cue.user_id = {} ".format(
            LINKER_CLUB_USER_EXECUTIVE_TABLE_NAME, user_id)
        join_statements.append(get_clubs_join)

        clubs = super().select(return_columns=return_columns, from_tables=from_statements,
                               join_statements=join_statements, group_by=[" c.id "])

        if extra_fields:
            if 'event_num' in extra_fields:
                get_event_num_join = " LEFT JOIN {} as e ON e.created_by = c.id ".format(EVENT_TABLE_NAME)

                event_num = super().select(return_columns=[" c.id, count(e) as event_num "],
                                           from_tables=[" {} as c".format(CLUB_TABLE_NAME)],
                                           join_statements=[get_event_num_join], group_by=[" c.id "])

                # TODO: REFACTOR THIS PART !!!!!!
                for club in event_num:
                    for cl in clubs:
                        if cl['id'] == club['id']:
                            cl['event_num'] = club['event_num']
                            break

            if 'participant_num' in extra_fields:
                get_participant_num_join = " LEFT JOIN {} as cup ON cup.club_id = c.id " \
                                           " LEFT JOIN {} as u ON u.id = cup.user_id " \
                    .format(LINKER_CLUB_USER_PARTICIPANT_TABLE_NAME, USER_TABLE_NAME)

                participant_num = super().select(return_columns=[" c.id, count(u) as participant_num "],
                                                 from_tables=[" {} as c".format(CLUB_TABLE_NAME)],
                                                 join_statements=[get_participant_num_join], group_by=[" c.id "])

                # TODO: REFACTOR THIS PART !!!!!!
                for club in participant_num:
                    for cl in clubs:
                        if cl['id'] == club['id']:
                            cl['participant_num'] = club['participant_num']
                            break

        return clubs

    @classmethod
    def save_registration_questions_responses(cls, user_responses, user_id):
        """
            Save user responses to database.

        :param user_responses:  The user answers to event registration questions.
        :param user_id
        """

        for question_id in user_responses.keys():
            user_response = user_responses[question_id]

            new_user_response = {'question_id': question_id, 'user_id': user_id, 'response_type': user_response['type']}

            user_response_id = super().add(table_name=EVENT_REGISTRATION_QUESTION_USER_RESPONSE_TABLE_NAME,
                                           data=new_user_response, return_id=True)

            if user_response['type'] == 'text':
                new_text_user_response = {'id': user_response_id, 'user_response': user_response['answer']}
                super().add(table_name=EVENT_REGISTRATION_QUESTION_TEXT_TYPE_USER_RESPONSE_TABLE_NAME,
                            data=new_text_user_response)

            elif user_response['type'] == 'choice':
                new_choice_user_response = {'id': user_response_id, 'selected_option_id': user_response['answer']}
                super().add(table_name=EVENT_REGISTRATION_QUESTION_CHOICE_TYPE_USER_RESPONSE_TABLE_NAME,
                            data=new_choice_user_response)

    @classmethod
    def delete_registration_questions_responses(cls, question_ids, user_id):
        """
            Delete user's responses from database.

        :param question_ids:  The ids of the questions from which the user's answers will be deleted.
        :param user_id
        """

        for q_id in question_ids:
            super().delete(table_name=EVENT_REGISTRATION_QUESTION_USER_RESPONSE_TABLE_NAME,
                           where={'question_id': q_id['id'], 'user_id': user_id})
