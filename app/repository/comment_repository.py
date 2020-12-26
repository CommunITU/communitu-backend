from app.constants.database_constants import EVENT_COMMENT_TABLE_INIT_STAT, LINKER_COMMENT_REPLY_TABLE_INIT_STAT
from app.constants.database_constants import EVENT_COMMENT_TABLE_NAME
from app.repository import BaseRepository


class CommentRepository(BaseRepository):
    """ Repository class for the comment objects.
        Performs all database operations related to comment objects.
    """

    #TODO MOVE THIS REPO TO EVENT

    def __init__(self):
        super().__init__(table=EVENT_COMMENT_TABLE_NAME)

    @classmethod
    def initialize_table(cls):
        super().initialize_table(initialization_statement=EVENT_COMMENT_TABLE_INIT_STAT)
        super().initialize_table(initialization_statement=LINKER_COMMENT_REPLY_TABLE_INIT_STAT)
