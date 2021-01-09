from app.controllers.event_controller import event_repo


def create_event(user_id, club_id, event_data, registration_questions):

    event_repo.create_event(event_data, user_id)

    pass
