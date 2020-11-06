from app.models.base_model import BaseModel


class EventModel(BaseModel):
    """ Model class for the event objects """

    def __init__(self, title, description, start_date, end_date, quota):
        self.title = title
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.quota = quota
        super().__init__(id=0, create_date="create", update_date="update")

    @property
    def get_title(self):
        return self.title

    @get_title.setter
    def set_title(self, title):
        self.title = title
