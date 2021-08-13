from google.oauth2 import id_token
from google.auth.transport import requests
from src.data_layer import auth_client


def verify(session, access_token):
    try:
        if session['token']['access_token'].strip() == access_token.strip():
            return True
        else:
            print(session['token']['access_token'])
            return False
    except Exception as e:
        print(e)
        return False


def verify_token(token):
    client_id = auth_client.CLIENT_ID
    try:
        idinfo = id_token.verify_oauth2_token(
            token,
            requests.Request(),
            client_id
        )
        userid = idinfo['sub']
        return True
    except Exception as e:
        print(e)
        return False
