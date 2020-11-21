from app.repository.base_repository import BaseRepository
from app.constants.database_constants import COMMENT_DB_TABLE_INIT_STAT, REPLYTO_TABLE_INIT_STAT
from app.constants.database_constants import REPLYTO_DB_TABLE_NAME
from app.constants.database_constants import COMMENT_DB_TABLE_NAME


class CommentRepository(BaseRepository):
    """ Repository class for the comment objects.
        Performs all database operations related to comment objects.
    """

    def __init__(self):
        super().__init__(table=COMMENT_DB_TABLE_NAME)

    def initialize_table(self):
        super().initialize_table(initialization_statement=COMMENT_DB_TABLE_INIT_STAT)
        super().initialize_table(initialization_statement=REPLYTO_TABLE_INIT_STAT)
