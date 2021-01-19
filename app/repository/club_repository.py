from app.constants.database_constants import CLUB_TABLE_INIT_STAT, \
    LINKER_CLUB_USER_EXECUTIVE_TABLE_INIT_STAT, CLUB_TABLE_NAME, \
    LINKER_CLUB_USER_PARTICIPANT_TABLE_INIT_STAT, LINKER_CLUB_USER_EXECUTIVE_TABLE_NAME, \
    LINKER_CLUB_USER_PARTICIPANT_TABLE_NAME

from app.repository import BaseRepository


class ClubRepository(BaseRepository):
    """ Repository class for the club objects.
        Performs all database operations related to clubs.
    """

    @classmethod
    def create_club(cls, club_data, user_id_who_created):
        club_data["created_by"] = user_id_who_created
        club_id = super().add(club_data, table_name=CLUB_TABLE_NAME, return_id=True)
        map_user_club = {"user_id": user_id_who_created,
                         "club_id": club_id}

        # Link the club with the user who created.
        super().add(map_user_club, table_name=LINKER_CLUB_USER_EXECUTIVE_TABLE_NAME)
        super().add(map_user_club, table_name=LINKER_CLUB_USER_PARTICIPANT_TABLE_NAME)

    @classmethod
    def get_club_by_id(cls, club_id):
        club = super().select(from_tables=[CLUB_TABLE_NAME], where={'id': club_id})
        return club

    @classmethod
    def update_club_by_id(cls, club_data):
        super().update(table_name=CLUB_TABLE_NAME, club_data=club_data, where={'id': club_data['id']})

    @classmethod
    def delete_club_by_id(cls, club_id):
        super().delete(table_name=CLUB_TABLE_NAME, where={'id': club_id})

    @classmethod
    def participate_to_club(cls, club_data, user_id_who_created):
        # TODO COMPLETE THIS FUNCTION
        club_id = super().add(club_data, table_name=CLUB_TABLE_NAME, return_id=True)
        map_user_club = {"user_id": user_id_who_created,
                         "club_id": club_id}

        # Link the club with the user who created.
        super().add(map_user_club, table_name=LINKER_CLUB_USER_EXECUTIVE_TABLE_NAME)
        super().add(map_user_club, table_name=LINKER_CLUB_USER_PARTICIPANT_TABLE_NAME)
