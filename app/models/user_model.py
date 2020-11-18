from app.models.base_model import BaseModel


class UserModel(BaseModel):
    """ Model class for the user objects """

    def __init__(self, email="", password="", name="", surname=""):
        self.email = email
        self.password = password
        self.name = name
        self.surname = surname
        super().__init__(id=0, create_date="created_date", update_date="updated_date")
