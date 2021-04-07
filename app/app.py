from flask import Flask, request, session, url_for, redirect, render_template
from src.service_layer import handler
from authlib.integrations.flask_client import OAuth
import logging
from src.auth import auth
from flask_cors import CORS
from src.data_layer import auth_client
import os

app = Flask(__name__)
CORS(app)

oauth = OAuth(app)
app.secret_key = "secret key"
google = oauth.register(
    name='google',
    client_id=auth_client.CLIENT_ID,
    client_secret=auth_client.CLIENT_SECRET,
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
    client_kwargs={'scope': 'openid email profile'},
)


@app.route('/getproduct/<pro_id>')
def getproduct(pro_id):
    response = {}
    token_access = request.args.get("access_token")
    if auth.verify_token(token_access):
        response = handler.getproduct(pro_id)
    else:
        response = {"error": "Not a valid Auth"}
    response = handler.getproduct(pro_id)
    return response


@app.route('/getfeaturedproduct', methods=["POST"])
def gettopproductadv():
    response = {}
    if request.method == "POST":
        # token_access = request.args.get("access_token")
        token_access = request.headers.get('Authorization')
        if auth.verify_token(token_access):
            try:
                request_data = request.json
                response = handler.gettopproductdemo(request_data)
            except Exception as e:
                print(e)
        else:
            response = {"error": "Not a valid Auth"}
    try:
        request_data = request.json
        response = handler.gettopproductdemo(request_data)
    except Exception as e:
        print(e)
    return response


@app.route('/getbrand', methods=["GET"])
def getbrand():
    token_access = request.args.get("access_token")
    response = {}
    if auth.verify_token(token_access):
        response = handler.getbrand()
    else:
        response = {"error": "Not a valid Auth"}
    response = handler.getbrand()
    return response


@app.route('/getcategory')
def getcategory():
    token_access = request.args.get("access_token")
    response = {}
    if auth.verify_token(token_access):
        response = handler.getcategory()
    else:
        response = {"error": "Not a valid Auth"}
    response = handler.getcategory()
    return response


@app.route('/getsales')
def getsales():
    token_access = request.args.get("access_token")
    response = {}
    if auth.verify_token(token_access):
        response = handler.getsales()
    else:
        response = {"error": "Not a valid Auth"}
    response = handler.getsales()
    return response


@app.route('/productbyfilter', methods=["POST"])
def productbyfilter():
    response = {}
    if request.method == "POST":
        # token_access = request.args.get("access_token")
        token_access = request.headers.get('Authorization')
        if auth.verify_token(token_access):
            try:
                request_data = request.json
                response = handler.get_product_by_filter(request_data)
            except Exception as e:
                print(e)
                return {"error": "Input is not a proper json format"}
        else:
            response = {"error": "Not a valid Auth"}
    try:
        request_data = request.json
        response = handler.get_product_by_filter(request_data)
    except Exception as e:
        print(e)
        return {"error": "Input is not a proper json format"}
    return response


@app.route('/login')
def login():
    google = oauth.create_client('google')  # create the google oauth client
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)


@app.route('/authorize', methods=["GET"])
def authorize():
    google = oauth.create_client('google')  # create the google oauth client
    token = google.authorize_access_token()  # Access token from google (needed to get user info)
    resp = google.get('userinfo')  # userinfo contains stuff u specificed in the scrope
    user_info = resp.json()
    user = oauth.google.userinfo()  # uses openid endpoint to fetch user info
    # Here you use the profile/user data that you got and query your database find/register the user
    # and set ur own data in the session not the profile from google
    session['profile'] = user_info
    session['token'] = token
    session.permanent = True  # make the session permanant so it keeps existing after broweser gets closed
    return redirect('/')


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


@app.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect('/')

@app.route('/chatbot', methods=["POST"])
def chatbot_interaction():
    if request.method == "POST":
        token_access = request.headers.get('Authorization')

        if auth.verify_token(token_access):
            data = request.json

            # Validate request body
            if ("session_id" in data) == False or ("query_string" in data) == False:
                return "Missing required parameters in body", 400

            response = handler.get_chatbot_response(data["session_id"], data["query_string"])
        else:
            response = {"error": "Not a valid Auth"}
    else:
        return {}, 404
    return response

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)


