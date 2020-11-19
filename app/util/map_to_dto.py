# DATA TRANSFER OBJECT MODELS
event_model_dto = ['id', 'title', 'description', 'start_date', 'end_date']
user_model_dto = ['id', 'email', 'name', 'surname']


def map_to_dto(dao, dto_model):
    """
    Converts data access object to data transfer object.

    :param dao: Data access object to be converted to its dto model.
    :param dto_model: A list that specifies the dto object fields.
    :return: Dto
    """
    dto = {field: dao[field] for field in dto_model}
    return dto
