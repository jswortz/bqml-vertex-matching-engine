import os

CLIENT_ID = os.environ.get('OAUTH_CLIENT') if 'OAUTH_CLIENT' in os.environ else "569181271116-9heitgoi3rnpq41hmdvvu2vbflkiqdoj.apps.googleusercontent.com"          #Google OAuth 2.0 Client id
CLIENT_SECRET = os.environ.get('OAUTH_KEY') if 'OAUTH_KEY' in os.environ else "UMKpyXQwjoc8hFjBlH4pEPbw"      #Google OAuth 2.0 Client secret
#CLIENT_ID = "52337824704-t9jfkcn0evvbinsimkaedd88toonvdjl.apps.googleusercontent.com"
#CLIENT_SECRET = "WIGEV2j1ESI6TVHnZhjAnJGA"