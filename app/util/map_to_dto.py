event_model_dto = ['id', 'title', 'description', 'start_date', 'end_date']


def map_to_dto(dao, dto_model):
    dto = {field: dao[field] for field in dto_model}
    return dto
