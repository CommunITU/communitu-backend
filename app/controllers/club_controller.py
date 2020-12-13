from app.repository.club_repository import ClubRepository
from flask import Blueprint, request

from app.services.auth_service import require_token

club_api = Blueprint('club_api', __name__)
er = ClubRepository()


@club_api.route("/clubs", methods=['POST'])
@require_token(request)
def create_club(user_id="", user_email=""):
    # TODO: ADD PYDOC

    # TODO: IMPLEMENT SERVICE AND REPOSITORY FUNCTIONS
    return "ok"
