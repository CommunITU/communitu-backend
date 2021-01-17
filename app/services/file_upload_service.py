from pyrebase import pyrebase

config = {
    'apiKey': "AIzaSyA121lUAo69l4-1P9oAG83N7pL_e6wyXyQ",
    'authDomain': "communitu.firebaseapp.com",
    'databaseURL': "https://communitu-default-rtdb.firebaseio.com",
    'projectId': "communitu",
    'storageBucket': "communitu.appspot.com",
    'messagingSenderId': "696413296279",
    'appId': "1:696413296279:web:890d7e9e3427ffc1c0bbd2"
}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()


def upload_club_photo(file, club_id):
    """
        Upload club photos to firebase storage.
    """
    upload = storage.child("images/clubs/{}".format(club_id)).put(file)
    file_url = storage.child(upload['name']).get_url(upload['downloadTokens'])
    return file_url


def upload_event_photo(file, event_id):
    """
          Upload event photos to firebase storage.
      """
    upload = storage.child("images/events/{}".format(event_id)).put(file)
    file_url = storage.child(upload['name']).get_url(upload['downloadTokens'])
    return file_url
