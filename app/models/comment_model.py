from app.models.base_model import BaseModel


class CommentModel(BaseModel):
    """ Model class for the comment objects """

    def __init__(self, content, user_id):
        self.content = content
        self.user_id = user_id
        super().__init__(id=0, create_date="create", update_date="update")
