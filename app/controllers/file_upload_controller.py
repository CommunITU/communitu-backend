from flask import Blueprint, request, make_response, jsonify

from app.services import file_upload_service as fus

upload_api = Blueprint('upload_api', __name__)


@upload_api.route("/upload/clubs/<club_id>", methods=['POST'])
def upload_club_photo(club_id):
    photo = request.files.get('file')
    try:
        file_url = fus.upload_club_photo(photo, club_id)
    except Exception as e:
        return make_response(jsonify({'message': str(e)}), 400)

    return make_response(jsonify({'file_url': file_url, 'message': "File uploaded successfully!"}), 200)


@upload_api.route("/upload/events/<event_id>", methods=['POST'])
def upload_event_photo(event_id):
    photo = request.files.get('file')
    try:
        file_url = fus.upload_event_photo(photo, event_id)
    except Exception as e:
        return make_response(jsonify({'message': str(e)}), 400)

    return make_response(jsonify({'file_url': file_url, 'message': "File uploaded successfully!"}), 200)
