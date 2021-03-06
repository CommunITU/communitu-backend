# DATA TRANSFER OBJECT MODELS
event_model_dto = ['id', 'name', 'description', 'image_url', 'start_date', 'end_date', 'location', 'quota',
                   'created_by']
user_model_dto = ['id', 'email', 'name', 'surname', 'profile_photo_url']


def map_to_dto(dao_obj, dto_model):
    """
    Converts data access object to data transfer object.

    :param dao: Data access object to be converted to its dto model.
    :param dto_model: A list that specifies the dto object fields.
    :return: Dto
    """
    dto = {field: dao_obj[field] for field in dto_model}
    return dto
