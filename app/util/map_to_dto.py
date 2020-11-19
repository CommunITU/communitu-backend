event_model_dto = ['id', 'title', 'description', 'start_date', 'end_date']
user_model_dto = ['id', 'email', 'name', 'surname']


def map_to_dto(dao, dto_model):
    dto = {field: dao[field] for field in dto_model}
    return dto
