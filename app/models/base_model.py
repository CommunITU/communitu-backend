class BaseModel:
    """ Base class for the models.  """

    def __init__(self, id, create_date, update_date):
        self.id = id
        self.create_date = create_date
        self.update_date = update_date
